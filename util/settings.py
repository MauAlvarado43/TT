import json
import os

CALIBRATION_FILE = 'calibration.json'

def get_calibration():
    
    if not os.path.exists(CALIBRATION_FILE):
        with open(CALIBRATION_FILE, "w") as file:
            json.dump({}, file)
    
    with open(CALIBRATION_FILE, "r") as file:
        return json.load(file)
    
def save_calibration(calibration_data):
    with open(CALIBRATION_FILE, "w") as file:
        json.dump(calibration_data, file)