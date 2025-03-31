from flet import Page, app
from src.view.app import App


def main(page: Page) -> None:
    App(page)


if __name__ == "__main__":
    app(target=main, assets_dir='assets')
