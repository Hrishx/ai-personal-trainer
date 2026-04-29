import cv2
import mediapipe as mp
import time
from mediapipe.tasks import python
from mediapipe.tasks.python import vision


class VisionEngine:

    def __init__(self, model_path="pose_landmarker_full.task"):

        base_options = python.BaseOptions(model_asset_path=model_path)

        options = vision.PoseLandmarkerOptions(
            base_options=base_options,
            running_mode=vision.RunningMode.VIDEO,
            num_poses=1
        )

        self.landmarker = vision.PoseLandmarker.create_from_options(options)
        self.start_time = time.time()

    def process_frame(self, frame):

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        mp_image = mp.Image(
            image_format=mp.ImageFormat.SRGB,
            data=frame_rgb
        )

        # 🔥 FIX: use real-time timestamp
        timestamp_ms = int(time.time() * 1000)

        results = self.landmarker.detect_for_video(mp_image, timestamp_ms)

        if results.pose_landmarks:
            return results.pose_landmarks[0]

        return None