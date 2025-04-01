from pyautogui import *


def smart_click(image_path: str, flag_path: str = None):
    while True:
        try:
            if flag_path:
                if locateOnScreen(flag_path):
                    click(image_path)
                    break
            else:
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
