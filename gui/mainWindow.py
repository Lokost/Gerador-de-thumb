# coding: utf-8

import flet as ft
import function as func

from gui.window import Window


def mainWindow(page: ft.Page, gui):
    """
    Main Window

    :param page: The page that will show the components
    :param gui: The GUI class from the app
    """

    page.clean()
    page.title = "Gerador de Thumb"
    page.window_width = 400
    page.window_height = 400
    page.window_resizable = False
    page.window_maximizable = False
    page.window_title_bar_hidden = True
    page.horizontal_alignment = ft.CrossAxisAlignment.START

    data = {"alias": "*"}

    # Components

    dragWindow = ft.WindowDragArea(
        content=ft.Row([ft.Icon(ft.icons.DRAG_HANDLE)], alignment="center")
    )

    appBar = ft.AppBar(
        title=ft.Text("Gerador de Thumb"),
        center_title=False,
        actions=[
            ft.IconButton(
                ft.icons.SETTINGS,
                tooltip="Configurações",
                on_click=lambda e: gui.set_gui(Window.settings),
            ),
            ft.IconButton(
                ft.icons.MINIMIZE,
                tooltip="Minimizar",
                on_click=lambda e: minimize(),
            ),
            ft.IconButton(
                ft.icons.CLOSE,
                tooltip="Fechar",
                on_click=lambda e: page.window_close(),
            ),
        ],
    )

    title = ft.Text("Configurar a Thumb")

    alias = ft.Dropdown(
        options=[ft.dropdown.Option("*")]
        + [ft.dropdown.Option(i) for i in func.get_alias()],
        on_focus=lambda _: update_alias(),
        on_change=lambda e: set_alias(e.control.value),
        tooltip='Deixe "*" para pegar um apelido aleatório.',
        label="Apelido",
        expand=True,
    )

    today = ft.Checkbox(
        label="A live será hoje",
        value=True,
        on_change=lambda e: showField(not e.control.value, dateRow),
    )

    dayField = ft.TextField(
        label="Dia",
        keyboard_type=ft.KeyboardType.NUMBER,
        max_length=2,
        expand=True,
    )

    monthField = ft.TextField(
        label="Mês",
        keyboard_type=ft.KeyboardType.NUMBER,
        max_length=2,
        expand=True,
    )

    yearField = ft.TextField(
        label="Ano",
        keyboard_type=ft.KeyboardType.NUMBER,
        max_length=2,
        expand=True,
    )

    dateRow = ft.Row(
        [dayField, monthField, yearField],
        visible=False,
    )

    nextHour = ft.Checkbox(
        label="Hora automática",
        value=True,
        on_change=lambda e: showField(not e.control.value, hourField),
    )

    hourField = ft.TextField(
        label="Hora",
        visible=False,
        suffix_text="h",
        keyboard_type=ft.KeyboardType.NUMBER,
        max_length=2,
    )

    hasTitle = ft.Checkbox(
        label="Há título",
        value=False,
        on_change=lambda e: showField(e.control.value, titleField),
    )

    titleField = ft.TextField(
        label="Título",
        visible=False,
        max_length=20,
    )

    generateButton = ft.ElevatedButton(
        text="Gerar",
        icon=ft.icons.CHECK_CIRCLE_OUTLINE,
        on_click=lambda _: generate(),
    )

    thumbBases = ft.ElevatedButton(
        text="Bases",
        icon=ft.icons.IMAGE,
        on_click=lambda _: gui.set_gui(Window.bases_list),
    )

    buttonsRow = ft.Row(
        [generateButton, thumbBases],
        alignment="center",
        expand=True,
    )

    page.add(
        dragWindow,
        appBar,
        title,
        alias,
        today,
        dateRow,
        nextHour,
        hourField,
        hasTitle,
        titleField,
        buttonsRow,
    )

    # Functions

    def update_alias():
        """
        Update the alias dropdown
        """

        alias.options = [ft.dropdown.Option("*")] + [
            ft.dropdown.Option(i) for i in func.get_alias()
        ]

    def set_alias(e):
        """
        Set the alias
        """

        data["alias"] = e

    def showField(value, field: ft.TextField):
        """
        Show the field if the checkbox is checked
        """
        field.visible = value
        if value:
            page.window_height += 90
        else:
            page.window_height -= 90

        page.update()

    def minimize():
        page.page_minimized = True
        page.update()

    def generate():
        generator = func.ThumbGen(
            auto_date = today.value,
            auto_hour = nextHour.value,
            title = titleField.value if hasTitle.value else None,
            alias = data["alias"],
        )

        if not today.value:
            generator.set_date(f"{dayField.value}/{monthField.value}/{yearField.value}" if (dayField.value and monthField.value and yearField.value) else "")
        
        if not nextHour.value:
            generator.set_hour(hourField.value + "h" if hourField.value else "")

        generator.generate()


# Fim
