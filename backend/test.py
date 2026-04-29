import cv2
import time
import threading  # 🔥 NEW

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


VIDEO_PATH = r"D:\1- Phase\squat_video\squats.mp4"

TARGET_REPS = 5

DISPLAY_WIDTH = 960
DISPLAY_HEIGHT = 720


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

    # 🔥 CAMERA OPTIMIZED
    camera = cv2.VideoCapture(0)
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, 800)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 600)
    camera.set(cv2.CAP_PROP_BUFFERSIZE, 1)

    cv2.namedWindow("AI Trainer", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("AI Trainer", DISPLAY_WIDTH, DISPLAY_HEIGHT)

    # 🔥 FIX: NO START DELAY
    threading.Thread(target=coach_llm.warmup, daemon=True).start()

    print("System Ready")

    intro_done = False
    rep_logged = 0
    set_data = []
    score = 0
    rep_flash = 0

    knee_path = []
    knee_smooth = []

    frame_count = 0  # 🔥 NEW
    prev_landmarks = None  # 🔥 NEW

    try:
        while True:

            ret, frame = camera.read()
            if not ret:
                break

            frame = cv2.flip(frame, 1)

            # 🔥 SPEED BOOST
            frame = cv2.resize(frame, (800, 600))

            # 🔥 FRAME SKIP
            # frame_count += 1
            # if frame_count % 2 != 0:
            #     continue

            landmarks = vision.process_frame(frame)

            # 🔥 SMOOTHING FIX
            if landmarks:
                if prev_landmarks:
                    alpha = 0.3
                    for i in range(len(landmarks)):
                        landmarks[i].x = alpha * prev_landmarks[i].x + (1 - alpha) * landmarks[i].x
                        landmarks[i].y = alpha * prev_landmarks[i].y + (1 - alpha) * landmarks[i].y

                prev_landmarks = landmarks

                exercise, confidence = exercise_detector.detect_exercise(landmarks)

                if confidence > 0.8 and not intro_done and biomech.rep_count > 0:
                    intro = exercise_coach.get_intro(exercise)
                    voice.speak(intro)
                    intro_done = True

                # 🔥 MULTI EXERCISE (UNCHANGED)
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

                feedback = realtime_coach.get_feedback(posture_state, errors, phase)

                if feedback and not voice.is_speaking():
                    voice.speak(feedback)

                # ---------------- REP LOGIC (UNCHANGED)
                if rep > rep_logged:
                    rep_logged = rep
                    rep_flash = 12
                    knee_path.clear()
                    knee_smooth.clear()

                    score = rep_quality.score_rep(posture_state, biomech_data, smoothness)

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

            frame_display = cv2.resize(frame, (DISPLAY_WIDTH, DISPLAY_HEIGHT))
            cv2.imshow("AI Trainer", frame_display)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    finally:
        # 🔥 CLEAN EXIT FIX
        camera.release()
        cv2.destroyAllWindows()
        cv2.waitKey(1)


if __name__ == "__main__":
    main()