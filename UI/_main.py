import tkinter as tk
from tkinter import font
import win32gui
import win32con
import win32api

root = tk.Tk()
root.overrideredirect(True)

INSTRUCTION_FONT = font.Font(root=root, size=20, weight='bold')
NUMBER_FONT = font.Font(root=root, size=18, weight='bold')
MENU_WIDTH = 80
MENU_HEIGHT = 640
CURRENT_SIDE = 'right'

def close_calibration(window):
    window.destroy()  
    root.deiconify()  
    menu_frame.pack(fill='both', expand=True)
    
# Función para configurar y mover la ventana
def configure_window(hwnd, width, height, side='right'):
    """Main window configuration"""
    ex_style = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
    win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, ex_style | win32con.WS_EX_LAYERED | win32con.WS_EX_TOOLWINDOW)
    win32gui.SetLayeredWindowAttributes(hwnd, win32con.NULL, 255, win32con.LWA_ALPHA)

    screen_width, screen_height = win32api.GetSystemMetrics(win32con.SM_CXSCREEN), win32api.GetSystemMetrics(win32con.SM_CYSCREEN)
    x = screen_width - width if side == 'right' else 0
    y = (screen_height - height) // 2
    win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, x, y, width, height, 0)

def move_menu():
    """Mueve el menú al lado opuesto de la pantalla."""
    global CURRENT_SIDE  # Usa la variable global
    CURRENT_SIDE = 'left' if CURRENT_SIDE == 'right' else 'right'
    hwnd = win32gui.FindWindow(None, root.title())
    configure_window(hwnd, MENU_WIDTH, MENU_HEIGHT, CURRENT_SIDE)


def show_calibration_screen():
    menu_frame.pack_forget()  
    root.withdraw()
    
    screen_width, screen_height = win32api.GetSystemMetrics(win32con.SM_CXSCREEN), win32api.GetSystemMetrics(win32con.SM_CYSCREEN)
    cal_width, cal_height = screen_width - 200, screen_height - 200
    calibration_window = tk.Toplevel(root)
    calibration_window.overrideredirect(True)
    calibration_window.attributes('-topmost', True)
    calibration_window.geometry(f"{cal_width}x{cal_height}+{(screen_width - cal_width) // 2}+{(screen_height - cal_height) // 2}")

    close_button = tk.Button(calibration_window, text="X", command=lambda: close_calibration(calibration_window), bg='white')
    close_button.pack(anchor='ne', padx=5, pady=5)
    
    instruction_label = tk.Label(calibration_window, text="Oberva cada uno de los recuadros y parpadea.", bg='white', font=INSTRUCTION_FONT)
    instruction_label.pack(side='top', pady=10)
    
    main_frame = tk.Frame(calibration_window, bg='white')
    main_frame.pack(expand=True, fill='both')

    for i in range(9):
        label = tk.Label(main_frame, text=str(i + 1), borderwidth=2, relief="solid", bg='black', fg='white', font=NUMBER_FONT, highlightbackground='gray', highlightthickness=4) # Aumentado el grosor del borde
        label.grid(row=i // 3, column=i % 3, padx=15, pady=15, sticky='nsew')
        main_frame.grid_columnconfigure(i % 3, weight=1)
        main_frame.grid_rowconfigure(i // 3, weight=1)


def add_menu_button(frame, text, icon_path, action=None):
    """Agrega un botón al menú con el texto e icono especificados."""
    icon = tk.PhotoImage(file=icon_path)
    button = tk.Button(frame, text=text, image=icon, compound='top', borderwidth=0, highlightthickness=0, bg='white', command=action)
    button.image = icon
    button.pack(fill='x', pady=10, padx=0, anchor='e')

# Creación de la interfaz de usuario del menú
menu_frame = tk.Frame(root, width=MENU_WIDTH, height=MENU_HEIGHT, bg='white')
menu_frame.pack_propagate(False)
menu_frame.pack(fill='both', expand=True)

# Botones del menú
buttons_info = [
    ("Click izquierdo", './media/left_click.png', None),
    ("Click derecho", './media/right_click.png', None),
    ("Doble click", './media/double_click.png', None),
    ("Drag", './media/drag.png', None),
    ("Teclado", './media/keyboard.png', None),
    ("Recalibrar", './media/calibration.png', show_calibration_screen),
    ("Distribución", './media/layout.png', None),
    ("Mover menu", './media/move_main.png', move_menu),
]

for text, icon_path, command in buttons_info:
    add_menu_button(menu_frame, text, icon_path, command)

root.update_idletasks()
hwnd = win32gui.FindWindow(None, root.title())
configure_window(hwnd, MENU_WIDTH, MENU_HEIGHT, CURRENT_SIDE)
root.mainloop()
