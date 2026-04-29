#coach_llm_engine.py
import requests
import threading
import re

class CoachLLMEngine:

    def __init__(self):

        # Model
        self.model = "qwen2.5:3b-instruct"

        # Ollama API
        self.url = "http://localhost:11434/api/chat"

        self.latest_response = None
        self.lock = threading.Lock()

        self.running = False

    # ==========================================
    # LLM WARMUP
    # ==========================================

    def warmup(self):

        try:

            print("Warming up LLM...")

            requests.post(
                self.url,
                json={
                    "model": self.model,
                    "messages": [
                        {"role": "user", "content": "hello"}
                    ],
                    "options": {
                        "num_predict": 20
                    },
                    "stream": False
                },
                timeout=60
            )

            print("LLM Ready")

        except Exception as e:

            print("LLM warmup failed:", e)
            
    def reset(self):
        self.latest_response = None
        self.running = False

    # ==========================================
    # REQUEST SUMMARY
    # ==========================================

    def request_set_summary(self, summary_data, user_profile):

        if self.running:
            print("LLM already running, skipping...")
            return

        self.running = True

        thread = threading.Thread(
            target=self._generate_set_summary,
            args=(summary_data, user_profile)
        )

        thread.daemon = True
        thread.start()

    # ==========================================
    # FORMAT REP DATA
    # ==========================================

    def _format_rep_data(self, rep_data):

        lines = []

        for rep in rep_data:

            line = (
                f"Rep {rep['rep']} | "
                f"Score: {rep['quality_score']} | "
                f"Knee: {rep['knee']} | "
                f"Back: {rep['back']} | "
                f"Depth: {rep['depth']} | "
                f"Fatigue: {rep['fatigue']}"
            )

            lines.append(line)

        return "\n".join(lines)

    # ==========================================
    # FORMAT REP ANALYSIS
    # ==========================================

    def _format_rep_analysis(self, analysis):

        if isinstance(analysis, list):
            return "\n".join(analysis)

        return str(analysis)

    # ==========================================
    # GENERATE REPORT
    # ==========================================

    def _generate_set_summary(self, summary_data, user_profile):

        try:

            rep_data_text = self._format_rep_data(summary_data["rep_data"])

            rep_analysis_text = self._format_rep_analysis(
                summary_data.get("rep_analysis", [])
            )

            prompt = prompt = f"""
You are an AI strength coach analyzing a squat workout.

Workout Summary
Total reps: {summary_data['total_reps']}

Rep-by-Rep Analysis:
{rep_analysis_text}

Detailed Rep Data:
{rep_data_text}

Injury Risks:
{summary_data.get('injury_risks', [])}

---

TASK:
Generate a structured coaching report.

OUTPUT FORMAT (STRICT — FOLLOW EXACTLY):

Performance Overview:
<write 3-4 lines paragraph>

Form Corrections:
<write 2-3 sentences>

Injury Prevention:
<write 2-3 sentences>

Motivation:
<write exactly 2 sentences>

---

STRICT RULES:
- ALL 4 sections MUST be present
- DO NOT skip any section
- DO NOT rename headings
- DO NOT merge sections
- DO NOT leave any section empty
- If no issue exists, still write a meaningful sentence

STYLE:
- Natural human tone
- No bullet points
- No extra headings
- Clean readable paragraphs

FAIL CONDITION:
If any section is missing, the output is INVALID.

Now generate the report.
"""

            print("Sending request to Ollama...")

            response = requests.post(
                self.url,
                json={
                    "model": self.model,
                    "messages": [
                        {"role": "user", "content": prompt}
                    ],
                    "options": {
                        "num_predict": 120,
                        "temperature": 0.3
                    },
                    "stream": False
                },
                timeout=180
            )

            if response.status_code != 200:

                print("LLM ERROR:", response.text)
                self.running = False
                return

            data = response.json()

            message = data.get("message", {}).get("content", "")
            print("\n================ RAW LLM OUTPUT ================\n")
            print(message)
            print("\n===============================================\n")

            def parse_report(text):
                sections = {
                    "performance": "",
                    "corrections": "",
                    "injury": "",
                    "motivation": ""
                }

                # Keep original text (DO NOT lower everything)
                patterns = {
                    "performance": r"Performance Overview:\s*(.*?)(Form Corrections:|Injury Prevention:|Motivation:|$)",
                    "corrections": r"Form Corrections:\s*(.*?)(Injury Prevention:|Motivation:|$)",
                    "injury": r"Injury Prevention:\s*(.*?)(Motivation:|$)",
                    "motivation": r"Motivation:\s*(.*)"
                }

                for key, pattern in patterns.items():
                    match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
                    if match:
                        sections[key] = match.group(1).strip()

                return sections


            parsed = parse_report(message)
            if not parsed["injury"]:
                parsed["injury"] = "Maintain proper alignment and controlled movement to avoid unnecessary joint stress."

            if not parsed["motivation"]:
                parsed["motivation"] = "You're improving consistently. Keep pushing your limits with focus and control."
            print("\n================ PARSED OUTPUT ================\n")
            print(parsed)
            print("\n==============================================\n")

            with self.lock:
                self.latest_response = parsed

            print("LLM response received")

        except Exception as e:

            print("LLM ERROR:", e)

        self.running = False

    # ==========================================
    # GET RESPONSE
    # ==========================================

    def get_latest_message(self):

        with self.lock:

            msg = self.latest_response
            self.latest_response = None

        return msg