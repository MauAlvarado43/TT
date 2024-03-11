import win32api
import win32con
import win32gui
import tkinter as tk
from ui.calibration import Calibration
from ui.base.window import Window
from ui.base.window import LOCATION

class Menu(Window):

    def __init__(self, APPLICATION):
        super().__init__(80, 720)
        self.APPLICATION = APPLICATION
        self.run()

    def run(self):
        
        self.set_topmost(True)

        # Botones del menú
        buttons_info = [
            ("Click izquierdo", './media/left_click.png', None),
            ("Click derecho", './media/right_click.png', None),
            ("Doble click", './media/double_click.png', None),
            ("Drag", './media/drag.png', None),
            ("Teclado", './media/keyboard.png', None),
            ("Recalibrar", './media/calibration.png', self.show_calibration_screen),
            ("Distribución", './media/layout.png', None),
            ("Mover menu", './media/move_main.png', self.move_menu),
            ("Salir", './media/exit.png', self.close)
        ]

        for text, icon_path, command in buttons_info:
            self.add_menu_button(self.FRAME, text, icon_path, command)

        self.set_location(LOCATION.RIGHT)
        self.update()
    
    def add_menu_button(self, frame, text, icon_path, action=None):
        """Agrega un botón al menú con el texto e icono especificados."""
        icon = tk.PhotoImage(file=icon_path)
        button = tk.Button(frame, text=text, image=icon, compound='top', borderwidth=0, highlightthickness=0, bg='white', command=action)
        button.image = icon
        button.pack(fill='x', pady=10, padx=0, anchor='e')

    def move_menu(self):
        """Mueve el menú al lado opuesto de la pantalla."""
        if self.LOCATION == LOCATION.RIGHT: self.set_location(LOCATION.LEFT)
        else: self.set_location(LOCATION.RIGHT)

    def show_calibration_screen(self):
        Calibration(self.APPLICATION).keep_alive()
    
    def close(self):
        exit()

    def handle_pupile_action(self, right_pupile, left_pupile):
        print(right_pupile, left_pupile)
        pass