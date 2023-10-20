import argparse
import cv2 as cv
import numpy as np
import time
from detectors.face_detector import get_faces, get_face_landmarks, detect_blink, crop_eye, pupile_detector

def process_image(image):

    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    face_rects, faces = get_faces(gray)

    if faces is not None:

        landmarks = get_face_landmarks(gray, faces[0])
        right_eye_points = landmarks[36:42]
        left_eye_points = landmarks[42:48]

        if draw_faces:
            for face in face_rects:
                cv.rectangle(image, face[0], face[1], (0, 255, 0), 2)

        if draw_landmarks:
            for landmark in landmarks:
                cv.circle(image, landmark, 1, (0, 0, 255), 2)

        right_blink_ratio = detect_blink(right_eye_points)
        left_blink_ratio = detect_blink(left_eye_points)

        print("Blink Ratio Right: ", right_blink_ratio)
        print("Blink Ratio Left: ", left_blink_ratio)

        right_eye_region, right_top_left, right_bottom_right = crop_eye(gray, right_eye_points)
        left_eye_region, left_top_left, left_bottom_right = crop_eye(gray, left_eye_points)

        if right_blink_ratio > 0.20:

            right_pupile = pupile_detector(right_eye_region)
            print("Right Pupile: ", right_pupile)

            if right_pupile is not None:
                
                rcx, rcy, rr = right_pupile
                rcx += right_top_left[0]
                rcy += right_top_left[1]

                if draw_pupile:
                    cv.circle(image, (rcx, rcy), rr, (0, 255, 0), 2)

        if left_blink_ratio > 0.20:

            left_pupile = pupile_detector(left_eye_region)
            print("Left Pupile: ", left_pupile)

            if left_pupile is not None:
                lcx, lcy, lr = left_pupile
                lcx += left_top_left[0]
                lcy += left_top_left[1]

                if draw_pupile:
                    cv.circle(image, (lcx, lcy), lr, (0, 255, 0), 2)

    cv.imshow("Image", image)
    cv.waitKey(0)

def video_execution():

    frame_counter = 0
    prev_time = 0
    next_time = 0
    fps = 0

    camera = cv.VideoCapture(0)
    camera_fps = camera.get(cv.CAP_PROP_FPS)
    camera_width = camera.get(cv.CAP_PROP_FRAME_WIDTH)
    camera_height = camera.get(cv.CAP_PROP_FRAME_HEIGHT)

    print("FPS: ", camera_fps)
    print("Width: ", camera_width)
    print("Height: ", camera_height)

    while True:

        frame_counter += 1
        ret, frame = camera.read()

        if not ret: break

        process_image(frame)

        next_time = time.time()
        fps = 1 / (next_time - prev_time)
        prev_time = next_time

        cv.putText(frame, "FPS: " + str(round(fps, 2)), (10, 30), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv.imshow("Camera", frame)

    camera.release()
    cv.destroyAllWindows()

def image_execution(image_path):
    image = cv.imread(image_path)
    process_image(image)
    
if __name__ == "__main__":
    
    args = argparse.ArgumentParser()
    args.add_argument("--draw-faces", action = "store_true", default=False)
    args.add_argument("--draw-landmarks", action = "store_true", default=False)
    args.add_argument("--draw-pupile", action = "store_true", default=False)
    args.add_argument("--video", action="store_true", default=False)
    args.add_argument("--image-path", type=str, default=None)

    args = args.parse_args()

    draw_faces = args.draw_faces
    draw_landmarks = args.draw_landmarks
    draw_pupile = args.draw_pupile
    video = args.video
    image_path = args.image_path

    if video: video_execution()
    if image_path is not None: image_execution(image_path)