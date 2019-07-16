import controller
from controller import *
from tkinter import *
from tkinter import messagebox
import datetime
from tkinter import ttk


class DayDialog:
    def __init__(self, app, day: int):
        self.top = Toplevel(app.mainWindow)
        self.top.transient(app.mainWindow)
        self.top.grab_set()
        DayDialog.DayFrame(self, day, app)

    def ok(self):
        self.top.destroy()

    def cancel(self):
        self.top.destroy()

    class DayFrame:
        def __init__(self, parent, day: int, app):
            self.state = app.state
            self.day = day
            self.window = parent.top
            self.parent = parent
            self.initUI()

        def initUI(self):
            notes, images = self.state.get_day_data(self.day)
            frame = ttk.Frame(self.window)
            frame.pack(fill=BOTH)
            # frame = self

            notes_frame = ttk.LabelFrame(frame, text="Notatki")
            ttk.Button(notes_frame, text="+").pack()
            if len(notes) == 0:
                ttk.Label(notes_frame, text="Brak notatek.").pack()
            for n in notes:
                ttk.Label(notes_frame, text=n['value']).pack()

            images_frame = ttk.LabelFrame(frame, text="Obrazy")
            ttk.Button(images_frame, text="+").pack()

            if len(images) == 0:
                ttk.Label(images_frame, text="Brak obrazów.").pack()
            for i in images:
                ttk.Label(images_frame, text=i['path']).pack()

            buttons_frame = ttk.Frame(frame)
            ttk.Button(buttons_frame, text='Anuluj', command=self.parent.cancel).pack(side=RIGHT)
            ttk.Button(buttons_frame, text='Ok', command=self.parent.ok).pack(side=RIGHT)

            buttons_frame.pack(side=BOTTOM, anchor=E)

            notes_frame.pack(side=LEFT, fill=BOTH, padx=2, pady=2)
            images_frame.pack(side=LEFT, fill=BOTH, padx=2, pady=2)
