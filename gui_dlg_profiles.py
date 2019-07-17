from tkinter import Toplevel


class ProfilesDialog:
    def __init__(self, app):
        self.top = Toplevel(app.mainWindow)
        self.top.transient(app.mainWindow)
        self.top.grab_set()
        self.top.iconbitmap("planer.ico")
        # self.top.tk.call('wm', 'iconphoto', self.mainWindow._w, PhotoImage(file='planer.png'))
        self.top.title("Planer - Profile")
