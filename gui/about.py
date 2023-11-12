# coding: utf-8

import flet as ft
import function as func
from webbrowser import open

from gui.window import Window


def about(page: ft.Page, gui):
    page.clean()
    page.window_width = 350
    page.window_height = 350
    page.horizontal_alignment = "center"
    page.vertical_alignment = "center"
    page.title = "Sobre"

    # Components

    appBar = ft.AppBar(
        title=ft.Text("Sobre"),
        center_title=False,
        leading=ft.IconButton(
            ft.icons.ARROW_BACK,
            on_click=lambda _: gui.set_gui(Window.settings),
        ),
        actions=[
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

    icon = ft.Image(
        src=func.resource_path("icon.png"),
        height=80,
        width=80,
    )

    name = ft.Text(
        "Gerador de Thumb", style=ft.TextStyle(size=20, weight=ft.FontWeight.BOLD)
    )

    version = ft.Text(f"Versão: {func.data['version']}")

    copy = ft.Text(
        "Copyright @ Gabriel Gomes 2023. Sob a licença GNU GPLv3",
        text_align="center",
    )

    git = ft.ElevatedButton(
        text="GitHub",
        on_click=lambda _: open("https://github.com/Lokost"),
    )

    page.add(
        appBar,
        dragWindow,
        icon,
        name,
        version,
        copy,
        git,
    )  # <-- Add the components here.

    # Functions

    def update_field(e, field):
        content = e.path if e.path else ""

        if content:
            field.value = content
            page.update()

    def minimize():
        page.window_minimized = True
        page.update()


# Fim
