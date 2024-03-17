import cv2 as cv
import numpy as np
import dlib
import os
import time
import threading
from datetime import datetime
from util.settings import get_calibration, save_calibration, FACE_LANDMARKS_MODEL, download_face_landmarks_model
from util.math import mid_point, distance

if not os.path.exists(FACE_LANDMARKS_MODEL):
    download_face_landmarks_model()

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(FACE_LANDMARKS_MODEL)

class PupileDetector:

    frame = None

    def __init__(self, blink_callback = None, fixation_callback = None):
        self.blink_callback = blink_callback
        self.fixation_callback = fixation_callback
        self.capture_frames()

    def capture_frames(self):

        def capture_frames_thread():
      
            cap = cv.VideoCapture(0)
            
            while True:
                _, frame = cap.read()
                self.frame = frame
                if cv.waitKey(1) == ord('q'): break

        threading.Thread(target=capture_frames_thread, daemon=True).start()

    def get_faces(self):
        
        self.process_frame = self.frame.copy()
        self.process_frame_gray = cv.cvtColor(self.process_frame, cv.COLOR_BGR2GRAY)
        faces = detector(self.process_frame_gray, 1)
        if len(faces) == 0: return (None, None)

        faces_rects = []

        for face in faces:
            top_left = (face.left(), face.top())
            bottom_right = (face.right(), face.bottom())
            faces_rects.append((top_left, bottom_right))

        return (faces_rects, faces)
    
    def get_face_landmarks(self, face):
        landmarks = predictor(self.process_frame_gray, face)
        landmarks_points = [ (landmarks.part(i).x, landmarks.part(i).y) for i in range(0, 68) ]
        return landmarks_points
    
    def detect_blink(self, eye_points):

        A = distance(eye_points[1], eye_points[5])
        B = distance(eye_points[2], eye_points[4])
        C = distance(eye_points[0], eye_points[3])

        # Eye aspect ratio
        ear = (A + B) / (2.0 * C)
        return ear

        top = eye_points[1 : 3]
        bottom = eye_points[4 : 6]

        top_mid = mid_point(top[0], top[1])
        bottom_mid = mid_point(bottom[0], bottom[1])

        vertical_distance = distance(top_mid, bottom_mid)
        horizontal_distance = distance(eye_points[0], eye_points[3])

        blink_ratio = horizontal_distance / vertical_distance

        return blink_ratio
    
    def crop_eye(self, eye_points):
        x1, y1 = np.amin(eye_points, axis = 0)
        x2, y2 = np.amax(eye_points, axis = 0)
        return self.process_frame_gray[y1 : y2, x1 : x2], (x1, y1), (x2, y2)

    def get_pupile(self, region_image):

        # Remove brightness
        image = cv.equalizeHist(region_image)

        _, threshold = cv.threshold(image, 70, 255, cv.THRESH_BINARY)
        threshold = cv.erode(threshold, None, iterations = 2)
        threshold = cv.dilate(threshold, None, iterations = 4)
        threshold = cv.medianBlur(threshold, 3)
        threshold = cv.bitwise_not(threshold)

        # Find contours
        contours, _ = cv.findContours(threshold, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

        # Find the biggest contour
        if len(contours) == 0: return None

        contour = max(contours, key = cv.contourArea)

        # Bounding box
        x, y, w, h = cv.boundingRect(contour)

        # Center
        cx = x + w // 2
        cy = y + h // 2

        # Approximate radius
        radius = (w + h) // 4

        if radius < 1.5: return None
        return (cx, cy, radius)

    def process_pupile(self):

        blink_dates = []

        while True:

            calibration_data = get_calibration()
            if self.frame is None: continue

            _, faces = self.get_faces()

            if faces is not None:

                landmarks = self.get_face_landmarks(faces[0])
                right_eye_points = landmarks[36:42]
                left_eye_points = landmarks[42:48]

                right_blink_ratio = self.detect_blink(right_eye_points)
                left_blink_ratio = self.detect_blink(left_eye_points)

                if "rbr_max" in calibration_data: calibration_data["rbr_max"] = max(calibration_data["rbr_max"], right_blink_ratio)
                else: calibration_data["rbr_max"] = right_blink_ratio

                if "rbr_min" in calibration_data: calibration_data["rbr_min"] = min(calibration_data["rbr_min"], right_blink_ratio)
                else: calibration_data["rbr_min"] = right_blink_ratio

                if "lbr_max" in calibration_data: calibration_data["lbr_max"] = max(calibration_data["lbr_max"], left_blink_ratio)
                else: calibration_data["lbr_max"] = left_blink_ratio

                if "lbr_min" in calibration_data: calibration_data["lbr_min"] = min(calibration_data["lbr_min"], left_blink_ratio)
                else: calibration_data["lbr_min"] = left_blink_ratio

                save_calibration(calibration_data)

                right_blink_ratio = (right_blink_ratio - calibration_data["rbr_min"]) / (calibration_data["rbr_max"] - calibration_data["rbr_min"])
                left_blink_ratio = (left_blink_ratio - calibration_data["lbr_min"]) / (calibration_data["lbr_max"] - calibration_data["lbr_min"])

                right_pupile = None
                if right_blink_ratio > 0.20:
                    right_eye_region, right_top_left, right_bottom_right = self.crop_eye(right_eye_points)
                    right_pupile = self.get_pupile(right_eye_region)

                left_pupile = None
                if left_blink_ratio > 0.20:
                    left_eye_region, left_top_left, left_bottom_right = self.crop_eye(left_eye_points)
                    left_pupile = self.get_pupile(left_eye_region)

                if right_pupile is None and left_pupile is None:
                    blink_dates.append(datetime.now())
                    if len(blink_dates) > 2: blink_dates.pop(0)

                if right_pupile is not None and left_pupile is not None:

                    rcx, rcy, rr = right_pupile
                    lcx, lcy, lr = left_pupile

                    rcx += right_top_left[0]
                    rcy += right_top_left[1]

                    lcx += left_top_left[0]
                    lcy += left_top_left[1]

                    rc = [int(rcx), int(rcy)]
                    lc = [int(lcx), int(lcy)]

                    # Fixation
                    self.fixation_callback(rc, lc)
                    
                    # blink
                    if len(blink_dates) == 2 and (blink_dates[1] - blink_dates[0]).total_seconds() > 1.5:
                        self.blink_callback(rc, lc)
                        blink_dates = []

            else:
                
                blink_dates = []

            time.sleep(0.05)