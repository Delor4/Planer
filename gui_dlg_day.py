from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import os


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
            self.images_data = []

            self.notes_frame = None
            self.initUI()

        def ok(self):
            for n in self.notes_data:
                text = n['text_widget'].get("1.0", 'end-1c')
                if text != n['old_value']:
                    self.state.update_textnote(n['id'], text)
            self.parent.top.destroy()

        def cancel(self):
            self.parent.top.destroy()

        def create_new_note(self):
            txt = "Nowa notatka."
            id = self.state.add_textnote(self.day, txt)
            self.make_frame_note(self.notes_frame, {'id': id, 'value': txt})

        def create_new_image(self):
            filename = filedialog.askopenfilename(initialdir=".", title="Select file",
                                                  filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))
            if os.path.isfile(filename):
                id = self.state.add_image(filename)
                im = self.state.get_image(id)
                self.make_frame_image(self.images_frame, {'id': im.id,
                                                          'path': im.path,
                                                          'geo_coord': im.geo_coord
                                                          })

        def initUI(self):
            notes, images = self.state.get_day_data(self.day)
            frame = ttk.Frame(self.window)
            frame.pack(fill=BOTH)

            self.notes_frame = self.make_notes_frame(frame, notes)
            self.images_frame = self.make_images_frame(frame, images)
            buttons_frame = self.make_buttons_frame(frame)

            buttons_frame.pack(side=BOTTOM, anchor=E)
            self.notes_frame.pack(side=LEFT, fill=BOTH, padx=2, pady=2)
            self.images_frame.pack(side=LEFT, fill=BOTH, padx=2, pady=2)

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

        def make_frame_image(self, frame, image_data):
            ttk.Label(frame, text=image_data['path']).pack()

        def make_notes_frame(self, frame, notes):
            notes_frame = ttk.LabelFrame(frame, text="Notatki")
            ttk.Button(notes_frame, text="+", command=self.create_new_note).pack()
            if len(notes) == 0:
                ttk.Label(notes_frame, text="Brak notatek.").pack()
            for n in notes:
                self.make_frame_note(notes_frame, n)
            return notes_frame

        def make_images_frame(self, frame, images):
            images_frame = ttk.LabelFrame(frame, text="Obrazy")
            ttk.Button(images_frame, text="+", command=self.create_new_image).pack()

            if len(images) == 0:
                ttk.Label(images_frame, text="Brak obrazów.").pack()
            for i in images:
                self.make_frame_image(images_frame, i)
            return images_frame

        def make_buttons_frame(self, frame):
            buttons_frame = ttk.Frame(frame)
            ttk.Button(buttons_frame, text='Anuluj', command=self.cancel).pack(side=RIGHT)
            ttk.Button(buttons_frame, text='Ok', command=self.ok).pack(side=RIGHT)
            return buttons_frame
