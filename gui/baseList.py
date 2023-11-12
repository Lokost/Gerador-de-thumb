# coding: utf-8

import flet as ft
import function as func

from gui.window import Window


def bases_list(page: ft.Page, gui):
    page.clean()
    page.title = "Bases de imagens"
    page.window_width = 400
    page.window_height = 400
    page.horizontal_alignment = "center"

    class alias_tile:
        def __init__(self, alias, edit, delete):
            self.alias = alias
            self.edit = edit
            self.delete = delete
        
        def build(self):
            return ft.Row(
                [
                    ft.Text(self.alias, weight=ft.FontWeight.BOLD),
                    ft.Row(
                        [
                            ft.IconButton(
                                icon=ft.icons.EDIT,
                                on_click=lambda _: self.edit(self.alias)
                            ),

                            ft.IconButton(
                                icon=ft.icons.DELETE,
                                on_click=lambda _: self.delete(self.alias)
                            ),
                        ]
                    ),
                ],
                expand=True,
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            )

    def minimize():
        page.window_minimized = True
        page.update()

    def edit_base(alias):
        gui.set_gui(Window.newbase, True, alias)

    def delete_base(alias):
        func.remove_base(alias)
        gui.set_gui(Window.bases_list)
        page.update()
        return True if alias in func.get_alias() else False

    def get_alias():
        return [
            alias_tile(value, edit_base, delete_base).build()
            for value in func.get_alias()
        ]

    appBar = ft.AppBar(
        title=ft.Text("Bases"),
        center_title=False,
        leading=ft.IconButton(
            icon=ft.icons.ARROW_BACK, on_click=lambda _: gui.set_gui(Window.main)
        ),
        actions=[
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

    dragWindow = ft.WindowDragArea(
        content=ft.Row(
            [ft.Icon(ft.icons.DRAG_HANDLE)],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
    )

    add_button = ft.ElevatedButton(
        icon=ft.icons.ADD,
        text="Adicionar base",
        on_click=lambda e: gui.set_gui(Window.newbase),
    )

    btt_row = ft.Row([add_button], alignment=ft.MainAxisAlignment.CENTER)

    alias_list = ft.ListView(
        expand=True,
        spacing=10,
        controls=get_alias(),
    )

    page.add(appBar, dragWindow, alias_list, btt_row)


# Fim
