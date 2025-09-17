"""Define screens for the application and UI behaviour"""
import datetime

import flet as ft
from flet.core.date_picker import DatePicker
from sqlalchemy import create_engine, select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

import settings as sett
from labels import labels
from models import Vault, LogEntry

active_user = ""

double_divider = ft.Text(
    value="==============================================="
)

single_short_divider = ft.Text(
    value="----------"
)

security_level_options = [
    ft.DropdownOption(key="1", text="1", style=sett.TXT_STYLE),
    ft.DropdownOption(key="2", text="2", style=sett.TXT_STYLE),
    ft.DropdownOption(key="3", text="3", style=sett.TXT_STYLE),
    ft.DropdownOption(key="4", text="4", style=sett.TXT_STYLE),
    ft.DropdownOption(key="5", text="5", style=sett.TXT_STYLE),
]

vault_status_options = [
    ft.DropdownOption(key="active", text=labels[sett.LAN]["active"],
                      style=sett.TXT_STYLE),
    ft.DropdownOption(key="inactive", text=labels[sett.LAN]["inactive"],
                      style=sett.TXT_STYLE),
]

vault_door_options = [
    ft.DropdownOption(key="open", text=labels[sett.LAN]["open"],
                      style=sett.TXT_STYLE),
    ft.DropdownOption(key="closed", text=labels[sett.LAN]["closed"],
                      style=sett.TXT_STYLE),
]


def on_hover_btn(e: ft.HoverEvent):
    """On hover of text button"""
    if e.data == "true":
        e.control.style = sett.TXT_BTN_STYLE_HOVER
    else:
        e.control.style = sett.TXT_BTN_STYLE
    e.control.update()


def on_hover_box_btn(e: ft.HoverEvent):
    """On hover of box buttons"""
    if e.data == "true":
        e.control.style = sett.BTN_STYLE_HOVER
    else:
        e.control.style = sett.BTN_STYLE
    e.control.update()


def on_hover_box(e: ft.HoverEvent):
    """On hover of box menu item like Valut or Entry """
    if e.data == "true":
        e.control.bgcolor = sett.FONT_COLOR
        e.control.content.controls[0].color = "black"
        e.control.content.controls[1].color = "black"
    else:
        e.control.bgcolor = "transparent"
        e.control.content.controls[0].color = sett.FONT_COLOR
        e.control.content.controls[1].color = sett.FONT_COLOR
    e.control.update()
    e.control.content.controls[0].update()
    e.control.content.controls[1].update()


def validation_num(e):
    e.control.error_text = ""
    e.control.update()
    value = e.control.value
    if value.isdigit():
        pass
    else:
        e.control.error_text = labels[sett.LAN]["num_value_error"]
        e.control.update()


def validation_empty_field(field, validator):
    if field.value == "":
        field.error_text = labels[sett.LAN]["not_empty"]
        field.update()
        validator.append(field)
    return validator


def logout(e):
    global active_user
    active_user = ""
    interface.controls[1] = LogInPage()
    interface.update()
    login_screen.password.value = ""
    login_screen.username.value = ""


class ControlButton(ft.TextButton):
    """Dfinition of a control button."""

    def __init__(self, text, on_click):
        super().__init__(
            text=f"[{labels[sett.LAN][text]}]",
            style=sett.TXT_BTN_STYLE,
            on_hover=on_hover_btn,
            on_click=on_click)


class ErrorMessage(ft.SnackBar):
    """Dfinition of a error message display."""

    def __init__(self, text):
        super().__init__(
            open=True,
            bgcolor=sett.FONT_COLOR,
            content=ft.Text(
                value=labels[sett.LAN][text],
                color=sett.DARK_COLOR,
                weight=ft.FontWeight.W_900)
        )


def error_message(text, page):
    """Displays an error message."""
    error_msg = ErrorMessage(text=text)
    page.open(error_msg)
    page.update()


class DeleteDialog(ft.AlertDialog):
    """Dfinition of a delete dialog."""

    def __init__(self, label, text, on_click):
        super().__init__(
            modal=True,
            bgcolor=sett.POP_UP_COLOR,
            shape=ft.RoundedRectangleBorder(radius=0),

            title=ft.Text(labels[sett.LAN][label],
                          color=sett.FONT_COLOR),
            content=ft.Text(labels[sett.LAN][text]),
            actions=[
                ControlButton(text="yes", on_click=on_click),
                ControlButton(text="cancel",
                              on_click=lambda e: e.page.close(self))
            ]
        )


class InputField(ft.TextField):
    """Definition of an input field."""

    def __init__(self, width=286, height=56, **kwargs):
        super().__init__(
            width=width,
            bgcolor=sett.DARK_COLOR,
            border_color="transparent",
            color=sett.FONT_COLOR,
            height=height,
            border_radius=0,
            error_style=sett.ERROR_STYLE,
            **kwargs
        )


class DropdownList(ft.Dropdown):
    """Definition of a dropdown list."""

    def __init__(self, width=286, **kwargs):
        super().__init__(
            width=width,
            select_icon=ft.Icons.KEYBOARD_ARROW_DOWN,
            selected_trailing_icon=ft.Icons.KEYBOARD_ARROW_UP,
            bgcolor="#073605",
            border_color=sett.DARK_COLOR,
            border_radius=0,
            color=sett.FONT_COLOR,
            filled=True,
            fill_color=sett.DARK_COLOR,
            hint_text=labels[sett.LAN]["select"],
            hint_style=sett.TXT_STYLE,
            **kwargs
        )


class MenuItemText(ft.Text):
    """Definition of a menu item text."""

    def __init__(self, text, **kwargs):
        super().__init__(
            width=142,
            text_align=ft.TextAlign.CENTER,
            value=text,
            style=sett.TXT_STYLE,
            weight=ft.FontWeight.BOLD,
            **kwargs
        )


class Header(ft.Container):
    """Header of the application."""

    def __init__(self):
        print("Header")
        try:
            with Session(engine) as header_session:
                active_vault = header_session.scalar(
                    select(Vault).where(Vault.status == "active"))
                if active_vault:
                    vault_number = f"Server {active_vault.vault_number}"
                else:
                    vault_number = labels[sett.LAN]["no_active_vault_short"]
        except Exception:
            vault_number = labels[sett.LAN]["no_active_vault_short"]

        header_text = ft.Text(
            color=sett.FONT_COLOR,
            text_align=ft.TextAlign.CENTER,
            size=18,
            weight=ft.FontWeight.BOLD,
            value=f"ROBCO INDUSTRIES UNIFIED OPERATING SYSTEM\nCOPYRIGHT 2075-2077 ROBCO INDUSTRIES\n- {vault_number} -"
        )

        super().__init__()
        self.width = 1850
        self.height = 193
        self.alignment = ft.alignment.center
        self.content = header_text


class LogInPage(ft.Container):
    """Login page definition."""

    def __init__(self):
        self.username = InputField()
        self.password = InputField(password=True)

        logo = ft.Image(
            width=434,
            height=143,
            src="./resources/images/Logo.png"
        )

        enter_btn = ft.OutlinedButton(
            text=labels[sett.LAN]["enter"],
            width=208,
            height=54,
            style=sett.BTN_STYLE,
            on_hover=on_hover_box_btn,
            on_click=self.verification
        )

        super().__init__()
        """Login screen layout"""
        self.width = 1850
        self.height = 586
        self.content = (
            ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,
                controls=[
                    ft.Container(
                        bgcolor=ft.Colors.with_opacity(0.3, "#223026"),
                        border_radius=50,
                        width=538,
                        height=586,
                        padding=52,
                        content=(
                            ft.Column(
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                spacing=42,
                                controls=[
                                    logo,
                                    ft.Container(height=2),
                                    ft.Row(
                                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                        expand=True,
                                        controls=[
                                            ft.Text(
                                                value=labels[sett.LAN]["login"]
                                            ),
                                            self.username,
                                        ]
                                    ),
                                    ft.Row(
                                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                        expand=True,
                                        controls=[
                                            ft.Text(
                                                value=labels[sett.LAN][
                                                    "password"]
                                            ),
                                            self.password,
                                        ]
                                    ),
                                    enter_btn
                                ]
                            )
                        )
                    )
                ]
            )
        )

    # class functionality
    def clear_credentials(self):
        """Clears credentials from the text fields."""
        self.username.value = ""
        self.password.value = ""
        self.username.update()
        self.password.update()

    def unauthorized(self, text):
        """Plays error sound when credentials are invalid."""
        audio = ft.Audio(
            src="./resources/sounds/error-126627.mp3",
            autoplay=True,
            volume=1.0
        )
        self.page.overlay.append(audio)
        self.page.update()
        page = self.page
        error_message(text=text, page=page)
        audio.play()
        self.clear_credentials()

    def verification(self, e):
        """
        Verifies credentials and redirects to the menu screen or Game Master menu screen.
        Saves game master session.
        """
        global active_user

        with Session(engine) as login_session:
            active_vault_data = select(Vault).where(
                Vault.status == "active")
            active_vault = login_session.scalar(active_vault_data)

        if self.username.value == "EXIT":
            e.page.window.destroy()
        elif self.username.value.lower() == "game master" and self.password.value.lower() == "fallout":
            active_user = "game master"
            self.clear_credentials()
            interface.controls[1] = GameMasterMenu()
            interface.update()
        elif self.username.value.lower() == "game master" and self.password.value.lower() != "fallout":
            self.unauthorized("gm_error")
        elif active_vault:
            if self.username.value.lower() == 'haker' and self.password.value:
                result = self.password.value
                result_int = int(result)
                difficulty = active_vault.security_level
                if result_int >= difficulty:
                    self.clear_credentials()
                    interface.controls[1] = MenuScreen()
                    interface.update()
                elif not result:
                    self.unauthorized("unauthorized_access")
                else:
                    self.unauthorized("unauthorized_access")
            elif self.username.value.lower() == labels[sett.LAN][
                "overseer"].lower():
                result = self.password.value
                vault_password = active_vault.overseer_password
                if result == vault_password:
                    self.clear_credentials()
                    interface.controls[1] = MenuScreen()
                    interface.update()
                else:
                    self.unauthorized("unauthorized_access")
            else:
                self.unauthorized("unauthorized_access")
        else:
            page = e.control.page
            error_message(text="no_active_vault", page=page)
            self.username.value = ""
            self.password.value = ""
            self.username.update()
            self.password.update()

        # logo = ft.Image(
        #     width=434,
        #     height=143,
        #     src="./resources/images/Logo.png"
        # )
        #
        # enter_btn = ft.OutlinedButton(
        #     text=labels[sett.LAN]["enter"],
        #     width=208,
        #     height=54,
        #     style=sett.BTN_STYLE,
        #     on_hover=on_hover_box_btn,
        #     on_click=verification
        # )

        # super().__init__()
        # """Login screen layout"""
        # self.width = 1850
        # self.height = 586
        # self.content = (
        #     ft.Row(
        #         alignment=ft.MainAxisAlignment.CENTER,
        #         controls=[
        #             ft.Container(
        #                 bgcolor=ft.Colors.with_opacity(0.3, "#223026"),
        #                 border_radius=50,
        #                 width=538,
        #                 height=586,
        #                 padding=52,
        #                 content=(
        #                     ft.Column(
        #                         horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        #                         spacing=42,
        #                         controls=[
        #                             logo,
        #                             ft.Container(height=2),
        #                             ft.Row(
        #                                 alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        #                                 expand=True,
        #                                 controls=[
        #                                     ft.Text(
        #                                         value=labels[sett.LAN]["login"]
        #                                     ),
        #                                     self.username,
        #                                 ]
        #                             ),
        #                             ft.Row(
        #                                 alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        #                                 expand=True,
        #                                 controls=[
        #                                     ft.Text(
        #                                         value=labels[sett.LAN][
        #                                             "password"]
        #                                     ),
        #                                     self.password,
        #                                 ]
        #                             ),
        #                             enter_btn
        #                         ]
        #                     )
        #                 )
        #             )
        #         ]
        #     )
        # )


class MenuScreen(ft.Container):
    """Main menu screen for non-Game Master users."""

    def __init__(self):
        super().__init__()
        """Main menu screen layout"""
        # UI element
        self.door_status = self.get_door_status()
        self.door_status_btn = ft.TextButton(
            on_click=self.change_door_status,
            text=f"{labels[sett.LAN]["status"]}: [{self.door_status}]",
            style=sett.TXT_BTN_STYLE,
            on_hover=on_hover_btn
        )
        self.log_entries_btn = ControlButton(
            text="log_entries",
            on_click=self.open_log_screen
        )
        self.logout_btn = ControlButton(
            text="logout",
            on_click=logout
        )

        # Menu Screen layout
        self.width = 1850
        self.height = 586
        self.padding = ft.Padding(
            left=300,
            top=100,
            right=0,
            bottom=0
        )
        self.content = (
            ft.Column(
                controls=[
                    ft.Text(
                        value="- RobCo Trespasser Management System -",
                        weight=ft.FontWeight.BOLD
                    ),
                    double_divider,
                    ft.Text(
                        value=labels[sett.LAN]["env_sensors"]
                    ),
                    ft.Text(
                        value=labels[sett.LAN]["monitoring"]
                    ),
                    single_short_divider,
                    self.door_status_btn,
                    self.log_entries_btn,
                    single_short_divider,
                    self.logout_btn,
                    double_divider
                ]
            )
        )

    def get_door_status(self):
        """Gets the door status of the active vault."""
        try:
            with Session(engine) as active_vault_session:
                active_vault_data = select(Vault).where(
                    Vault.status == "active")
                active_vault = active_vault_session.scalar(
                    active_vault_data)
                return labels[sett.LAN][str(active_vault.door_status)]
                # self.door_status = labels[sett.LAN][active_vault_door_status]
        except Exception:
            error_message(text="problem_loading_data", page=self.page)

    def change_door_status(self, e):
        """Changes active vault door status for the time of the session"""
        if self.door_status == labels[sett.LAN]["closed"]:
            self.door_status = labels[sett.LAN]["open"]
        else:
            self.door_status = labels[sett.LAN]["closed"]
        self.door_status_btn.text = f"{labels[sett.LAN]["status"]}: [{self.door_status}]"
        self.door_status_btn.update()

    def open_log_screen(self, e):
        """Opens screen with log entries."""
        interface.controls[1] = LogEntriesScreen()
        interface.update()


class LogEntriesScreen(ft.Container):
    """Screen showing log entries for the active vault."""

    # Inner class with menu items
    class MenuItem(ft.Container):
        """Log entry menu item."""

        def __init__(self, data, on_select):
            def handle_click(e):
                on_select(
                    data.title,
                    data.date,
                    data.population,
                    data.text,
                    data.id
                )

            super().__init__(
                padding=5,
                alignment=ft.alignment.center,
                width=sett.MENU_ITEM_WIDTH,
                height=75,
                bgcolor="transparent",
                border=sett.BORDER,
                on_hover=on_hover_box,
                on_click=handle_click,
                content=ft.Column(
                    width=142,
                    alignment=ft.MainAxisAlignment.CENTER,
                    controls=[
                        MenuItemText(data.title),
                        MenuItemText(data.date, size=12)
                    ]
                )
            )

    # Screen definition
    def __init__(self):
        super().__init__()
        global active_user

        # Load entries from DB
        with Session(engine) as session:
            entries_data = (
                select(LogEntry)
                .join(LogEntry.vault)
                .where(Vault.status == "active")
            )
            self.active_entries = session.scalars(entries_data).all()

        # UI state variables
        self.entry_id = None
        self.detail_title = ft.Text(weight=ft.FontWeight.BOLD,
                                    style=sett.ENTRY_TXT_STYLE,
                                    value="")
        self.detail_date = ft.Text("")
        self.detail_population = ft.Text("")
        self.detail_text = ft.Text(style=sett.ENTRY_TXT_STYLE, value="")
        self.divider = ft.Text(value="")
        self.delete_btn = ft.Container()

        # Log Screen layout
        log_entries = self.build_menu_items(active_user)
        back_btn = ControlButton(text="back", on_click=self.back)

        self.height = 664
        self.width = 1850
        self.padding = ft.padding.symmetric(horizontal=233)
        self.content = ft.Column(
            controls=[
                ft.Row(
                    spacing=36,
                    controls=[
                        ft.Column(
                            width=sett.SIDE_LIST_WIDTH,
                            height=614,
                            scroll=ft.ScrollMode.ADAPTIVE,
                            controls=log_entries
                        ),
                        ft.VerticalDivider(
                            thickness=3,
                            leading_indent=50,
                            trailing_indent=50,
                            color=sett.FONT_COLOR
                        ),
                        ft.Container(
                            width=sett.LOG_ENTRY_WIDTH,
                            height=614,
                            content=ft.Column(
                                controls=[
                                    self.detail_title,
                                    self.detail_date,
                                    self.detail_population,
                                    self.divider,
                                    self.detail_text,
                                    self.delete_btn
                                ]
                            )
                        )
                    ]
                ),
                back_btn
            ]
        )

    def build_menu_items(self, active_user):
        """Builds the menu items for the log entries screen."""
        log_entries = []
        if active_user == "game master":
            add_new_entry_btn = ControlButton(
                text="add_log_entry",
                on_click=self.add_new_entry
            )
            log_entries.append(add_new_entry_btn)

        for data in self.active_entries:
            log_entries.append(
                self.MenuItem(data=data, on_select=self.show_details)
            )
        return log_entries

    def save_entry(self, e):
        """Saves a new log entry in the database."""
        empty_fields = []
        validation_empty_field(self.new_entry_title, empty_fields)
        validation_empty_field(self.new_entry_date, empty_fields)
        validation_empty_field(self.new_entry_population, empty_fields)

        if not empty_fields and self.new_entry_title.value.isdigit() and self.new_entry_population.value.isdigit():
            with Session(engine) as session:
                vault_data = select(Vault).where(Vault.status == "active")
                active_vault = session.scalar(vault_data)

                new_entry = LogEntry(
                    title=f"{self.new_entry_title.prefix_text}{self.new_entry_title.value}",
                    date=self.new_entry_date.value,
                    population=self.new_entry_population.value,
                    text=self.new_entry_text.value,
                    vault_id=active_vault.id
                )
                session.add(new_entry)
                session.commit()

            interface.controls[1] = LogEntriesScreen()
            interface.update()
        else:
            error_message(text="incorrect_data", page=self.page)

    def add_new_entry(self, e):
        """Creates a new log entry form."""

        def select_date(e):
            self.new_entry_date.value = e.control.value.strftime("%Y-%m-%d")
            self.new_entry_date.update()

        date_picker = DatePicker(
            first_date=datetime.date(2077, 1, 1),
            last_date=datetime.date(2288, 1, 1),
            on_change=select_date
        )

        self.new_entry_title_tag = ft.Text(f"{labels[sett.LAN]['entry']} #")
        self.new_entry_title = InputField(
            keyboard_type=ft.KeyboardType.NUMBER,
            prefix_text=labels[sett.LAN]["entry_prefix"],
            on_change=validation_num
        )
        self.new_entry_population_tag = ft.Text(labels[sett.LAN]["population"])
        self.new_entry_population = InputField(on_change=validation_num)
        self.new_entry_date_tag = ft.Text(labels[sett.LAN]["date"])
        self.new_entry_date = InputField(
            read_only=True,
            on_click=lambda e: e.page.open(date_picker)
        )
        self.new_entry_text = InputField(
            multiline=True,
            width=sett.SIDE_SCREEN_WIDTH,
            min_lines=10,
            max_lines=10,
        )

        save_entry_btn = ControlButton(text="save", on_click=self.save_entry)

        self.new_entry_form = ft.Column(
            controls=[
                ft.Text(value=labels[sett.LAN]["add_log_entry"],
                        style=sett.TXT_STYLE),
                double_divider,
                ft.Row([self.new_entry_title_tag, self.new_entry_title],
                       width=sett.FORM_FIELD_WIDTH,
                       alignment=ft.MainAxisAlignment.END),
                ft.Row(
                    [self.new_entry_population_tag, self.new_entry_population],
                    width=sett.FORM_FIELD_WIDTH,
                    alignment=ft.MainAxisAlignment.END),
                ft.Row([self.new_entry_date_tag, self.new_entry_date],
                       width=sett.FORM_FIELD_WIDTH,
                       alignment=ft.MainAxisAlignment.END),
                self.new_entry_text,
                double_divider,
                ft.Row([save_entry_btn],
                       width=sett.SIDE_SCREEN_WIDTH,
                       alignment=ft.MainAxisAlignment.END),
            ]
        )

        # Display add-form in the main part of the screen
        self.content.controls[0].controls[2] = self.new_entry_form
        self.content.controls[0].update()

    def delete_entry_confirmed(self, e):
        """Deletes selected entry."""
        with Session(engine) as session:
            entry = session.get(LogEntry, self.entry_id)
            if entry:
                session.delete(entry)
                session.commit()

        interface.controls[1] = LogEntriesScreen()
        interface.update()

    def show_details(self, title, date, population, text, entry_id):
        """Displays selected log entry in the main part of the screen."""
        self.detail_title.value = title
        self.detail_date.value = f"{labels[sett.LAN]['date']}: {date}"
        self.detail_population.value = f"{labels[sett.LAN]['population']}: {population}"
        self.detail_text.value = text
        self.divider.value = "=" * 94

        for entry_detail in [self.detail_title, self.detail_date,
                             self.detail_population,
                             self.detail_text, self.divider]:
            entry_detail.update()

        self.entry_id = entry_id

        if active_user == "game master":
            delete_dlg = DeleteDialog(
                label="delete_entry",
                text="delete_entry_confirmation",
                on_click=self.delete_entry_confirmed
            )
            self.delete_btn.content = ControlButton(
                text="delete_entry",
                on_click=lambda e: e.page.open(delete_dlg)
            )
            self.delete_btn.update()

    def back(self, e):
        """Return to previous menu depending on a user."""
        if active_user == "game master":
            interface.controls[1] = GameMasterMenu()
        else:
            interface.controls[1] = MenuScreen()
        interface.update()


class GameMasterMenu(ft.Container):
    """Game MAster Menu screen definition"""

    def __init__(self):
        super().__init__()
        vault_management_btn = ControlButton(
            text="vault_management",
            on_click=self.open_vault_manager)

        log_entries = ControlButton(
            text="log_entries",
            on_click=self.mg_log_entries)

        logout_btn = ControlButton(
            text="logout",
            on_click=logout)

        try:
            with Session(engine) as session:
                active_vault_data = select(Vault.vault_number).where(
                    Vault.status == "active")
                self.active_vault = session.scalar(active_vault_data)
            if not self.active_vault:
                self.active_vault = labels[sett.LAN]["no_active_vault_short"]
        except Exception as e:
            self.vaults = ["Error loading vaults"]

        """Game Master Menu layout"""
        self.width = 1850
        self.height = 586
        self.padding = ft.Padding(
            left=300,
            top=100,
            right=0,
            bottom=0
        )
        self.content = (
            ft.Column(
                controls=[
                    ft.Text(
                        value="- Game Master's Vault Manager -",
                        weight=ft.FontWeight.BOLD
                    ),
                    double_divider,
                    ft.Row(
                        controls=[
                            ft.Text(
                                f"{labels[sett.LAN]["active_vault"]}: {self.active_vault}"),
                        ]
                    ),
                    single_short_divider,
                    vault_management_btn,
                    log_entries,
                    single_short_divider,
                    logout_btn,
                    double_divider
                ]
            )
        )

    def open_vault_manager(self, e):
        """Opens screen with vault management options."""
        interface.controls[1] = VaultManager()
        interface.update()
        print(active_user)

    def mg_log_entries(self, e):
        """Opens screen with log entries."""
        interface.controls[1] = LogEntriesScreen()
        interface.update()


class VaultManager(ft.Container):
    class VaultItem(ft.Container):
        """Vault menu item."""

        def __init__(self, id, number, on_select):
            def handle_click(e):
                on_select(id, number)

            super().__init__(
                padding=5,
                alignment=ft.alignment.center,
                width=sett.MENU_ITEM_WIDTH,
                height=75,
                bgcolor="transparent",
                border=sett.BORDER,
                on_hover=on_hover_box,
                on_click=handle_click,
                content=ft.Column(
                    width=142,
                    alignment=ft.MainAxisAlignment.CENTER,
                    controls=[
                        MenuItemText(f"{labels[sett.LAN]['vault']} #{number}"),
                        MenuItemText("===========")
                    ]
                )
            )

    def __init__(self):
        super().__init__()

        # buttons
        save_vault_btn = ControlButton("save",
                                       on_click=self.update_vault_details)
        save_new_vault_btn = ControlButton("save", on_click=self.save_new_vault)
        delete_vault_btn = ControlButton("delete_vault",
                                         on_click=lambda e: e.page.open(
                                             self.delete_dlg))
        add_new_vault_btn = ControlButton("add_new_vault",
                                          on_click=self.add_new_vault_form)
        back_btn = ControlButton("back", on_click=self.back)

        # Delete - confirmation window
        self.delete_dlg = DeleteDialog(
            label="delete_vault",
            text="delete_vault_confirmation",
            on_click=self.delete_entry_confirmed,
        )

        self.vault_list = [add_new_vault_btn]

        # New Vault form
        self.vault_title = ft.Text("", weight=ft.FontWeight.BOLD,
                                   style=sett.ENTRY_TXT_STYLE)
        self.vault_status = DropdownList(options=vault_status_options)
        self.vault_door_status = DropdownList(options=vault_door_options)
        self.vault_security_level = DropdownList(options=security_level_options)
        self.overseer_password = InputField(width=200)

        # New Vault form layout
        self.vault_status_row = ft.Row(
            width=sett.VAULT_WIDTH,
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[ft.Text(labels[sett.LAN]["status"], style=sett.TXT_STYLE),
                      self.vault_status]
        )
        self.vault_door_status_row = ft.Row(
            width=sett.VAULT_WIDTH,
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                ft.Text(labels[sett.LAN]["door_status"], style=sett.TXT_STYLE),
                self.vault_door_status]
        )
        self.vault_security_level_row = ft.Row(
            width=sett.VAULT_WIDTH,
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[ft.Text(labels[sett.LAN]["security_level"],
                              style=sett.TXT_STYLE), self.vault_security_level]
        )
        self.overseer_password_row = ft.Column(
            width=sett.VAULT_WIDTH,
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                ft.Text(labels[sett.LAN]["overseer_access"],
                        style=sett.TXT_STYLE, weight=ft.FontWeight.BOLD),
                ft.Row(
                    width=sett.VAULT_WIDTH,
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        ft.Text(f"{labels[sett.LAN]['login']}: OVERSEER",
                                style=sett.TXT_STYLE),
                        ft.Text(f"{labels[sett.LAN]['password']}: ",
                                style=sett.TXT_STYLE),
                        self.overseer_password,
                    ]
                ),
            ]
        )

        # Vault details display
        self.vault_for_display = ft.Container(width=sett.LOG_ENTRY_WIDTH,
                                              height=614)

        self.load_vault_list()

        # Screen layout
        self.width = 1850
        self.height = 664
        self.padding = ft.padding.symmetric(horizontal=233)
        self.content = ft.Column(
            controls=[
                ft.Row(
                    spacing=36,
                    controls=[
                        ft.Column(
                            alignment=ft.MainAxisAlignment.CENTER,
                            width=sett.SIDE_LIST_WIDTH,
                            height=614,
                            scroll=ft.ScrollMode.ADAPTIVE,
                            controls=self.vault_list
                        ),
                        ft.VerticalDivider(
                            thickness=3, leading_indent=50, trailing_indent=50,
                            color=sett.FONT_COLOR
                        ),
                        self.vault_for_display,
                    ]
                ),
                back_btn
            ]
        )

    def unique_active_vault(self, session):
        """Ensure only one vault is active at a time."""
        session.execute(update(Vault).where(Vault.status == "active").values(
            status="inactive"))
        session.commit()

    def back(self, e):
        """Return to Game Master menu."""
        interface.controls[1] = GameMasterMenu()
        interface.update()

    def add_new_vault_form(self, e):
        """Show form for adding a new vault."""
        self.new_vault_title = InputField(on_change=validation_num)
        self.vault_status.value = ""
        self.vault_door_status.value = ""
        self.vault_security_level.value = ""
        self.overseer_password.value = ""

        self.new_vault_title_row = ft.Column(
            controls=[
                ft.Text(labels[sett.LAN]["add_new_vault"], style=sett.TXT_STYLE,
                        weight=ft.FontWeight.BOLD),
                double_divider,
                ft.Row(
                    width=sett.VAULT_WIDTH,
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[ft.Text(f"{labels[sett.LAN]['vault']} #",
                                      style=sett.TXT_STYLE),
                              self.new_vault_title],
                ),
            ]
        )

        save_new_vault_btn = ControlButton("save", on_click=self.save_new_vault)
        self.new_vault_form = ft.Column(
            controls=[
                self.new_vault_title_row,
                self.vault_status_row,
                self.vault_security_level_row,
                self.vault_door_status_row,
                double_divider,
                self.overseer_password_row,
                ft.Row(width=sett.SIDE_SCREEN_WIDTH,
                       alignment=ft.MainAxisAlignment.END,
                       controls=[save_new_vault_btn]),
            ]
        )
        self.vault_for_display.content = self.new_vault_form
        self.vault_for_display.update()

    def save_new_vault(self, e):
        """Save a new vault in the database."""
        empty_fields = []
        validation_empty_field(self.new_vault_title, empty_fields)
        validation_empty_field(self.vault_status, empty_fields)
        validation_empty_field(self.overseer_password, empty_fields)
        validation_empty_field(self.vault_security_level, empty_fields)
        validation_empty_field(self.vault_door_status, empty_fields)

        if not empty_fields and self.new_vault_title.value.isdigit():
            try:
                with Session(engine) as new_vault_session:
                    if self.vault_status.value == "active":
                        self.unique_active_vault(new_vault_session)

                    new_vault = Vault(
                        vault_number=self.new_vault_title.value,
                        status=self.vault_status.value,
                        security_level=self.vault_security_level.value,
                        door_status=self.vault_door_status.value,
                        overseer_password=self.overseer_password.value,
                    )
                    new_vault_session.add(new_vault)
                    new_vault_session.commit()

                    interface.controls[1] = VaultManager()
                    interface.controls[0] = Header()
                    interface.update()
            except IntegrityError:
                error_message("vault_exists", self.page)
        else:
            error_message(text="incorrect_data", page=self.page)

    def update_vault_details(self, e):
        """Update details of the selected vault."""
        with Session(engine) as update_session:
            if self.vault_status.value == "active":
                self.unique_active_vault(update_session)

            vault_to_update = update_session.get(Vault, self.vault_id)
            vault_to_update.status = self.vault_status.value
            vault_to_update.security_level = self.vault_security_level.value
            vault_to_update.door_status = self.vault_door_status.value
            vault_to_update.overseer_password = self.overseer_password.value
            update_session.commit()

        update_dlg = ft.AlertDialog(
            modal=True,
            bgcolor=sett.POP_UP_COLOR,
            shape=ft.RoundedRectangleBorder(radius=0),
            title=ft.Text(labels[sett.LAN]["vault_update"],
                          color=sett.FONT_COLOR),
            content=ft.Text(labels[sett.LAN]["vault_updated"]),
            actions=[ControlButton("ok", on_click=lambda e: e.page.close(
                update_dlg))],
        )
        interface.controls[0] = Header()
        interface.update()
        e.page.open(update_dlg)

    def delete_entry_confirmed(self, e):
        """Delete the selected vault after confirmation."""
        with Session(engine) as delete_session:
            vault_for_delete = delete_session.get(Vault, self.vault_id)
            delete_session.delete(vault_for_delete)
            delete_session.commit()

        interface.controls[1] = VaultManager()
        interface.update()
        e.page.close(self.delete_dlg)

    def show_vault_details(self, id, number):
        """Display vault details based on selection."""
        try:
            vault_query = select(Vault).where(Vault.id == id)
            with Session(engine) as session2:
                vault_details = session2.scalar(vault_query)

                if vault_details:
                    self.vault_id = vault_details.id
                    self.vault_title.value = f"{labels[sett.LAN]['vault']} # {vault_details.vault_number}"
                    self.vault_status.value = vault_details.status
                    self.vault_security_level.value = vault_details.security_level
                    self.vault_door_status.value = vault_details.door_status
                    self.overseer_password.value = vault_details.overseer_password

            self.vault_information = ft.Column(
                controls=[
                    self.vault_title,
                    double_divider,
                    self.vault_status_row,
                    self.vault_security_level_row,
                    self.vault_door_status_row,
                    double_divider,
                    self.overseer_password_row,
                    ft.Row(
                        width=sett.SIDE_SCREEN_WIDTH,
                        alignment=ft.MainAxisAlignment.END,
                        controls=[ControlButton("save",
                                                on_click=self.update_vault_details),
                                  ControlButton("delete_vault",
                                                on_click=lambda e: e.page.open(
                                                    self.delete_dlg))]
                    )
                ]
            )
            self.vault_for_display.content = self.vault_information
            self.vault_for_display.update()

        except Exception as e:
            error_message("problem_loading_vault", e.page)
            print("Data problem", e)

    def load_vault_list(self):
        """Load all vaults into the sidebar list."""
        try:
            with Session(engine) as session:
                vaults = session.scalars(select(Vault)).all()
                if vaults:
                    for vault in vaults:
                        self.vault_list.append(
                            self.VaultItem(id=vault.id,
                                           number=vault.vault_number,
                                           on_select=self.show_vault_details)
                        )
                else:
                    self.vault_list.append(
                        ft.Container(
                            content=ft.Text(labels[sett.LAN]["no_vaults"],
                                            style=sett.TXT_STYLE,
                                            weight=ft.FontWeight.BOLD))
                    )
        except Exception:
            self.vault_list = [ft.Text("Error loading vaults")]


engine = create_engine("sqlite:///resources/database/vault.db")

header = Header()
login_screen = LogInPage()
vault_manager = VaultManager()

interface = ft.Column(
    alignment=ft.MainAxisAlignment.CENTER,
    spacing=36,
    controls=[
        header,
        login_screen,
    ]

)
