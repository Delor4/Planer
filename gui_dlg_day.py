from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from PIL import ImageTk, Image
import os

import gui_dlg_imageviewer


class DayDialog:
    def __init__(self, app, day: int):
        self.top = Toplevel(app.mainWindow)
        self.top.transient(app.mainWindow)
        self.top.grab_set()
        self.T = app.state.translate
        self.state = app.state
        app.set_icon(self.top)
        self.top.title("Planer - {}".format(self.state.get_data_string(day)))
        self.dialog = DayDialog.DayFrame(self, day, app)

    class DayFrame:
        def __init__(self, parent, day: int, app):
            self.state = app.state
            self.day = day
            self.window = parent.top
            self.parent = parent
            self.T = parent.T

            self.notes_data = []
            self.images_data = []

            self.notes_frame = None
            self.images_frame = None
            self.buttons_frame = None
            self.notes_bottom = None

            self.no_notes = None
            self.no_images = None

            self.entry_text = StringVar()
            self.initial_dir = '.'

            self.init_ui()

        def ok(self):
            for n in self.notes_data:
                text = n['text_widget'].get("1.0", 'end-1c')
                if text != n['old_value']:
                    self.state.update_textnote(n['id'], text)
            self.parent.top.destroy()

        # def cancel(self):
        #    self.parent.top.destroy()

        def create_new_note(self, txt):
            txt_id = self.state.add_textnote(self.day, txt)
            self.make_frame_note(self.notes_frame, {'id': txt_id, 'value': txt})

        def create_new_image(self):
            print(self.initial_dir)
            filename = filedialog.askopenfilename(initialdir=self.initial_dir, title=self.T("select_file"), filetypes=
            ((self.T("jpeg files"), "*.jpg"), (self.T("all_files"), "*.*")))
            if os.path.isfile(filename):
                img_id = self.state.add_image(self.day, filename)
                im = self.state.get_image(img_id)
                self.make_frame_image(self.images_frame, im)
                self.initial_dir = os.path.dirname(filename)

        def init_ui(self):
            notes, images = self.state.get_day_data(self.day)
            frame = ttk.Frame(self.window)
            frame.pack(fill=BOTH)

            self.notes_frame = self.make_all_notes_frame(frame, notes)
            self.images_frame = self.make_images_frame(frame, images)
            self.buttons_frame = self.make_buttons_frame(frame)

            self.repack()

        def repack(self):
            self.buttons_frame.pack(side=BOTTOM, anchor=E)
            self.notes_frame.pack(side=LEFT, fill=BOTH, padx=2, pady=2)
            self.images_frame.pack(side=LEFT, fill=BOTH, padx=2, pady=2)

        def remove_note(self, n_id):
            for note in self.notes_data:
                if note['id'] == n_id:
                    self.state.delete_textnote(n_id)
                    note['frame'].pack_forget()
                    note['frame'].destroy()
                    self.notes_data.remove(note)
                    self.repack()
                    break

        def remove_image(self, i_id, frame):
            self.state.delete_image(i_id)
            frame.pack_forget()
            frame.destroy()
            self.repack()

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
            close_button = Button(f, text='x', command=lambda id=note_data['id']: self.remove_note(id))
            close_button.place(relx=1, x=-18, y=-3, anchor=NE)
            self.notes_data.append(
                {'id': note_data['id'], 'old_value': note_data['value'], 'text_widget': tn, 'frame': f})

        def make_frame_image(self, frame, image_data):
            if self.no_images is not None:
                self.no_images.pack_forget()
                self.no_images.destroy()
                self.no_images = None
            i_frame = ttk.Frame(frame)
            img = ImageTk.PhotoImage(
                Image.open(os.path.join(self.state.get_images_folder(),
                                        self.state.thumbnail_from_filename(image_data['path']))))
            canvas = Canvas(i_frame, width=img.width(), height=img.height())
            canvas.pack()
            canvas.create_image(0, 0, anchor=NW, image=img)
            i_frame.pack()
            close_button = Button(i_frame, text='x',
                                  command=lambda id=image_data['id'], fr=i_frame: self.remove_image(id, fr))
            close_button.place(relx=1, x=-3, y=-3, anchor=NE)
            canvas.bind("<Button-1>", lambda event, d=image_data: self.on_image_click(event, d))
            self.images_data.append({'img': img})

        def make_all_notes_frame(self, frame, notes):
            notes_frame = ttk.LabelFrame(frame, text=self.T("notes").capitalize())
            notes_wrapper = ttk.Frame(notes_frame)
            if len(notes) == 0:
                self.no_notes = ttk.Label(notes_wrapper, text=self.T("no_notes"))  # Brak notatek.
                self.no_notes.pack()
            for n in notes:
                self.make_frame_note(notes_wrapper, n)
            notes_wrapper.pack()

            self.create_notes_bottom(notes_frame)

            return notes_frame

        def create_notes_bottom(self, frame):
            self.notes_bottom = ttk.Frame(frame)
            ttk.Button(self.notes_bottom, text="↲", command=self.on_new_note).pack(side=RIGHT)

            e = ttk.Entry(self.notes_bottom, textvariable=self.entry_text)
            e.pack(fill=X)
            e.bind('<Return>', lambda event: self.on_new_note())

            self.notes_bottom.pack(fill=X)

        def on_new_note(self):
            if self.entry_text.get() == "":
                return
            self.create_new_note(self.entry_text.get())
            self.entry_text.set("")
            self.notes_bottom.pack_forget()
            self.notes_bottom.destroy()
            self.create_notes_bottom(self.notes_frame)
            self.repack()

        def make_images_frame(self, frame, images):
            images_frame = ttk.LabelFrame(frame, text=self.T("images").capitalize())
            ttk.Button(images_frame, text="+", command=self.create_new_image).pack()

            if len(images) == 0:
                self.no_images = ttk.Label(images_frame, text=self.T("no_images"))  # Brak obrazów.
                self.no_images.pack()

            for i in images:
                self.make_frame_image(images_frame, i)
            return images_frame

        def make_buttons_frame(self, frame):
            buttons_frame = ttk.Frame(frame)
            # ttk.Button(buttons_frame, text=self.T('cancel'), command=self.cancel).pack(side=RIGHT)
            ttk.Button(buttons_frame, text=self.T('ok'), command=self.ok).pack(side=RIGHT)
            return buttons_frame

        def on_image_click(self, _, image_data):
            self.show_image_viewer(image_data)

        def show_image_viewer(self, image_data):
            d = gui_dlg_imageviewer.ImageViewerDialog(self.parent, image_data['path'])
            self.parent.top.wait_window(d.top)


