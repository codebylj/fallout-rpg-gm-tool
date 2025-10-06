import flet as ft
from sqlalchemy import create_engine

import screens as scr
import settings as sett
from models import *

engine = create_engine("sqlite:///resources/database/vault.db")
Base.metadata.create_all(engine)


def main(page: ft.Page):
    page.title = "Fallout Terminal"
    page.window.height = 1080
    page.window.width = 1920
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.window.frameless = True
    page.window.resizable = False
    page.window.maximized = True
    page.window.full_screen = True
    page.bgcolor = sett.GBCOLOR
    page.fonts = sett.FONTS
    page.theme = ft.Theme(
        font_family="Chakra Petch",
        text_theme=ft.TextTheme(
            body_medium=ft.TextStyle(
                color=sett.MAIN_COLOR,
                font_family="Chakra Petch",
                size=16)
        ),
        color_scheme=ft.ColorScheme(
            error=sett.MAIN_COLOR,
        )
    )

    bg_image = ft.Image(
        src="./resources/images/Background_1200.jpg",
        fit=ft.ImageFit.SCALE_DOWN

    )

    screen = ft.Container(
        padding=0,
        content=ft.Stack(
            [
                bg_image,
                ft.Container(
                    padding=36,
                    content=scr.interface
                )
            ]
        )
    )
    page.add(screen)


ft.app(main)
