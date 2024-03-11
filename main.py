import tkinter as tk
from tkinter import font
import threading
from detectors.face_detector import PupileDetector
from ui.menu import Menu
from ui.calibration import Calibration

# Función para configurar y mover la ventana

# def show_calibration_screen():

#     global ACTION_THREAD
#     ACTION_THREAD.terminate()

#     close_button = tk.Button(calibration_window, text="X", command=lambda: close_calibration(calibration_window), bg='white')
#     close_button.pack(anchor='ne', padx=5, pady=5)
    
#     instruction_label = tk.Label(calibration_window, text="Oberva cada uno de los recuadros y parpadea.", bg='white', font=INSTRUCTION_FONT)
#     instruction_label.pack(side='top', pady=10)
    
#     cal_frame = tk.Frame(calibration_window, bg='white')
#     cal_frame.pack(expand=True, fill='both')

#     for i in range(9):

#         x = (i % 3) * (cal_width // 3)
#         y = (i // 3) * (cal_height // 3)

#         cx = x + cal_width // 6
#         cy = y + cal_height // 6

#         padding = 15
#         label = tk.Label(cal_frame, text=str(i + 1), borderwidth=2, relief="solid", bg='black', fg='white', font=NUMBER_FONT, highlightbackground='gray', highlightthickness=4)
#         label.place(x=x + padding, y=y + padding, width=cal_width // 3 - padding * 2, height=cal_height // 3 - padding * 2)

#         right_pupile, left_pupile = next(pupile_detector.get_pupile_action())

#         print(cx, cy, "vs", right_pupile, left_pupile)

#         cal_frame.update_idletasks()


class BlinkAssistant:

    def __init__(self):
        self.pupile_detector = PupileDetector()
        self.pupile_callback = None

    def run(self):
        self.listen_pupile_action()
        Menu(self).keep_alive()

    def set_action_callback(self, callback):
        self.pupile_callback = callback

    def listen_pupile_action(self):
        
        def handle_callback():
            while True:
                right_pupile, left_pupile = next(self.pupile_detector.get_pupile_action())
                if self.pupile_callback is not None:
                    self.pupile_callback(right_pupile, left_pupile)

        threading.Thread(target=handle_callback, daemon=True).start()

if __name__ == "__main__":
    BlinkAssistant().run()