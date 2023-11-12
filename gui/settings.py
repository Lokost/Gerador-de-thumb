# coding: utf-8

import flet as ft
import function as func
from gui.window import Window


def settings_gui(page: ft.Page, gui):
    page.clean()
    page.window_height = 250
    page.window_width = 500
    page.horizontal_alignment = "center"
    page.title = "Configurações"

    config = func.get_config()

    # Components
    appBar = ft.AppBar(
        title=ft.Text("Configurações"),
        center_title=False,
        leading=ft.IconButton(
            ft.icons.ARROW_BACK,
            on_click=lambda _: gui.set_gui(Window.main),
        ),
        actions=[
            ft.IconButton(
                ft.icons.HELP,
                tooltip="Sobre",
                on_click=lambda _: gui.set_gui(Window.about),
            ),
            ft.IconButton(
                ft.icons.MINIMIZE,
                tooltip="Minimizar",
                on_click=lambda _: minimize(),
            ),
            ft.IconButton(
                ft.icons.CLOSE,
                tooltip="Fechar",
                on_click=lambda _: page.window_close(),
            ),
        ],
    )

    dragWindow = ft.WindowDragArea(
        content=ft.Row(
            [ft.Icon(ft.icons.DRAG_HANDLE)],
            alignment="center",
        )
    )

    pathField = ft.TextField(
        value=config["outputFolder"],
        label="Pasta de Saída",
        width=200,
        read_only=True,
        expand=True,
    )

    browseFolder = ft.FilePicker(
        on_result=lambda e: update_field(e, pathField),
    )

    searchFolder = ft.ElevatedButton(
        icon=ft.icons.FOLDER_OPEN,
        text="Procurar",
        on_click=lambda _: browseFolder.get_directory_path(),
    )

    folderPick = ft.Row([pathField, searchFolder])

    save_button = ft.ElevatedButton(text="Save", on_click=lambda _: save_settings())

    page.add(
        appBar,
        dragWindow,
        folderPick,
        browseFolder,
        save_button,
    )

    # Functions
    def save_settings():
        func.save_config(path=pathField.value)
        gui.set_gui(Window.main)

    def update_field(e, field):
        content = e.path if e.path else ""

        if content:
            field.value = content
            page.update()

    def minimize():
        page.window_minimized = True
        page.update()


# Fim
