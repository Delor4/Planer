from tkinter import *
from tkinter import ttk


class DayDialog:
    def __init__(self, app, day: int):
        self.top = Toplevel(app.mainWindow)
        self.top.transient(app.mainWindow)
        self.top.grab_set()
        DayDialog.DayFrame(self, day, app)

    class DayFrame:
        def __init__(self, parent, day: int, app):
            self.state = app.state
            self.day = day
            self.window = parent.top
            self.parent = parent

            self.notes_data = []

            self.initUI()

        def ok(self):
            for n in self.notes_data:
                text = n['text_widget'].get("1.0", 'end-1c')
                if text != n['old_value']:
                    self.state.update_textnote(n['id'], text)
            self.parent.top.destroy()

        def cancel(self):
            self.parent.top.destroy()

        def initUI(self):
            notes, images = self.state.get_day_data(self.day)
            frame = ttk.Frame(self.window)
            frame.pack(fill=BOTH)

            notes_frame = self.make_notes_frame(frame, notes)
            images_frame = self.make_images_frame(frame, images)
            buttons_frame = self.make_buttons_frame(frame)

            buttons_frame.pack(side=BOTTOM, anchor=E)
            notes_frame.pack(side=LEFT, fill=BOTH, padx=2, pady=2)
            images_frame.pack(side=LEFT, fill=BOTH, padx=2, pady=2)

        def make_frame_note(self, frame, note_data):
            f = Frame(frame)
            tn = Text(f, height=4, wrap=WORD)
            tn.insert("1.0", note_data['value'])
            sy = Scrollbar(f)
            sy.pack(side=RIGHT, fill=Y)
            tn.pack()
            sy.config(command=tn.yview)
            f.pack()
            self.notes_data.append({'id': note_data['id'], 'old_value': note_data['value'], 'text_widget': tn})

        def make_notes_frame(self, frame, notes):
            notes_frame = ttk.LabelFrame(frame, text="Notatki")
            ttk.Button(notes_frame, text="+").pack()
            if len(notes) == 0:
                ttk.Label(notes_frame, text="Brak notatek.").pack()
            for n in notes:
                self.make_frame_note(notes_frame, n)
            return notes_frame

        def make_images_frame(self, frame, images):
            images_frame = ttk.LabelFrame(frame, text="Obrazy")
            ttk.Button(images_frame, text="+").pack()

            if len(images) == 0:
                ttk.Label(images_frame, text="Brak obrazów.").pack()
            for i in images:
                ttk.Label(images_frame, text=i['path']).pack()
            return images_frame

        def make_buttons_frame(self, frame):
            buttons_frame = ttk.Frame(frame)
            ttk.Button(buttons_frame, text='Anuluj', command=self.cancel).pack(side=RIGHT)
            ttk.Button(buttons_frame, text='Ok', command=self.ok).pack(side=RIGHT)
            return buttons_frame
