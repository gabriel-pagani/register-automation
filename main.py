from flet import Page, app
from src.view.app import App
from src.utils.connection import close_connection


def main(page: Page) -> None:
    App(page)


if __name__ == "__main__":
    try:
        app(target=main, assets_dir='assets')
    finally:
        close_connection()
