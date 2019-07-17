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
        # self.db = models.PlanerDB() # db in memory
        self.create_folder(self.get_data_folder())
        self.db = models.PlanerDB(os.path.join(self.get_data_folder(), 'notes.sqlite'))

    def prev_month(self):  # ustawienie poprzedniego miesiąca
        d = self.date - datetime.timedelta(28)
        self.date = datetime.date(d.year, d.month, 1)

    def next_month(self):  # ustawienie następnego miesiąca
        d = self.date + datetime.timedelta(31)
        self.date = datetime.date(d.year, d.month, 1)

    def _make_date(self, day):
        return datetime.date(self.date.year, self.date.month, day)

    def get_day_data(self, day):
        notes = []
        for i in self.db.get_notes(self._make_date(day)):
            notes.append(
                {'id': i.id,
                 'value': i.value,
                 'geo_coord': i.geo_coord
                 }
            )
        images = []
        for i in self.db.get_images(self._make_date(day)):
            images.append(
                {'id': i.id,
                 'path': i.path,
                 'geo_coord': i.geo_coord
                 }
            )
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

    def get_month_data_mock(self):
        return [
            {'day_of_month': 1, 'week_of_month': 0, 'day_of_week': 4, 'notes_count': 0, 'images_count': 0},
            {'day_of_month': 2, 'week_of_month': 0, 'day_of_week': 5, 'notes_count': 1, 'images_count': 1},
            {'day_of_month': 3, 'week_of_month': 0, 'day_of_week': 6, 'notes_count': 0, 'images_count': 0},
            {'day_of_month': 4, 'week_of_month': 1, 'day_of_week': 0, 'notes_count': 0, 'images_count': 5},
            {'day_of_month': 5, 'week_of_month': 1, 'day_of_week': 1, 'notes_count': 1, 'images_count': 0},
            {'day_of_month': 6, 'week_of_month': 1, 'day_of_week': 2, 'notes_count': 0, 'images_count': 0},
            {'day_of_month': 7, 'week_of_month': 1, 'day_of_week': 3, 'notes_count': 0, 'images_count': 1},
            {'day_of_month': 8, 'week_of_month': 1, 'day_of_week': 4, 'notes_count': 0, 'images_count': 0},
            {'day_of_month': 9, 'week_of_month': 1, 'day_of_week': 5, 'notes_count': 6, 'images_count': 2},
            {'day_of_month': 10, 'week_of_month': 1, 'day_of_week': 6, 'notes_count': 0, 'images_count': 0},
            {'day_of_month': 11, 'week_of_month': 2, 'day_of_week': 0, 'notes_count': 0, 'images_count': 0},
            {'day_of_month': 12, 'week_of_month': 2, 'day_of_week': 1, 'notes_count': 9, 'images_count': 3},
            {'day_of_month': 13, 'week_of_month': 2, 'day_of_week': 2, 'notes_count': 0, 'images_count': 0},
            {'day_of_month': 14, 'week_of_month': 2, 'day_of_week': 3, 'notes_count': 0, 'images_count': 15},
            {'day_of_month': 15, 'week_of_month': 2, 'day_of_week': 4, 'notes_count': 2, 'images_count': 0},
            {'day_of_month': 16, 'week_of_month': 2, 'day_of_week': 5, 'notes_count': 0, 'images_count': 0},
            {'day_of_month': 17, 'week_of_month': 2, 'day_of_week': 6, 'notes_count': 32, 'images_count': 0},
            {'day_of_month': 18, 'week_of_month': 3, 'day_of_week': 0, 'notes_count': 0, 'images_count': 0},
            {'day_of_month': 19, 'week_of_month': 3, 'day_of_week': 1, 'notes_count': 0, 'images_count': 0},
            {'day_of_month': 20, 'week_of_month': 3, 'day_of_week': 2, 'notes_count': 0, 'images_count': 0},
            {'day_of_month': 21, 'week_of_month': 3, 'day_of_week': 3, 'notes_count': 0, 'images_count': 0},
            {'day_of_month': 22, 'week_of_month': 3, 'day_of_week': 4, 'notes_count': 87, 'images_count': 54},
            {'day_of_month': 23, 'week_of_month': 3, 'day_of_week': 5, 'notes_count': 0, 'images_count': 0},
            {'day_of_month': 24, 'week_of_month': 3, 'day_of_week': 6, 'notes_count': 0, 'images_count': 0},
            {'day_of_month': 25, 'week_of_month': 4, 'day_of_week': 0, 'notes_count': 4, 'images_count': 0},
            {'day_of_month': 26, 'week_of_month': 4, 'day_of_week': 1, 'notes_count': 0, 'images_count': 0},
            {'day_of_month': 27, 'week_of_month': 4, 'day_of_week': 2, 'notes_count': 0, 'images_count': 0},
            {'day_of_month': 28, 'week_of_month': 4, 'day_of_week': 3, 'notes_count': 0, 'images_count': 0}
        ]

    def get_day_data_mock(self, _):
        return [
                   {'id': 1, 'value': 'Lorem ipsum dolor sit amet ...', 'geo_coord': {}},
                   {'id': 2,
                    'value': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Proin nibh augue, suscipit a, scelerisque sed, lacinia in, mi.',
                    'geo_coord': {}},
                   {'id': 3,
                    'value': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Proin nibh augue, suscipit a, scelerisque sed, lacinia in, mi. Cras vel lorem. Etiam pellentesque aliquet tellus. Phasellus pharetra nulla ac diam. Quisque semper justo at risus. Donec venenatis, turpis vel hendrerit interdum, dui ligula ultricies purus, sed posuere libero dui id orci. Nam congue, pede vitae dapibus aliquet, elit magna vulputate arcu, vel tempus metus leo non est. Etiam sit amet lectus quis est congue mollis. Phasellus congue lacus eget neque. Phasellus ornare, ante vitae consectetuer consequat, purus sapien ultricies dolor, et mollis pede metus eget nisi. Praesent sodales velit quis augue. Cras suscipit, urna at aliquam rhoncus, urna quam viverra nisi, in interdum massa nibh nec erat.',
                    'geo_coord': {}}
               ], [
                   {'id': 1, 'path': 'image1.jpg', 'geo_coord': {}},
                   {'id': 2, 'path': 'image2.jpg', 'geo_coord': {}},
                   {'id': 3, 'path': 'image3.jpg', 'geo_coord': {}}
               ]

    def add_textnote(self, day, note):
        return self.db.add_textnote(self._make_date(day), note)

    def update_textnote(self, id, value=None, geo_cord=None):
        self.db.update_textnote(id, value, geo_cord)

    def delete_textnote(self, id):
        self.db.delete_textnote(id)

    def update_image(self, id, path, geo_cord):
        self.db.update_image(id, path, geo_cord)

    def delete_image(self, id):
        self.db.delete_image(id)

    def get_image(self, image_id):
        i = self.db.get_image(image_id)
        return {'id': i.id,
                'path': i.path,
                'geo_cord': i.geo_coord
                }

    def add_image(self, day, source_path):
        path_to_image = self.get_images_folder()
        self.create_folder(path_to_image)
        ext = self.get_extension(source_path)
        id = self.db.add_image(self._make_date(day), path_to_image)
        filename = self.make_new_name(id, ext)
        shutil.copy(source_path, os.path.join(path_to_image, filename))
        self.db.update_image(id, path=filename)
        thumbnail = self.make_thumbnail(os.path.join(path_to_image, filename), filename)
        return id

    def get_images_folder(self):
        return os.path.join(self.get_data_folder(), str(self.db.get_curr_profile()))

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

    def make_thumbnail(self, path, filename):
        image = Image.open(path)
        image.thumbnail((200, 120), Image.ANTIALIAS)
        image.save(os.path.join(self.get_images_folder(), "t_" + filename))
