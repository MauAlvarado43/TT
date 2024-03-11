import win32api
import win32con
import win32gui
import tkinter as tk
from tkinter import font
from ui.base.window import Window
from ui.base.window import LOCATION

class Calibration(Window):
  
    def __init__(self, APPLICATION):
        super().__init__(400, 400)
        self.APPLICATION = APPLICATION
        self.INSTRUCTION_FONT = font.Font(root=self.WINDOW, size=20, weight='bold')
        self.NUMBER_FONT = font.Font(root=self.WINDOW, size=18, weight='bold')

        self.calibration_frame = None
        self.label = None

        self.calibration_data = {
            "step": 0,
            "total_steps": 9,
            "label_points": [],
            "pupile_points": []
        }

        self.run()

    def run(self):
        
        screen_width, screen_height = win32api.GetSystemMetrics(win32con.SM_CXSCREEN), win32api.GetSystemMetrics(win32con.SM_CYSCREEN)

        self.set_topmost(True)
        self.set_bounds(screen_width - 200, screen_height - 200)
        self.set_location(LOCATION.CENTER)

        close_button = tk.Button(self.FRAME, text="X", command=self.close, bg='white')
        close_button.pack(anchor='ne', padx=5, pady=5)

        instruction_label = tk.Label(self.FRAME, text="Oberva cada uno de los recuadros y parpadea.", bg='white', font=self.INSTRUCTION_FONT)
        instruction_label.pack(side='top', pady=10)

        self.calibrate()

    def show_calibration_step(self, step):
        
        if self.label is not None:
            self.label.destroy()

        if self.calibration_frame is None:
            self.calibration_frame = tk.Frame(self.FRAME, bg='white')
            self.calibration_frame.pack(expand=True, fill='both')

        panel_width = self.calibration_frame.winfo_width()
        panel_height = self.calibration_frame.winfo_height()

        x = (step % 3) * (panel_width // 3)
        y = (step // 3) * (panel_height // 3)

        cx = x + panel_width // 6
        cy = y + panel_height // 6

        self.calibration_data["label_points"].append((cx, cy))

        padding = 15
        self.label = tk.Label(self.calibration_frame, text=str(step + 1), borderwidth=2, relief="solid", bg='black', fg='white', font=self.NUMBER_FONT, highlightbackground='gray', highlightthickness=4)
        self.label.place(x=x + padding, y=y + padding, width=panel_width // 3 - padding * 2, height=panel_height // 3 - padding * 2)

    def calibrate(self):
        self.show_calibration_step(self.calibration_data["step"])
        self.APPLICATION.set_action_callback(self.handle_pupile_action)

    def handle_pupile_action(self, right_pupile, left_pupile):
        
        if self.calibration_data["step"] < self.calibration_data["total_steps"]:
            self.calibration_data["pupile_points"].append((right_pupile, left_pupile))
            self.calibration_data["step"] += 1
            self.show_calibration_step(self.calibration_data["step"])
        else:
            print(self.calibration_data)
            # self.save_calibration()
            self.close()