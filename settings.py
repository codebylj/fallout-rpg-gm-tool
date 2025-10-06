import flet as ft

LAN = "en"
GBCOLOR = "black"
DARK_COLOR = "#073605"
MAIN_COLOR = "#00ee00"
POP_UP_COLOR = "#223026"

FONTS = {
    "Chakra Petch": "https://github.com/cadsondemak/Chakra-Petch/raw/refs/heads/master/fonts/ChakraPetch-Regular.ttf"}

SIDE_SCREEN_WIDTH = 664
FORM_FIELD_WIDTH = 664
VAULT_WIDTH = 500
MENU_ITEM_WIDTH = 152
SIDE_LIST_WIDTH = 180
LOG_ENTRY_WIDTH = 896

TXT_STYLE = ft.TextStyle(
    color=MAIN_COLOR,
    font_family="Chakra Petch",
    size=16)

TXT_BTN_STYLE_TXT = ft.TextStyle(
    weight=ft.FontWeight.W_900,
    color=MAIN_COLOR,
    font_family="Chakra Petch",
    size=16)

TXT_BTN_STYLE = ft.ButtonStyle(
    padding=ft.padding.symmetric(horizontal=5),
    overlay_color="transparent",
    shape=ft.RoundedRectangleBorder(radius=0),
    text_style=TXT_STYLE,
    color=MAIN_COLOR)

TXT_BTN_STYLE_HOVER = ft.ButtonStyle(
    padding=ft.padding.symmetric(horizontal=5),
    overlay_color=MAIN_COLOR,
    bgcolor=MAIN_COLOR,
    shape=ft.RoundedRectangleBorder(radius=0),
    text_style=TXT_BTN_STYLE_TXT,
    color="black")

ENTRY_TXT_STYLE = ft.TextStyle(
    color=MAIN_COLOR,
    font_family="Chakra Petch",
    size=18)

BTN_STYLE = ft.ButtonStyle(
    side=ft.BorderSide(
        color=MAIN_COLOR,
        width=1
    ),
    text_style=TXT_STYLE,
    color=MAIN_COLOR,
    shape=ft.RoundedRectangleBorder(radius=0)
)

BTN_STYLE_HOVER = ft.ButtonStyle(
    bgcolor=MAIN_COLOR,
    side=ft.BorderSide(
        color=MAIN_COLOR,
        width=1
    ),
    text_style=TXT_STYLE,
    color="black",
    shape=ft.RoundedRectangleBorder(radius=0)
)

ERROR_STYLE = ft.TextStyle(
    color=MAIN_COLOR,
    decoration_color=MAIN_COLOR,
)

BORDER = ft.border.all(2, MAIN_COLOR)
