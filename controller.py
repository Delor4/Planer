import datetime
import models
import calendar
import os
import shutil
from PIL import Image
from pathlib import Path


class Calendar:
    def __init__(self, _=None):
        d = datetime.date.today()
        self.date = datetime.date(d.year, d.month, 1)
        self.T = self.translate
        # self.db = models.PlanerDB() # db in memory
        self.create_folder(self.get_data_folder())
        self.db = models.PlanerDB(os.path.join(self.get_data_folder(), 'notes.sqlite'))
        self.db.add_hook("on_after_delete_image", lambda data: self.after_db_delete_image(data))

    def after_db_delete_image(self, data):
        self.delete_image_files(data['path'], data['day']['profile']['id'])
        return True

    def prev_month(self):  # ustawienie poprzedniego miesiąca
        d = self.date - datetime.timedelta(28)
        self.date = datetime.date(d.year, d.month, 1)

    def next_month(self):  # ustawienie następnego miesiąca
        d = self.date + datetime.timedelta(31)
        self.date = datetime.date(d.year, d.month, 1)

    def _make_date(self, day):
        return datetime.date(self.date.year, self.date.month, day)

    def get_data_string(self, day):
        return '{:%Y-%m-%d}'.format(self._make_date(day))

    def get_day_data(self, day):
        notes = []
        for i in self.db.get_notes(self._make_date(day)):
            notes.append(i)
        images = []
        for i in self.db.get_images(self._make_date(day)):
            images.append(i)
        return notes, images

    def get_month_data(self):
        row = 0
        for day in calendar.Calendar().itermonthdays2(self.date.year, self.date.month):
            if day[0] > 0:
                yield {'day_of_month': day[0],
                       'week_of_month': row,
                       'day_of_week': day[1],
                       'notes_count': self.db.count_textnotes(self._make_date(day[0])),
                       'images_count': self.db.count_images(self._make_date(day[0]))
                       }
            if day[1] == 6:
                row += 1

    def get_month(self):
        return self.date.month

    def get_year(self):
        return self.date.year

    def add_textnote(self, day, note):
        return self.db.add_textnote(self._make_date(day), note)

    def get_textnotes(self, day):
        return self.db.get_notes(self._make_date(day))

    def update_textnote(self, id, value=None, geo_cord=None):
        self.db.update_textnote(id, value, geo_cord)

    def delete_textnote(self, id):
        self.db.delete_textnote(id)

    def update_image(self, id, path, geo_cord):
        self.db.update_image(id, path, geo_cord)

    def delete_image(self, id):
        self.db.delete_image(id)

    def get_image(self, image_id):
        return self.db.get_image(image_id)

    def delete_image_files(self, file_path, profile_id):
        # TODO: tu kasowanie plików (obraz główny i thumb) powiązanych z rekordem image_id
        return

    def add_image(self, day, source_path):
        path_to_image = self.get_curr_images_folder()
        self.create_folder(path_to_image)
        ext = self.get_extension(source_path)
        id = self.db.add_image(self._make_date(day), path_to_image)
        filename = self.make_new_name(id, ext)
        shutil.copy(source_path, os.path.join(path_to_image, filename))
        self.db.update_image(id, path=filename)
        thumbnail = self.make_thumbnail(os.path.join(path_to_image, filename), filename)
        return id

    def get_images_folder(self, profile_id):
        return os.path.join(self.get_data_folder(), str(profile_id))

    def get_curr_images_folder(self):
        return self.get_images_folder(self.db.get_curr_profile())

    def get_data_folder(self):  # TODO sprawdzenie czy __file__ zawsze zwraca sciezke
        return os.path.join(os.path.abspath(os.path.dirname(__file__)), "data")

    def get_extension(self, source_path):
        old_name, extension = os.path.splitext(source_path)
        return extension

    def make_new_name(self, id, ext):
        return "img_" + str(id) + ext

    def create_folder(self, path):
        if not os.path.exists(path):
            parent_path = Path(path).parent
            self.create_folder(parent_path)
            os.mkdir(path)

    def thumbnail_from_filename(self, filename):
        return "t_" + filename

    def make_thumbnail(self, path, filename):
        image = Image.open(path)
        image.thumbnail((200, 120), Image.ANTIALIAS)
        image.save(os.path.join(self.get_curr_images_folder(), self.thumbnail_from_filename(filename)))

    def get_no_image_image(self):
        return Image.open(os.path.join(self.get_data_folder(), 'no_image.jpg'))

    def make_profile(self, name):
        return self.db.make_profile(name)

    def update_profile(self, id, name):
        return self.db.update_profile(id, name)

    def set_current_profile(self, id):
        return self.db.set_curr_profile(id)

    def get_all_profiles(self):
        return self.db.get_all_profiles()

    def get_curr_profile(self):
        return self.db.get_curr_profile()

    def get_profile_name(self, p_id):
        return self.db.get_profile_name(p_id)

    def get_curr_profile_name(self):
        return self.db.get_curr_profile_name()

    def delete_profile(self, p_id):
        return self.db.delete_profile(p_id)

    def get_language(self):
        return self.db.get_language()

    def set_language(self, l_id):
        return self.db.set_language(l_id)

    def get_all_languages(self):
        return self.db.get_all_languages()

    def translate(self, tag):
        # TODO: zwraca tekst przypisany do taga
        # TODO: język tekstu: self.(db.)get_language()
        print("To translate:", tag)
        return "{" + tag + "}"
