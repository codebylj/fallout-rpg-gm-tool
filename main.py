import flet as ft

import screens as scr
import settings as sett



def main(page: ft.Page):
    page.title = "Fallout Terminal"
    page.window.height = 1080
    page.window.width = 1920
    page.padding = 36
    # page.window.frameless = True
    page.window.resizable = False
    page.window.maximized = True
    # page.window.full_screen = True
    page.bgcolor = sett.GBCOLOR
    page.fonts = sett.FONTS
    page.theme = ft.Theme(
        font_family="Chakra Petch",
        text_theme=ft.TextTheme(
            body_medium=ft.TextStyle(
                color=sett.FONT_COLOR,
                font_family="Chakra Petch",
                size=16)
        )

    )

    bg_image = ft.Image(
        src="./resources/images/Background v3.jpg",

    )

    screen = ft.Container(
        padding=0,
        content=ft.Stack(
            [
                bg_image,
                scr.interface
            ]
        )
    )

    page.add(screen)


ft.app(main)
