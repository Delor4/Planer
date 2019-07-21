import datetime
import models
import calendar
import os
import shutil
from PIL import Image
from pathlib import Path
import csv


class Calendar:
    def __init__(self, _=None):
        d = datetime.date.today()
        self.date = datetime.date(d.year, d.month, 1)  # always set to first day of month
        self.db = self.setup_db()
        self.T = self.translate
        self.translations = self.read_translations()

    def after_db_delete_image(self, hook_data):
        self.delete_image_files(hook_data['path'], hook_data['day']['profile']['id'])
        return True

    def setup_db(self):
        self.create_folder(self.get_data_folder())
        # db = models.PlanerDB()  # db in memory
        db = models.PlanerDB(os.path.join(self.get_data_folder(), 'notes.sqlite'))
        db.add_hook("on_after_delete_image", lambda data: self.after_db_delete_image(data))
        return db

    def read_translations(self):
        # read file
        file = []
        with open(os.path.join(self.get_data_folder(), 'translations.csv')) as csvfile:
            for line in csvfile:
                file.append(line.encode('windows-1250').decode('utf-8'))
        # parse file
        translations = {}
        reader = csv.reader(file, delimiter=';')
        for row in reader:
            translations[row[0]] = row[1:]

        return translations

    # date operations
    def _make_date(self, day):
        return datetime.date(self.date.year, self.date.month, day)

    def get_month(self):
        return self.date.month

    def get_year(self):
        return self.date.year

    def prev_month(self):  # ustawienie poprzedniego miesiąca
        d = self.date - datetime.timedelta(28)
        self.date = datetime.date(d.year, d.month, 1)

    def next_month(self):  # ustawienie następnego miesiąca
        d = self.date + datetime.timedelta(31)
        self.date = datetime.date(d.year, d.month, 1)

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

    def add_textnote(self, day, note):
        return self.db.add_textnote(self._make_date(day), note)

    def get_textnotes(self, day):
        return self.db.get_notes(self._make_date(day))

    def update_textnote(self, tid, value=None, geo_cord=None):
        self.db.update_textnote(tid, value, geo_cord)

    def delete_textnote(self, tid):
        self.db.delete_textnote(tid)

    def update_image(self, tid, path=None, geo_cord=None):
        self.db.update_image(tid, path, geo_cord)

    def delete_image(self, tid):
        self.db.delete_image(tid)

    def get_image(self, image_id):
        return self.db.get_image(image_id)

    def delete_image_files(self, file_path, profile_id):
        img_folder = self.get_images_folder(profile_id)
        os.remove(os.path.join(img_folder, file_path))
        os.remove(os.path.join(img_folder, self.thumbnail_from_filename(file_path)))

    def add_image(self, day, source_path):
        path_to_image = self.get_curr_images_folder()
        self.create_folder(path_to_image)
        im_id = self.db.add_image(self._make_date(day), path_to_image)
        filename = self.make_new_name(im_id, self.get_extension(source_path))
        self.update_image(im_id, path=filename)
        shutil.copy(source_path, os.path.join(path_to_image, filename))
        self.make_thumbnail(os.path.join(path_to_image, filename), filename)
        return im_id

    def get_images_folder(self, profile_id):
        return os.path.join(self.get_data_folder(), str(profile_id))

    def get_curr_images_folder(self):
        return self.get_images_folder(self.db.get_curr_profile())

    def get_data_folder(self):  # TODO sprawdzenie czy __file__ zawsze zwraca sciezke
        return os.path.join(os.path.abspath(os.path.dirname(__file__)), "data")

    def get_extension(self, source_path):
        _, extension = os.path.splitext(source_path)
        return extension

    def make_new_name(self, im_id, ext):
        return "img_" + str(im_id) + ext

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

    def update_profile(self, pid, name):
        return self.db.update_profile(pid, name)

    def set_current_profile(self, pid):
        return self.db.set_curr_profile(pid)

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
        if tag in self.translations:
            return self.translations[tag][self.get_language() - 1]
        print("To translate:", tag)
        return "{" + tag + "}"
