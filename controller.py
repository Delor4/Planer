import datetime

import models
import calendar
import os
import shutil
from PIL import Image
from pathlib import Path
import csv


class Calendar:
    no_image: Image = None

    def __init__(self, _=None):
        d = datetime.date.today()
        self.date = datetime.date(d.year, d.month, 1)  # always set to first day of month
        self.db = self._setup_db()
        self.T = self.translate
        self.translations = self._read_translations()

    # DATABASE
    def _setup_db(self) -> models.PlanerDB:
        self.create_folder(self.get_data_folder())
        # db = models.PlanerDB()  # db in memory
        db = models.PlanerDB(os.path.join(self.get_data_folder(), 'notes.sqlite'))
        db.add_hook("on_after_delete_image", lambda data: self._after_db_delete_image(data))
        return db

    def _after_db_delete_image(self, hook_data: dict) -> bool:
        self._delete_image_files(hook_data['path'], hook_data['day']['profile']['id'])
        return True

    # TRANSLATE
    def _read_translations(self) -> dict:
        # read file
        csvfile = open(os.path.join(self.get_resources_folder(), 'translations.csv'), encoding="utf-8")
        # parse file
        translations = {}
        reader = csv.reader(csvfile, delimiter=';')
        for row in reader:
            translations[row[0]] = row[1:]

        return translations

    def translate(self, tag: str) -> str:
        if tag in self.translations:
            return self.translations[tag][self.get_language() - 1]
        print("To translate:", tag)
        return "{" + tag + "}"

    # DATE
    def _make_date(self, day: int) -> datetime.date:
        return datetime.date(self.date.year, self.date.month, day)

    def get_month(self) -> int:
        return self.date.month

    def get_year(self) -> int:
        return self.date.year

    def prev_month(self) -> None:  # ustawienie poprzedniego miesiąca
        d = self.date - datetime.timedelta(28)
        self.date = datetime.date(d.year, d.month, 1)

    def next_month(self) -> None:  # ustawienie następnego miesiąca
        d = self.date + datetime.timedelta(31)
        self.date = datetime.date(d.year, d.month, 1)

    def get_data_string(self, day: int) -> str:
        return '{:%Y-%m-%d}'.format(self._make_date(day))

    # ALL DATA
    def get_month_data(self):  # generator
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

    # TEXTNOTE
    def add_textnote(self, day: int, note: str):
        return self.db.add_textnote(self._make_date(day), note)

    def get_textnotes(self, day: int):
        return self.db.get_notes(self._make_date(day))

    def update_textnote(self, tid: int, value: str = None, geo_cord=None):
        self.db.update_textnote(tid, value, geo_cord)

    def delete_textnote(self, tid: int):
        self.db.delete_textnote(tid)

    # IMAGE
    def update_image(self, tid: int, path: str = None, geo_cord=None):
        self.db.update_image(tid, path, geo_cord)

    def delete_image(self, tid: int):
        self.db.delete_image(tid)

    def get_image(self, image_id: int):
        return self.db.get_image(image_id)

    def get_images(self, day):
        return self.db.get_images(self._make_date(day))

    def _delete_image_files(self, file_path: str, profile_id: int):
        img_folder = self.get_images_folder(profile_id)
        os.remove(os.path.join(img_folder, file_path))
        os.remove(os.path.join(img_folder, self._make_thumbnail_from_filename(file_path)))

    def add_image(self, day: int, source_path: str):
        path_to_image = self.get_curr_images_folder()
        self.create_folder(path_to_image)
        im_id = self.db.add_image(self._make_date(day), path_to_image)
        filename = self._make_image_name(im_id, self._get_extension(source_path))
        self.update_image(im_id, path=filename)
        shutil.copy(source_path, os.path.join(path_to_image, filename))
        self._make_thumbnail(os.path.join(path_to_image, filename), filename, self.get_curr_profile())
        return im_id

    def get_images_folder(self, profile_id: int):
        return os.path.join(self.get_data_folder(), str(profile_id))

    def get_curr_images_folder(self):
        return self.get_images_folder(self.db.get_curr_profile())

    def get_data_folder(self):
        return os.path.join(os.path.abspath(os.path.dirname(__file__)),
                            # TODO sprawdzić czy __file__ zawsze zwraca sciezke
                            "data")

    def get_resources_folder(self):
        return os.path.join(os.path.abspath(os.path.dirname(__file__)),
                            # TODO sprawdzić czy __file__ zawsze zwraca sciezke
                            "resources")

    def _get_extension(self, source_path: str):
        _, extension = os.path.splitext(source_path)
        return extension

    def _make_image_name(self, im_id: int, ext: str):
        return "img_" + str(im_id) + ext

    def _make_thumbnail_from_filename(self, filename: str):
        return "t_" + filename

    def create_folder(self, path: str):
        if not os.path.exists(path):
            parent_path = Path(path).parent
            self.create_folder(parent_path)
            os.mkdir(path)

    def _make_thumbnail(self, path: str, filename: str, profile_id: int):
        image = Image.open(path)
        image.thumbnail((200, 120), Image.ANTIALIAS)
        image.save(os.path.join(self.get_images_folder(profile_id), self._make_thumbnail_from_filename(filename)))

    def get_no_image(self) -> Image:
        if self.no_image is None:
            self.no_image = Image.open(os.path.join(self.get_resources_folder(), 'no_image.jpg'))
        return self.no_image

    # PROFILE
    def make_profile(self, name: str):
        return self.db.make_profile(name)

    def update_profile(self, pid: int, name: str):
        return self.db.update_profile(pid, name)

    def set_current_profile(self, pid: int):
        return self.db.set_curr_profile(pid)

    def get_all_profiles(self):
        return self.db.get_all_profiles()

    def get_curr_profile(self):
        return self.db.get_curr_profile()

    def get_profile_name(self, p_id: int):
        return self.db.get_profile_name(p_id)

    def get_curr_profile_name(self):
        return self.db.get_curr_profile_name()

    def delete_profile(self, p_id: int):
        return self.db.delete_profile(p_id)

    # LANGUAGE
    def get_language(self):
        return self.db.get_language()

    def set_language(self, l_id: int):
        return self.db.set_language(l_id)

    def get_all_languages(self):
        return self.db.get_all_languages()
