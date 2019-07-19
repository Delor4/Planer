from tkinter import *

from gui import PlanerApp


class PlanerBaseDialog:

    def __init__(self, parent, title: str = None):
        self.parent = parent
        self.app = parent.app
        self.state = parent.state
        self.T = parent.T

        self.top = Toplevel(parent.top)
        self.top.transient(parent.top)
        self.top.grab_set()

        PlanerApp.set_icon(self.top)

        self.set_title(title)

    def close_window(self):
        self.top.destroy()

    def set_title(self, title: str = None):
        tmp_title = PlanerApp.app_name
        if title is not None:
            tmp_title += " - " + title
        self.top.title(tmp_title)
