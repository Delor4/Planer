import platform
from tkinter import *


class PlanerBaseDialog:
    app_name = "Planer"

    def __init__(self, parent, title: str = None):
        self.parent = parent
        self.app = parent.app
        self.state = parent.state
        self.T = parent.T

        self.top = Toplevel(parent.top)
        self.top.transient(parent.top)
        self.top.grab_set()

        PlanerBaseDialog.set_icon(self.top)

        self.set_title(title)

    def close_window(self):
        self.top.destroy()

    def set_title(self, title: str = None):
        tmp_title = PlanerBaseDialog.app_name
        if title is not None:
            tmp_title += " - " + title
        self.top.title(tmp_title)

    @staticmethod
    def set_icon(window):
        if platform.system() == 'Windows':
            window.iconbitmap("planer.ico")
        elif platform.system() == 'Linux':
            window.tk.call('wm', 'iconphoto', window._w, PhotoImage(file='planer.png'))
