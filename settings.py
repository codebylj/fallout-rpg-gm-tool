import flet as ft

GBCOLOR = "black"
FONTS = {
    "Chakra Petch": "https://github.com/cadsondemak/Chakra-Petch/raw/refs/heads/master/fonts/ChakraPetch-Regular.ttf"}

FONT_COLOR = "#00ee00"

TXT_STYLE = ft.TextStyle(
    color=FONT_COLOR,
    font_family="Chakra Petch",
    size=16)

TXT_BTN_STYLE = ft.ButtonStyle(
    overlay_color="transparent",
    padding=0,
    text_style=TXT_STYLE,
    color=FONT_COLOR)

BTN_STYLE = ft.ButtonStyle(
    overlay_color="transparent",
    side=ft.BorderSide(
        color=FONT_COLOR,
        width=1
    ),
    text_style=TXT_STYLE,
    color=FONT_COLOR,

    shape=ft.RoundedRectangleBorder(radius=0)
)
