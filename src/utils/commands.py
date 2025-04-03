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
            print('Botão não foi encontrado!')
        sleep(0.5)


def smart_click_position(x: int, y: int, flag_path: str):
    while True:
        try:
            if locateOnScreen(flag_path):
                click(x=x, y=y)
                break

        except ImageNotFoundException:
            print('Referência não foi encontrada!')
        sleep(0.5)


def smart_press(image_path: str, key: str):
    while True:
        try:
            if locateOnScreen(image_path):
                press(key)
            break
        except ImageNotFoundException:
            print('Referência não foi encontrada!')
        sleep(0.5)
