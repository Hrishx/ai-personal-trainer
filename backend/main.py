#Main.py
import cv2
import time

from core.vision_engine import VisionEngine
from core.biomechanics_engine import BiomechanicsEngine
from core.posture_state_builder import PostureStateBuilder
from core.trend_analyzer import TrendAnalyzer
from core.fatigue_analyzer import FatigueAnalyzer
from core.coach_llm_engine import CoachLLMEngine
from core.voice_engine import VoiceCoach
from core.user_profile import UserProfile
from core.temporal_engine import TemporalEngine
from core.rep_quality_engine import RepQualityEngine
from core.advanced_fatigue_engine import AdvancedFatigueEngine
from core.exercise_detector import ExerciseDetector
from core.realtime_coach import RealtimeCoach
from core.exercise_coach import ExerciseCoach

from core.rep_phase_engine import RepPhaseEngine
from core.error_detection_engine import ErrorDetectionEngine
from core.injury_risk_engine import InjuryRiskEngine
from core.rep_analyzer import RepAnalyzer


# 🔥 GLOBAL ENGINE INIT (ADD THIS)

vision = VisionEngine()
biomech = BiomechanicsEngine()
state_builder = PostureStateBuilder()
trend = TrendAnalyzer()
fatigue = FatigueAnalyzer()

coach_llm = CoachLLMEngine()
voice = VoiceCoach()

temporal = TemporalEngine()
rep_quality = RepQualityEngine()
advanced_fatigue = AdvancedFatigueEngine()
rep_analyzer = RepAnalyzer()

exercise_detector = ExerciseDetector()
realtime_coach = RealtimeCoach()
exercise_coach = ExerciseCoach()

rep_phase_engine = RepPhaseEngine()
error_engine = ErrorDetectionEngine()
injury_engine = InjuryRiskEngine()

user_profile = UserProfile()
user_profile.set_profile(style="elite")

coach_llm.warmup()

# 🔥 GLOBAL STATE VARIABLES
rep_logged = 0
set_data = []
score = 0
rep_flash = 0
knee_path = []
knee_smooth = []

def reset_all_state():
    global rep_logged, set_data, score, biomech

    print("🔥 FULL BACKEND RESET")

    rep_logged = 0
    set_data.clear()
    score = 0

    # ✅ RESET ENGINES FIRST
    for engine in [
        temporal,
        advanced_fatigue,
        rep_phase_engine,
        rep_analyzer
    ]:
        try:
            engine.reset()
        except:
            pass

    try:
        rep_phase_engine.current_phase = None
    except:
        pass

    try:
        biomech.reset()
    except:
        pass

    try:
        trend.reset()
    except:
        pass

    # 🔥 FINAL OVERRIDE (VERY IMPORTANT)
    try:
        biomech.rep_count = 0
    except:
        pass
def process_single_frame(frame):

    global rep_logged, set_data, score, rep_flash, knee_path, knee_smooth

    landmarks = vision.process_frame(frame)

    if not landmarks:
        return {
            "reps": rep_logged,
            "phase": "NONE",
            "feedback": "No person detected",
            "score": score,
            "fatigue": 0,
            "zoom": 1,   # ✅ ADD DEFAULT
            "detected_exercise": "None"
        }

    # 👇 ADD ZOOM CODE HERE (after landmarks check)
    # =========================
    # AUTO ZOOM CALCULATION
    # =========================

    h, w, _ = frame.shape

    # head (nose) and feet landmarks
    head = landmarks[0]
    left_foot = landmarks[31]
    right_foot = landmarks[32]

    # convert to pixel coordinates
    head_y = int(head.y * h)
    foot_y = int(max(left_foot.y, right_foot.y) * h)

    person_height = abs(foot_y - head_y)

    # ratio of person to frame
    ratio = person_height / h

    # zoom logic
    if ratio < 0.4:
        zoom = 1.4   # far → zoom in
    elif ratio > 0.8:
        zoom = 0.9   # too close → zoom out
    else:
        zoom = 1.0

    exercise, confidence = exercise_detector.detect_exercise(landmarks)

    if exercise == "squat":
        biomech_data = biomech.analyze_squat(landmarks, frame.shape)

    elif exercise == "pushup":
        biomech_data = biomech.analyze_pushup(landmarks, frame.shape)

    elif exercise == "lunge":
        biomech_data = biomech.analyze_lunge(landmarks, frame.shape)

    elif exercise == "plank":
        biomech_data = biomech.analyze_plank(landmarks, frame.shape)

    else:
        return None

    posture_state = state_builder.build_state(biomech_data)
    posture_state = trend.analyze(posture_state)
    posture_state = fatigue.analyze(posture_state)

    rep = biomech_data["rep_count"]
    knee_angle = biomech_data["knee_angle"]

    temporal.update(knee_angle)
    smoothness = temporal.get_smoothness()

    phase = rep_phase_engine.update(knee_angle)

    errors = error_engine.detect(posture_state, biomech_data)

    corrections = []

    # 🔥 RULE BASED POSTURE CORRECTION

    if posture_state["knee_status"] == "mild_valgus":
        corrections.append("⚠️ Keep your knees aligned with toes")

    if posture_state["back_status"] != "neutral":
        corrections.append("⚠️ Keep your back straight")

    if posture_state["depth_status"] != "good_depth":
        corrections.append("⬇️ Go lower for proper depth")

    # ✅ FINAL FEEDBACK
    if corrections:
        feedback = " | ".join(corrections)
    else:
        feedback = "✅ Good form"

    if rep > rep_logged:
        rep_logged = rep

        score = rep_quality.score_rep(
            posture_state,
            biomech_data,
            smoothness
        )

        advanced_fatigue.update(score)

        fatigue_state = advanced_fatigue.detect_fatigue()

        set_data.append({
            "rep": rep,
            "quality_score": score,
            "knee": posture_state["knee_status"],
            "back": posture_state["back_status"],
            "depth": posture_state["depth_status"],
            "fatigue": fatigue_state
        })

        rep_analyzer.analyze_rep(set_data[-1])

    fatigue_state = advanced_fatigue.detect_fatigue()
    fatigue_value = 20 if fatigue_state == "fresh" else 70

    return {
        "reps": rep,
        "phase": phase,
        "feedback": feedback if feedback else "Good form",
        "score": score,
        "fatigue": fatigue_value, # ✅ THIS WAS MISSING
        "zoom": zoom,
        "detected_exercise": exercise
    }


VIDEO_PATH = r"D:\1- Phase\backend\squat_video\squats.mp4"

TARGET_REPS = 4

DISPLAY_WIDTH = 960
DISPLAY_HEIGHT = 720

MODE = "video"   # "video" or "camera"
# --------------------------------
# DASHBOARD
# --------------------------------

def draw_dashboard(frame, exercise, rep, phase, score, fatigue, error):

    cv2.putText(frame, f"Exercise: {exercise}", (30,40),
                cv2.FONT_HERSHEY_SIMPLEX,0.8,(0,255,255),2)

    cv2.putText(frame, f"Reps: {rep}", (30,70),
                cv2.FONT_HERSHEY_SIMPLEX,0.8,(0,255,0),2)

    cv2.putText(frame, f"Phase: {phase}", (30,100),
                cv2.FONT_HERSHEY_SIMPLEX,0.8,(255,255,0),2)

    bar_length = 220
    bar_height = 20

    x = 30
    y = 130

    filled = int((score / 100) * bar_length)

    if score >= 80:
        color = (0,255,0)
    elif score >= 60:
        color = (0,165,255)
    else:
        color = (0,0,255)

    cv2.rectangle(frame,(x,y),(x+bar_length,y+bar_height),(40,40,40),-1)
    cv2.rectangle(frame,(x,y),(x+filled,y+bar_height),color,-1)

    cv2.putText(frame,
                f"Form Score: {score}%",
                (x, y-5),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (255,255,255),
                2)

    fatigue_color = (0,200,255)

    if fatigue == "fatigued":
        fatigue_color = (0,0,255)

    cv2.putText(frame,
                f"Fatigue: {fatigue}",
                (30,190),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                fatigue_color,
                2)

    error_color = (0,0,255)

    if error == "None":
        error_color = (0,255,0)

    cv2.putText(frame,
                f"Error: {error}",
                (30,220),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                error_color,
                2)


# --------------------------------
# MAIN
# --------------------------------

def main():

    print("Starting AI Fitness Coach")

    vision = VisionEngine()
    biomech = BiomechanicsEngine()
    state_builder = PostureStateBuilder()
    trend = TrendAnalyzer()
    fatigue = FatigueAnalyzer()

    coach_llm = CoachLLMEngine()
    voice = VoiceCoach()

    temporal = TemporalEngine()
    rep_quality = RepQualityEngine()
    advanced_fatigue = AdvancedFatigueEngine()
    rep_analyzer = RepAnalyzer()

    exercise_detector = ExerciseDetector()
    realtime_coach = RealtimeCoach()
    exercise_coach = ExerciseCoach()

    rep_phase_engine = RepPhaseEngine()
    error_engine = ErrorDetectionEngine()
    injury_engine = InjuryRiskEngine()

    user_profile = UserProfile()
    user_profile.set_profile(style="elite")

    if MODE == "camera":
        camera = cv2.VideoCapture(0)
    else:
        camera = cv2.VideoCapture(VIDEO_PATH)
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    camera.set(cv2.CAP_PROP_BUFFERSIZE, 1)
    cv2.namedWindow("AI Trainer", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("AI Trainer", DISPLAY_WIDTH, DISPLAY_HEIGHT)

    coach_llm.warmup()

    print("System Ready")

    intro_done = False
    rep_logged = 0
    set_data = []
    score = 0
    rep_flash = 0

    # trajectory buffers
    knee_path = []
    knee_smooth = []

    while True:

        ret, frame = camera.read()
        frame = cv2.flip(frame, 1)

        if not ret:
            if MODE == "video":
                camera.set(cv2.CAP_PROP_POS_FRAMES, 0)
                continue
            else:
                break

        landmarks = vision.process_frame(frame)

        if landmarks:

            exercise, confidence = exercise_detector.detect_exercise(landmarks)

            if confidence > 0.8 and not intro_done and biomech.rep_count > 0:

                intro = exercise_coach.get_intro(exercise)
                voice.speak(intro)

                intro_done = True

            if exercise == "squat":
                biomech_data = biomech.analyze_squat(landmarks, frame.shape)

            elif exercise == "pushup":
                biomech_data = biomech.analyze_pushup(landmarks, frame.shape)

            elif exercise == "lunge":
                biomech_data = biomech.analyze_lunge(landmarks, frame.shape)

            elif exercise == "plank":
                biomech_data = biomech.analyze_plank(landmarks, frame.shape)

            else:
                continue

            posture_state = state_builder.build_state(biomech_data)
            posture_state = trend.analyze(posture_state)
            posture_state = fatigue.analyze(posture_state)

            rep = biomech_data["rep_count"]
            knee_angle = biomech_data["knee_angle"]

            temporal.update(knee_angle)

            smoothness = temporal.get_smoothness()

            phase = rep_phase_engine.update(knee_angle)

            errors = error_engine.detect(posture_state, biomech_data)

            injury_engine.update(errors)

            risks = injury_engine.assess_risk()

            feedback = realtime_coach.get_feedback(
                posture_state,
                errors,
                phase
            )

            if feedback and not voice.is_speaking():
                voice.speak(feedback)

            # -------------------------
            # REP LOGGING
            # -------------------------

            if rep > rep_logged:

                rep_logged = rep
                rep_flash =12
                knee_path.clear()
                knee_smooth.clear()

                score = rep_quality.score_rep(
                    posture_state,
                    biomech_data,
                    smoothness
                )

                advanced_fatigue.update(score)

                fatigue_state = advanced_fatigue.detect_fatigue()

                set_data.append({
                    "rep": rep,
                    "quality_score": score,
                    "knee": posture_state["knee_status"],
                    "back": posture_state["back_status"],
                    "depth": posture_state["depth_status"],
                    "fatigue": fatigue_state
                })

                rep_report = rep_analyzer.analyze_rep(set_data[-1])

                print(rep_report)
                print(f"Rep {rep}: Quality Score:", score)

            error_text = "None"

            if errors:
                error_text = errors[0]

            draw_dashboard(
                frame,
                exercise,
                rep,
                phase,
                score,
                posture_state["fatigue_level"],
                error_text
            )
            
            # REP SUCCESS ICON

            if rep_flash > 0:

                cv2.circle(frame,(820,120),60,(0,255,0),-1)

                cv2.putText(
                    frame,
                    "✓",
                    (800,145),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    2,
                    (255,255,255),
                    3
                )

                rep_flash -= 1
            
            
            if feedback:

                cv2.putText(
                    frame,
                    feedback,
                    (30, 260),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    (255,255,255),
                    2
                )
            

            # -------------------------
            # SMOOTH KNEE TRAJECTORY
            # -------------------------

            if phase in ["ECCENTRIC", "CONCENTRIC"]:

                knee_x = int(landmarks[26].x * frame.shape[1])
                knee_y = int(landmarks[26].y * frame.shape[0])

                # smoothing buffer
                knee_smooth.append((knee_x, knee_y))

                if len(knee_smooth) > 5:
                    knee_smooth.pop(0)

                # average position
                avg_x = int(sum(p[0] for p in knee_smooth) / len(knee_smooth))
                avg_y = int(sum(p[1] for p in knee_smooth) / len(knee_smooth))

                if not knee_path:
                    knee_path.append((avg_x, avg_y))
                else:
                    prev_x, prev_y = knee_path[-1]

                    movement = abs(avg_x - prev_x) + abs(avg_y - prev_y)

                    # ignore jitter
                    if movement > 5:
                        knee_path.append((avg_x, avg_y))

                if len(knee_path) > 40:
                    knee_path.pop(0)

            # draw trajectory
            for i in range(1, len(knee_path)):
                cv2.line(frame, knee_path[i-1], knee_path[i], (255,0,255), 2)

            # -------------------------
            # SKELETON
            # -------------------------

            connections = [
                (11,12),(11,13),(13,15),
                (12,14),(14,16),
                (11,23),(12,24),
                (23,25),(24,26),
                (25,27),(26,28)
            ]

            line_color = (0,255,0)

            if "knee_valgus" in errors:
                line_color = (0,0,255)

            elif "forward_lean" in errors:
                line_color = (0,0,255)

            elif "shallow_depth" in errors:
                line_color = (0,165,255)

            for i,j in connections:

                pt1 = (
                    int(landmarks[i].x * frame.shape[1]),
                    int(landmarks[i].y * frame.shape[0])
                )

                pt2 = (
                    int(landmarks[j].x * frame.shape[1]),
                    int(landmarks[j].y * frame.shape[0])
                )

                cv2.line(frame, pt1, pt2, line_color, 3)

            for idx in [11,12,13,14,15,16,23,24,25,26,27,28]:

                x = int(landmarks[idx].x * frame.shape[1])
                y = int(landmarks[idx].y * frame.shape[0])

                cv2.circle(frame,(x,y),5,line_color,-1)

            # -------------------------
            # SET COMPLETE
            # -------------------------

            if rep >= TARGET_REPS:

                print("\nSet complete. Generating report...\n")

                scores = [r["quality_score"] for r in set_data]
                avg_score = sum(scores)/len(scores)

                summary_data = {
                    "total_reps": len(set_data),
                    "average_score": round(avg_score,2),
                    "rep_data": set_data,
                    "rep_analysis": rep_analyzer.get_rep_reports(),
                    "injury_risks": risks
                }

                coach_llm.request_set_summary(
                    summary_data,
                    user_profile.get_profile()
                )

                print("Waiting for AI coach analysis...\n")

                start = time.time()

                while True:

                    msg = coach_llm.get_latest_message()

                    if msg:

                        print("====================")
                        print("AI COACH REPORT")
                        print("====================\n")
                        print(msg)

                        voice.speak(msg[:300])

                        break

                    if time.time() - start > 120:
                        break

                    time.sleep(0.2)

                break

        frame_display = cv2.resize(frame,(DISPLAY_WIDTH,DISPLAY_HEIGHT))

        cv2.imshow("AI Trainer", frame_display)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    camera.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()