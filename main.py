import cv2 as cv
import numpy as np
import time
from face_detector import get_faces, get_face_landmarks, detect_blink, crop_eye, pupile_detector

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

draw_faces = True
draw_landmarks = True

while True:

    frame_counter += 1
    
    ret, frame = camera.read()

    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    face_rects, faces = get_faces(gray)

    if faces is not None:

        landmarks = get_face_landmarks(gray, faces[0])

        if draw_faces:
            for face in face_rects:
                cv.rectangle(frame, face[0], face[1], (0, 255, 0), 2)

        if draw_landmarks:
            for landmark in landmarks:
                cv.circle(frame, landmark, 1, (0, 0, 255), 2)

        right_eye_points = landmarks[36:42]
        left_eye_points = landmarks[42:48]

        right_blink_ratio = detect_blink(right_eye_points)
        left_blink_ratio = detect_blink(left_eye_points)

        right_eye_region = crop_eye(gray, right_eye_points)
        left_eye_region = crop_eye(gray, left_eye_points)

        cv.imshow("Threshold", pupile_detector(right_eye_region))

        # try:

        #     contours = cv.findContours(right_eye_region, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)[0]
        #     contours = sorted(contours, key = lambda x: cv.contourArea(x), reverse = True)

        #     for contour in contours:
        #         (x, y, w, h) = cv.boundingRect(contour)
        #         cv.rectangle(right_eye_region, (x, y), (x + w, y + h), (255, 0, 0), 2)
        #         cv.line(right_eye_region, (x, y), (x + w, y + h), (255, 0, 0), 2)
        #         cv.line(right_eye_region, (x + w, y), (x, y + h), (255, 0, 0), 2)
        #         break

        #     cv.imshow("Right Eye", right_eye_region)
        #     if cv.waitKey(1) == ord('q'):
        #         break

        # except:
        #     pass

        # cv.putText(frame, "Right: " + str(round(right_blink_ratio, 2)), (10, 60), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        # cv.putText(frame, "Left: " + str(round(left_blink_ratio, 2)), (10, 90), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    if cv.waitKey(1) == ord('q'):
        break

    # next_time = time.time()
    # fps = 1 / (next_time - prev_time)
    # prev_time = next_time

    # cv.putText(frame, "FPS: " + str(round(fps, 2)), (10, 30), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    # cv.imshow("Camera", frame)

camera.release()
cv.destroyAllWindows()