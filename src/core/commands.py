from pyautogui import *


def smart_click(image_path: str):
    while True:
        try:
            click(image_path)
            break
        except ImageNotFoundException:
            None


def smart_press(image_path: str, key: str):
    while True:
        try:
            if locateOnScreen(image_path):
                press(key)
            break
        except ImageNotFoundException:
            None
