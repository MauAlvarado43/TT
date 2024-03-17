import pyautogui as pg

def click(x, y):
    pg.click(x, y)

def right_click(x, y):
    pg.rightClick(x, y)

def double_click(x, y):
    pg.doubleClick(x, y)

def move(x, y):
    pg.moveTo(x, y)

def toggle_drag(x, y, state):
    if state == "down":
        pg.mouseDown(x, y)
    elif state == "up":
        pg.mouseUp(x, y)