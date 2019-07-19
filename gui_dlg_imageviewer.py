import os
from tkinter import *

from PIL import ImageTk, Image

from gui import PlanerApp


class ImageViewerDialog:
    def __init__(self, parent, image_path):
        self.top = Toplevel(parent.top)
        self.top.transient(parent.top)
        self.top.grab_set()

        self.T = parent.T

        PlanerApp.set_icon(self.top)
        self.top.title("{0} - {1}".format(PlanerApp.app_name, self.T("imageview_title")))  # ImageView
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
