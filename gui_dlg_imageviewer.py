import os
from tkinter import *

from PIL import ImageTk, Image

from gui_base_dialog import PlanerBaseDialog


class ImageViewerDialog(PlanerBaseDialog):
    def __init__(self, parent, image_path):
        PlanerBaseDialog.__init__(self, parent)
        self.set_title(self.T("imageview_title"))  # ImageView

        self.image_path = image_path
        self.img = None

        self.init_ui()

    def init_ui(self):
        self.img = ImageTk.PhotoImage(Image.open(os.path.join(self.state.get_images_folder(), self.image_path)))
        canvas = Canvas(self.top, width=self.img.width(), height=self.img.height())
        canvas.pack()
        canvas.create_image(0, 0, anchor=NW, image=self.img)
