import os
from tkinter import *

from PIL import ImageTk, Image

import gui_base_dialog


class ImageViewerDialog(gui_base_dialog.PlanerBaseModalDialog):
    def __init__(self, parent, image_path):
        gui_base_dialog.PlanerBaseModalDialog.__init__(self, parent)
        self.set_title(self.T("imageview_title"))  # ImageView

        self.image_path = image_path
        self.img = None

        self.init_ui()

    def init_ui(self):
        try:
            self.img = ImageTk.PhotoImage(Image.open(os.path.join(self.state.get_curr_images_folder(), self.image_path)))
        except FileNotFoundError:
            self.img = ImageTk.PhotoImage(self.state.get_no_image())

        canvas = Canvas(self.top, width=self.img.width(), height=self.img.height())
        canvas.pack()
        canvas.create_image(0, 0, anchor=NW, image=self.img)
