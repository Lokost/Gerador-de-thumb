# coding: utf-8


from function import Alert
from gui.about import about
from gui.baseList import bases_list
from gui.mainWindow import mainWindow
from gui.newBase import new_base
from gui.settings import settings_gui
from gui.window import Window


class Gui:
    """
    Class GUI

    This class will be responsible for create and manage the app GUIs.
    """

    def __init__(self, page, alert: Alert):
        self.__page = page

    def set_gui(self, window: Window, *args):
        self.__current_gui = window
        self.run(args)

    def run(self, args=[]):
        match (self.__current_gui):
            case Window.main:
                mainWindow(self.__page, self)
        
            case Window.newbase:
                new_base(self.__page, self, *args)

            case Window.bases_list:
                bases_list(self.__page, self)

            case Window.settings:
                settings_gui(self.__page, self)

            case Window.about:
                about(self.__page, self)


# Fim
