from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from PIL import ImageTk, Image
import os


class DayDialog:
    def __init__(self, app, day: int):
        self.top = Toplevel(app.mainWindow)
        self.top.transient(app.mainWindow)
        self.top.grab_set()
        self.dialog = DayDialog.DayFrame(self, day, app)

    class DayFrame:
        def __init__(self, parent, day: int, app):
            self.state = app.state
            self.day = day
            self.window = parent.top
            self.parent = parent

            self.notes_data = []
            self.images_data = []

            self.notes_frame = None
            self.images_frame = None

            self.no_notes = None
            self.no_images = None
            self.init_ui()

        def ok(self):
            for n in self.notes_data:
                text = n['text_widget'].get("1.0", 'end-1c')
                if text != n['old_value']:
                    self.state.update_textnote(n['id'], text)
            self.parent.top.destroy()

        # def cancel(self):
        #    self.parent.top.destroy()

        def create_new_note(self):
            txt = "Nowa notatka."
            txt_id = self.state.add_textnote(self.day, txt)
            self.make_frame_note(self.notes_frame, {'id': txt_id, 'value': txt})

        def create_new_image(self):
            filename = filedialog.askopenfilename(initialdir=".", title="Select file",
                                                  filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))
            if os.path.isfile(filename):
                img_id = self.state.add_image(self.day, filename)
                im = self.state.get_image(img_id)
                self.make_frame_image(self.images_frame, im)

        def init_ui(self):
            notes, images = self.state.get_day_data(self.day)
            frame = ttk.Frame(self.window)
            frame.pack(fill=BOTH)

            self.notes_frame = self.make_all_notes_frame(frame, notes)
            self.images_frame = self.make_images_frame(frame, images)
            buttons_frame = self.make_buttons_frame(frame)

            buttons_frame.pack(side=BOTTOM, anchor=E)
            self.notes_frame.pack(side=LEFT, fill=BOTH, padx=2, pady=2)
            self.images_frame.pack(side=LEFT, fill=BOTH, padx=2, pady=2)

        def make_frame_note(self, frame, note_data):
            if self.no_notes is not None:
                self.no_notes.pack_forget()
                self.no_notes.destroy()
                self.no_notes = None
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
            if self.no_images is not None:
                self.no_images.pack_forget()
                self.no_images.destroy()
                self.no_images = None
            i_frame = ttk.Frame(frame)
            img = ImageTk.PhotoImage(
                Image.open(os.path.join(self.state.get_images_folder(), 't_' + image_data['path'])))
            canvas = Canvas(i_frame, width=img.width(), height=img.height())
            canvas.pack()
            canvas.create_image(0, 0, anchor=NW, image=img)
            i_frame.pack()
            canvas.bind("<Button-1>", lambda event, d=image_data: self.on_image_click(event, d))
            self.images_data.append({'img': img})

        def make_all_notes_frame(self, frame, notes):
            notes_frame = ttk.LabelFrame(frame, text="Notatki")
            notes_wrapper = ttk.LabelFrame(notes_frame, text="Wraper")
            if len(notes) == 0:
                self.no_notes = ttk.Label(notes_wrapper, text="Brak notatek.")
                self.no_notes.pack()
            for n in notes:
                self.make_frame_note(notes_wrapper, n)
            notes_wrapper.pack()
            notes_frame_bottom = ttk.LabelFrame(notes_frame, text="Bottom")
            ttk.Button(notes_frame_bottom, text="↲", command=self.create_new_note).pack(side=RIGHT)
            ttk.Entry(notes_frame_bottom).pack(fill=X)
            notes_frame_bottom.pack(fill=X)
            return notes_frame

        def make_images_frame(self, frame, images):
            images_frame = ttk.LabelFrame(frame, text="Obrazy")
            ttk.Button(images_frame, text="+", command=self.create_new_image).pack()

            if len(images) == 0:
                self.no_images = ttk.Label(images_frame, text="Brak obrazów.")
                self.no_images.pack()

            for i in images:
                self.make_frame_image(images_frame, i)
            return images_frame

        def make_buttons_frame(self, frame):
            buttons_frame = ttk.Frame(frame)
            # ttk.Button(buttons_frame, text='Anuluj', command=self.cancel).pack(side=RIGHT)
            ttk.Button(buttons_frame, text='Ok', command=self.ok).pack(side=RIGHT)
            return buttons_frame

        def on_image_click(self, _, image_data):
            self.show_image_viewer(image_data)

        def show_image_viewer(self, image_data):
            d = DayDialog.ImageViewerDialog(self.parent, image_data['path'])
            self.parent.top.wait_window(d.top)

    class ImageViewerDialog:
        def __init__(self, parent, image_path):
            self.top = Toplevel(parent.top)
            self.top.transient(parent.top)
            self.top.grab_set()
            self.parent = parent
            self.image_path = image_path
            self.state = self.parent.dialog.state
            self.img = None
            self.init_ui()

        def init_ui(self):
            self.img = ImageTk.PhotoImage(Image.open(os.path.join(self.state.get_images_folder(), self.image_path)))
            canvas = Canvas(self.top, width=self.img.width(), height=self.img.height())
            canvas.pack()
            canvas.create_image(0, 0, anchor=NW, image=self.img)
