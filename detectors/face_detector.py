import cv2 as cv
import numpy as np
import dlib
import os
from utils import mid_point, distance, angle

if not os.path.exists("models/shape_predictor_68_face_landmarks.dat"):
    print("Downloading shape_predictor_68_face_landmarks.dat...")
    os.system("wget http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2")
    os.system("bzip2 -dk shape_predictor_68_face_landmarks.dat.bz2")
    os.system("mv shape_predictor_68_face_landmarks.dat models/")
    print("Done!")

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("models/shape_predictor_68_face_landmarks.dat")

def get_faces(image):

    faces = detector(image, 1)
    if len(faces) == 0: return (None, None)

    faces_rects = []

    for face in faces:
        top_left = (face.left(), face.top())
        bottom_right = (face.right(), face.bottom())
        faces_rects.append((top_left, bottom_right))

    return (faces_rects, faces)

def get_face_landmarks(image, face):
    landmarks = predictor(image, face)
    landmarks_points = [ (landmarks.part(i).x, landmarks.part(i).y) for i in range(0, 68) ]
    return landmarks_points

def detect_blink(eye_points):

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

def crop_eye(image, eye_points):
    x1, y1 = np.amin(eye_points, axis = 0)
    x2, y2 = np.amax(eye_points, axis = 0)
    return image[y1 : y2, x1 : x2], (x1, y1), (x2, y2)

def pupile_detector(image):

    # Remove brightness
    image = cv.equalizeHist(image)

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