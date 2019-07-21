import platform
from tkinter import *


class PlanerBaseDialog:
    """
    Base class for all windows in app.
    """
    app_name = "Planer"

    def __init__(self, parent, title: str = None, window=None):
        self.parent = parent
        self.app = parent.app
        self.state = parent.state
        self.T = parent.T

        self.top = window

        self.set_icon()

        self.set_title(title)

    def close_window(self):
        self.top.destroy()

    def set_title(self, title: str = None):
        tmp_title = self.app_name
        if title is not None:
            tmp_title += " - " + title
        self.top.title(tmp_title)

    def set_icon(self):
        self._set_icon(self.top)

    @staticmethod
    def _set_icon(window):
        if platform.system() == 'Windows':
            window.iconbitmap("planer.ico")
        elif platform.system() == 'Linux':
            window.tk.call('wm', 'iconphoto', window._w, PhotoImage(file='planer.png'))


class PlanerBaseModalDialog(PlanerBaseDialog):
    """
    Base class for all child windows in app.
    """

    def __init__(self, parent, title: str = None):
        self.top = Toplevel(parent.top)
        self.top.transient(parent.top)
        self.top.grab_set()

        # set position
        self.top.geometry("+{0}+{1}".format(parent.top.winfo_x() + 20, parent.top.winfo_y() + 20))

        PlanerBaseDialog.__init__(self, parent, title=title, window=self.top)


class TextDialog(PlanerBaseModalDialog):
    """
    Class for input text from user.
    """

    def __init__(self, parent: PlanerBaseDialog, prompt: str, text: str = None, title: str = None):
        PlanerBaseModalDialog.__init__(self, parent, title=title)
        self.value = StringVar()
        self.ok = False

        if text is not None:
            self.value.set(text)

        self._init_ui(prompt)
        self.parent.top.wait_window(self.top)

    def _init_ui(self, prompt: str):
        Label(self.top, text=prompt, wraplength=500).pack(anchor=W, padx=5)
        e = Entry(self.top, textvariable=self.value, width=40)
        e.pack(fill=X, padx=5)
        e.bind('<Return>', lambda event: self._on_ok())
        Button(self.top, text=self.T("ok"), command=self._on_ok).pack(anchor=E, padx=5, pady=5)

    def _on_ok(self):
        self.ok = True
        self.close_window()

    def get_value(self):
        return self.value.get()


class YesNoDialog(PlanerBaseModalDialog):

    def __init__(self, parent: PlanerBaseDialog, prompt: str, title: str = None):
        PlanerBaseModalDialog.__init__(self, parent, title=title)
        self.yes = False
        self.no = False

        self._init_ui(prompt)
        self.parent.top.wait_window(self.top)

    def _init_ui(self, prompt: str):
        Label(self.top, text=prompt, wraplength=500).pack(anchor=W, padx=5, pady=5)

        f = Frame(self.top)
        Button(f, text=self.T("yes").capitalize(), command=self._on_yes).pack(side=LEFT, padx=5, pady=5)
        Button(f, text=self.T("no").capitalize(), command=self._on_no).pack(side=RIGHT, padx=5, pady=5)
        f.pack()

    def _on_yes(self):
        self.yes = True
        self.close_window()

    def _on_no(self):
        self.no = True
        self.close_window()


class CaptionDialog(PlanerBaseModalDialog):

    def __init__(self, parent: PlanerBaseDialog, caption: str, title: str = None):
        PlanerBaseModalDialog.__init__(self, parent, title=title)

        self._init_ui(caption)
        self.parent.top.wait_window(self.top)

    def _init_ui(self, prompt: str):
        Label(self.top, text=prompt, wraplength=500).pack(anchor=W, padx=25, pady=10)

        Button(self.top, text=self.T("ok").capitalize(), command=self._on_ok).pack(padx=5, pady=5)

    def _on_ok(self):
        self.close_window()
