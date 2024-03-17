import json
import os
import pickle

CALIBRATION_FILE = 'calibration.json'
REG_MODEL_FILE = 'models/gaze_mapper.pkl'
FACE_LANDMARKS_MODEL = 'models/shape_predictor_68_face_landmarks.dat'

def get_calibration():
    
    if not os.path.exists(CALIBRATION_FILE):
        with open(CALIBRATION_FILE, "w") as file:
            json.dump({}, file)
    
    with open(CALIBRATION_FILE, "r") as file:
        return json.load(file)
    
def save_calibration(calibration_data):
    with open(CALIBRATION_FILE, "w") as file:
        json.dump(calibration_data, file)

def download_face_landmarks_model():
    if not os.path.exists(FACE_LANDMARKS_MODEL):
        print("Downloading shape_predictor_68_face_landmarks.dat...")
        os.system("wget http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2")
        os.system("bzip2 -dk shape_predictor_68_face_landmarks.dat.bz2")
        os.system("mv shape_predictor_68_face_landmarks.dat models/")
        print("Done!")

def get_reg_model():
    if not os.path.exists(REG_MODEL_FILE):
        return None
    with open(REG_MODEL_FILE, "rb") as file:
        return pickle.load(file)
    
def save_reg_model(reg_model):
    with open(REG_MODEL_FILE, "wb") as file:
        pickle.dump(reg_model, file)