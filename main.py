# coding: utf-8

from flet import Page, app
from function import Alert, db_execute, get_config
from gui.gui_manager import Gui
from gui.window import Window


class Main:
    """
    Main Class
    
    Where the primary settings of the app was set.
    """

    def __init__(self, page: Page) -> None:
        get_config()
        db_execute(
            """CREATE TABLE IF NOT EXISTS bases(
                   id INTEGER PRIMARY KEY AUTOINCREMENT, 
                   alias TEXT NOT NULL, path TEXT NOT NULL, 
                   title_max INT, 
                   x INT NOT NULL, 
                   y INT NOT NULL, 
                   font TEXT, 
                   font_size INT NOT NULL,
                   stroke_color TEXT NOT NULL, 
                   stroke_weight INT
                )"""
        )
        get_config()
        self.page = page
        self.page.title = "Thumb Generator"
        self.alert = Alert()
        self.gui = Gui(self.page, self.alert)
        self.gui.set_gui(Window.main)

app(target=Main)

#Fim
