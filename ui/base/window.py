import tkinter as tk
import win32api
import win32con
import threading
from ui.base.location import LOCATION

class Window:

    def __init__(self, WIDTH = 200, HEIGHT = 200):

        self.WINDOW = tk.Tk()
        self.WINDOW.overrideredirect(True)

        self.HWND = self.WINDOW.winfo_id()
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        self.LOCATION = LOCATION.CENTER
        
        self.FRAME = tk.Frame(self.WINDOW, width=self.WIDTH, height=self.HEIGHT, bg='white')
        self.FRAME.pack_propagate(False)
        self.FRAME.pack(fill='both', expand=True)

    def set_location(self, side = LOCATION.CENTER):

        self.LOCATION = side
        screen_width, screen_height = win32api.GetSystemMetrics(win32con.SM_CXSCREEN), win32api.GetSystemMetrics(win32con.SM_CYSCREEN)

        if side == LOCATION.LEFT:
            x = 0
            y = (screen_height - self.HEIGHT) // 2
        elif side == LOCATION.RIGHT:
            x = screen_width - self.WIDTH
            y = (screen_height - self.HEIGHT) // 2
        elif side == LOCATION.CENTER:
            x = (screen_width - self.WIDTH) // 2
            y = (screen_height - self.HEIGHT) // 2
        elif side == LOCATION.TOP:
            x = (screen_width - self.WIDTH) // 2
            y = 0
        elif side == LOCATION.BOTTOM:
            x = (screen_width - self.WIDTH) // 2
            y = screen_height - self.HEIGHT

        self.WINDOW.geometry(f"{self.WIDTH}x{self.HEIGHT}+{x}+{y}")

    def locate(self, x, y):
        self.LOCATION = LOCATION.CUSTOM
        self.WINDOW.geometry(f"{self.WIDTH}x{self.HEIGHT}+{x}+{y}")

    def set_topmost(self, value = True):
        self.WINDOW.attributes('-topmost', value)

    def set_bounds(self, width, height):
        self.WIDTH = width
        self.HEIGHT = height
        self.WINDOW.geometry(f"{self.WIDTH}x{self.HEIGHT}")
        self.FRAME.config(width=self.WIDTH, height=self.HEIGHT)

    def set_title(self, title):
        self.WINDOW.title(title)

    def update(self):
        self.WINDOW.update_idletasks()

    def close(self):
        try: self.WINDOW.destroy()
        except: pass

    def hide(self):
        self.WINDOW.withdraw()

    def show(self):
        self.WINDOW.deiconify()

    def keep_alive(self):
        self.WINDOW.mainloop()