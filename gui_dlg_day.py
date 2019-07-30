from tkinter import *
#from tkinter import ttk
from tkinter import filedialog
from PIL import ImageTk, Image
import os

import gui_dlg_imageviewer
import gui_base_dialog


class DayDialog(gui_base_dialog.PlanerBaseModalDialog):
    def __init__(self, parent, day: int):
        gui_base_dialog.PlanerBaseModalDialog.__init__(self, parent)
        self.set_title(self.state.get_data_string(day))

        self.day = day

        self.notes_data = []
        self.images_data = []

        self.notes_frame = None
        self.images_frame = None
        self.buttons_frame = None
        self.notes_bottom = None

        self.no_notes = None
        self.no_images = None

        self.entry_text = StringVar()

        self._init_ui()

    def _init_ui(self):
        notes = self.state.get_textnotes(self.day)
        images = self.state.get_images(self.day)
        frame = ttk.Frame(self.top)
        frame.pack(fill=BOTH)

        self.notes_frame = self.create_notes_frame(frame, notes)
        self.images_frame = self.create_images_frame(frame, images)
        self.buttons_frame = self.create_buttons_frame(frame)

        self.repack()

    def repack(self):
        self.buttons_frame.pack(side=BOTTOM, anchor=E)
        self.notes_frame.pack(side=LEFT, fill=BOTH, padx=2, pady=2)
        self.images_frame.pack(side=LEFT, fill=BOTH, padx=2, pady=2)

    # Main frames
    def create_notes_frame(self, frame, notes):
        notes_frame = LabelFrame(frame, text=self.T("notes").capitalize())
        self.create_notes_top(notes_frame, notes)
        self.create_notes_bottom(notes_frame)
        return notes_frame

    def create_images_frame(self, frame, images):
        images_frame = LabelFrame(frame, text=self.T("images").capitalize())
        Button(images_frame, text="+", command=self.on_new_image).pack()

        added = False
        for i in images:
            self.make_frame_image(images_frame, i)
            added = True

        if not added:
            self.no_images = Label(images_frame, text=self.T("no_images"))  # Brak obrazów.
            self.no_images.pack()
        return images_frame

    def create_buttons_frame(self, frame):
        buttons_frame = Frame(frame)
        Button(buttons_frame, text=self.T('ok'), command=self.on_ok).pack(side=RIGHT, padx=5, pady=5)
        return buttons_frame

    # Notes frame
    def create_notes_top(self, frame, notes):
        notes_wrapper = Frame(frame)
        added = False
        for n in notes:
            self.make_frame_note(notes_wrapper, n)
            added = True
        if not added:
            self.no_notes = Label(notes_wrapper, text=self.T("no_notes"))  # Brak notatek.
            self.no_notes.pack()
        notes_wrapper.pack()

    def create_notes_bottom(self, frame):
        self.notes_bottom = Frame(frame)
        Button(self.notes_bottom, text="+", command=self.on_new_note).pack(side=RIGHT)

        e = Entry(self.notes_bottom, textvariable=self.entry_text)
        e.pack(fill=X)
        e.bind('<Return>', lambda event: self.on_new_note())

        self.notes_bottom.pack(fill=X)

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
        close_button = Button(f, text='x', command=lambda nid=note_data['id']: self.on_remove_note(nid))
        close_button.place(relx=1, x=-18, y=-3, anchor=NE)
        self.notes_data.append(
            {'id': note_data['id'], 'old_value': note_data['value'], 'text_widget': tn, 'frame': f})

    # Images frame
    def make_frame_image(self, frame, image_data):
        if self.no_images is not None:
            self.no_images.pack_forget()
            self.no_images.destroy()
            self.no_images = None

        i_frame = Frame(frame)
        try:
            img = ImageTk.PhotoImage(
                Image.open(os.path.join(self.state.get_curr_images_folder(),
                                        self.state._make_thumbnail_from_filename(image_data['path']))))
        except FileNotFoundError:
            img = ImageTk.PhotoImage(self.state.get_no_image())

        canvas = Canvas(i_frame, width=img.width(), height=img.height())
        canvas.pack()
        canvas.create_image(0, 0, anchor=NW, image=img)

        i_frame.pack()

        close_button = Button(i_frame, text='x',
                              command=lambda im_id=image_data['id'], fr=i_frame: self.on_remove_image(im_id, fr))
        close_button.place(relx=1, x=-3, y=-3, anchor=NE)
        canvas.bind("<Button-1>", lambda event, d=image_data: self.on_image_click(event, d))

        self.images_data.append({'img': img})

    # Event handlers
    def on_ok(self):
        for n in self.notes_data:
            text = n['text_widget'].get("1.0", 'end-1c')
            if text != n['old_value']:
                self.state.update_textnote(n['id'], text)
        self.close_window()

    def on_new_note(self):
        if self.entry_text.get() == "":
            return
        self.create_new_note(self.entry_text.get())
        self.entry_text.set("")
        self.notes_bottom.pack_forget()
        self.notes_bottom.destroy()
        self.create_notes_bottom(self.notes_frame)
        self.repack()

    def on_remove_note(self, n_id):
        for note in self.notes_data:
            if note['id'] == n_id:
                self.state.delete_textnote(n_id)
                note['frame'].pack_forget()
                note['frame'].destroy()
                self.notes_data.remove(note)
                self.repack()
                break

    def on_new_image(self):
        filename = filedialog.askopenfilename(initialdir=self.app.initial_dir,
                                              title=self.T("select_file_title"),
                                              filetypes=(
                                                         (self.T("image_files"), "*.jpg"),
                                                         (self.T("image_files"), "*.jpeg"),
                                                         (self.T("image_files"), "*.png"),
                                                         (self.T("image_files"), "*.bmp"),
                                                         (self.T("image_files"), "*.gif"),
                                                         (self.T("jpeg_files"), "*.jpg"),
                                                         (self.T("all_files"), "*.*")))
        if os.path.isfile(filename):
            img_id = self.state.add_image(self.day, filename)
            im = self.state.get_image(img_id)
            self.make_frame_image(self.images_frame, im)
            self.app.initial_dir = os.path.dirname(filename)

    def on_remove_image(self, i_id, frame):
        self.state.delete_image(i_id)
        frame.pack_forget()
        frame.destroy()
        self.repack()

    def on_image_click(self, _, image_data):
        self.show_image_viewer(image_data)

    # Helper methods
    def show_image_viewer(self, image_data):
        d = gui_dlg_imageviewer.ImageViewerDialog(self, image_data['path'])
        self.top.wait_window(d.top)

    def create_new_note(self, txt):
        txt_id = self.state.add_textnote(self.day, txt)
        self.make_frame_note(self.notes_frame, {'id': txt_id, 'value': txt})
