#app.py

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import cv2
import numpy as np
import sys
import os
import time

# 🔥 Ensure proper path
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

# 🔥 IMPORT YOUR REAL AI PIPELINE
from main import process_single_frame, coach_llm, rep_analyzer, set_data

app = FastAPI()

# 🔥 CORS (for Next.js frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🧠 LIVE DATA (cache)
latest_data = {
    "reps": 0,
    "phase": "idle",
    "feedback": "Starting...",
    "score": 0
}

# 🧠 SUMMARY DATA
summary_data = {
    "totalReps": 0,
    "avgFormScore": 0,
    "fatigueLevel": 0,
    "errors": [],
    "report": "Workout not completed yet"
}


# ✅ HEALTH CHECK
@app.get("/test")
def test():
    return {"message": "AI Coach Running (Frame Mode)"}


# 🔥 RESET SESSION (VERY IMPORTANT)
from main import reset_all_state

@app.post("/reset_session")
def reset_session():
    global summary_data

    reset_all_state()   # 🔥 THIS LINE FIXES EVERYTHING

    coach_llm.reset()

    summary_data = {
        "totalReps": 0,
        "avgFormScore": 0,
        "fatigueLevel": 0,
        "errors": [],
        "report": "Workout not completed yet"
    }

    return {"message": "Session reset"}
# 🔥 MAIN API — FRAME PROCESSING
@app.post("/process_frame")
async def process_frame(request: Request):
    global latest_data, summary_data

    try:
        body = await request.body()

        np_arr = np.frombuffer(body, np.uint8)
        frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        if frame is None:
            return {"error": "Invalid frame"}

        result = process_single_frame(frame)

        if result is None:
            return latest_data

        latest_data = result

        # 🔥 update summary live
        summary_data["totalReps"] = result.get("reps", 0)
        summary_data["avgFormScore"] = result.get("score", 0)
        fatigue = int((100 - result.get("score", 0)) * 0.7)

        summary_data["fatigueLevel"] = min(100, max(0, fatigue))

        return result

    except Exception as e:
        return {"error": str(e)}


# ✅ DEBUG API
@app.get("/data")
def get_data():
    return latest_data


# ✅ SUMMARY API
@app.get("/summary")
def get_summary():
    return summary_data


# 🔥 GENERATE FINAL REPORT
@app.post("/generate_summary")
def generate_summary():
    global summary_data

    try:
        print("Generating summary...")
        print("SET DATA:", set_data)

        if not set_data:
            return {"report": "No workout data captured"}

        # ✅ calculate real average
        scores = [r["quality_score"] for r in set_data]
        avg_score = sum(scores) / len(scores)

        summary = {
            "total_reps": len(set_data),
            "average_score": round(avg_score, 2),
            "rep_data": set_data,
            "rep_analysis": rep_analyzer.get_rep_reports(),
            "injury_risks": []
        }

        print("Sending request to Ollama...")

        # 🔥 CLEAR OLD RESPONSE
        coach_llm.latest_response = None

        # 🔥 START LLM
        coach_llm.reset()  # 🔥 reset LLM state
        coach_llm.request_set_summary(summary, {"style": "elite"})

        start = time.time()

        while True:
            msg = coach_llm.get_latest_message()

            import json

            if msg:
                print("LLM response received")

                if msg:
                    print("LLM response received")

                    try:
                        # ✅ FIX
                        if isinstance(msg, dict):
                            parsed = msg
                        else:
                            parsed = json.loads(msg)

                        return {
                            "performance": parsed.get("performance", ""),
                            "corrections": parsed.get("corrections", ""),
                            "injury": parsed.get("injury", ""),
                            "motivation": parsed.get("motivation", ""),
                            "total_reps": len(set_data),
                            "average_score": round(avg_score, 2),
                            "fatigue": summary_data.get("fatigueLevel", 0)
                        }

                    except Exception as e:
                        print("Parse failed:", e)

                        return {
                            "performance": str(msg),
                            "corrections": "",
                            "injury": "",
                            "motivation": "",
                            "total_reps": len(set_data),
                            "average_score": round(avg_score, 2)
                        }

            # 🔥 if LLM finished but no message
            if not coach_llm.running:
                return {
                    "report": "LLM failed",
                    "total_reps": len(set_data),
                    "average_score": round(avg_score, 2)
                }

            # 🔥 timeout safety
            if time.time() - start > 60:
                return {
                    "report": "LLM timeout",
                    "total_reps": len(set_data),
                    "average_score": round(avg_score, 2)
                }

            time.sleep(0.1)

    except Exception as e:
        print("ERROR:", e)
        return {"error": str(e)}