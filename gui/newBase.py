# coding: utf-8

import flet as ft
import flet.canvas as cv

from PIL import Image

import function as func
from gui.window import Window


def new_base(page: ft.Page, gui, edit=False, alias=""):
    """
    New Base

    This page will be responsible for create and edit bases

    parameters:

    page: flet.Page = Page where the components will be showed
    gui: gui.gui = gui object
    edit: bool = If the base is being edited
    alias: str = Alias of the base
    """

    page.clean()
    page.window_height = 710
    page.window_width = 580
    page.window_title_bar_hidden = True
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.title="Nova base" if not edit else "Editar base"

    data = {
        "imgWidth": 512,
        "imgHeight": 288,
        "opened_img_size": {"x": 0, "y": 0},
        "x": 0,
        "y": 0,
        "img": ".",
        "alias": "",
        "stroke_color": "",
        "stroke_weight": 0,
        "text": {"text": "Teste\nxx/xx/xx\nxxh", "size": 30, "color": ft.colors.WHITE},
    }

    # Components
    background = ft.Image(
        src=data["img"], width=data["imgWidth"], height=data["imgHeight"], expand=False
    )

    canvas = cv.Canvas(width=data["imgWidth"], height=data["imgHeight"], expand=False)

    st = ft.Stack([background, canvas])

    appBar = ft.AppBar(
        title=ft.Text("Nova Base" if not edit else "Editar base"),
        center_title=False,
        leading=ft.IconButton(
            ft.icons.ARROW_BACK,
            on_click=lambda _: gui.set_gui(Window.bases_list),
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
            [
                ft.Icon(ft.icons.DRAG_HANDLE),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
    )

    imgPath = ft.TextField(
        label="Caminho da imagem",
        value=data["img"] if data["img"] != "." else "",
        content_padding=10,
        read_only=True,
        expand=True,
    )

    filePick = ft.FilePicker(on_result=lambda e: change_img(e))

    browse = ft.ElevatedButton(
        text="Procurar",
        on_click=lambda _: filePick.pick_files(),
    )

    imgPick = ft.Row([imgPath, browse])

    xpos = ft.TextField(
        label="X: ",
        value=str(data["x"]),
        keyboard_type=ft.KeyboardType.NUMBER,
        text_align="center",
        expand=True,
        on_change=lambda e: change_pos(e, "x"),
        content_padding=10,
    )

    ypos = ft.TextField(
        label="Y: ",
        value=str(data["y"]),
        keyboard_type=ft.KeyboardType.NUMBER,
        text_align="center",
        expand=True,
        on_change=lambda e: change_pos(e, "y"),
        content_padding=10,
    )

    positionFields = ft.Row([xpos, ypos])

    aliasField = ft.TextField(
        label="Apelido",
        value=data["alias"] if data["alias"] else alias,
        text_align="center",
        expand=True,
        content_padding=10,
    )

    stroke_color_view = cv.Canvas(width=50, height=50, expand=False)

    color_code = ft.TextField(
        label="Cor do contorno (Hex)",
        expand=True,
        on_change=lambda e: update_color_view(
            e.control.value
            if e.control.value.startswith("#")
            else f"#{e.control.value}"
        ),
        prefix_text="#",
    )

    stroke_weight = ft.TextField(
        label="Grossura",
        expand=True,
        keyboard_type=ft.KeyboardType.NUMBER,
    )

    strokeSet = ft.Row([stroke_color_view, color_code, stroke_weight])

    cancel_btt = ft.ElevatedButton(
        text="Cancelar",
        icon=ft.icons.CANCEL,
        on_click=lambda _: gui.set_gui(Window.bases_list),
    )

    save_btt = ft.ElevatedButton(
        text="Salvar",
        icon=ft.icons.SAVE,
        on_click=lambda _: save_base(),
    )

    bttRow = ft.Row([cancel_btt, save_btt], alignment=ft.MainAxisAlignment.CENTER)

    page.add(
        appBar,
        dragWindow,
        st,
        filePick,
        imgPick,
        positionFields,
        aliasField,
        strokeSet,
        bttRow,
    )

    # Functions

    def save_base():
        if not edit:
            func.add_alias(
                aliasField.value,
                imgPath.value,
                float(xpos.value),
                float(ypos.value),
                color_code.value
                if color_code.value.startswith("#")
                else f"#{color_code.value}",
                float(stroke_weight.value),
            )

        else:
            func.update_base(
                aliasField.value,
                imgPath.value,
                float(xpos.value),
                float(ypos.value),
                color_code.value,
                float(stroke_weight.value),
            )

        gui.set_gui(Window.bases_list)

    def change_pos(e, axis):
        try:
            if isinstance(e, (float, int)):
                value = float(e)
            else:
                value = float(e.control.value)

            if axis == "x":
                data["x"] = (data["imgWidth"] / data["opened_img_size"]["x"]) * float(
                    value
                )

            elif axis == "y":
                data["y"] = (data["imgHeight"] / data["opened_img_size"]["y"]) * float(
                    value
                )

        except ValueError:
            pass

        canvas.clean()
        canvas.shapes = [
            cv.Text(
                data["x"],
                data["y"],
                data["text"]["text"],
                style=ft.TextStyle(
                    color=data["text"]["color"],
                    size=data["text"]["size"],
                ),
                text_align=ft.TextAlign.CENTER,
                alignment=ft.alignment.top_center,
            )
        ]
        canvas.update()

    def update_color_view(color="#FFFFFF"):
        stroke_color_view.clean()
        stroke_color_view.shapes = [
            cv.Rect(
                0,
                0,
                50,
                50,
                paint=ft.Paint(color=color, style=ft.PaintingStyle.FILL),
            )
        ]

        stroke_color_view.update()

    def change_img(e):
        if isinstance(e, str):
            img = e
        else:
            img = e.files[0].path if e.files else "."

        imgPath.value = img
        background.src = img
        with Image.open(img) as file:
            data["opened_img_size"]["x"], data["opened_img_size"]["y"] = file.size

        page.update()

    def minimize():
        page.window_minimized = True
        page.update()

    ## If is to edit a base:
    if edit and alias:
        base = func.get_base(alias)
        change_img(base["source"])
        change_pos(base["x"], "x")
        change_pos(base["y"], "y")
        xpos.value, ypos.value, color_code.value, stroke_weight.value = (
            base["x"],
            base["y"],
            base["stroke_color"][1:],
            base["stroke_weight"],
        )
        update_color_view(base["stroke_color"])
        page.update()


# Fim
