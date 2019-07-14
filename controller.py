import datetime
import models
import calendar


class Calendar:
    def __init__(self, _=None):
        d = datetime.date.today()
        self.date = datetime.date(d.year, d.month, 1)
        self.db = models.PlanerDB()

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
                 'values': i.value,
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

    def get_day_data2(self, day):
        self.day_selected = day
        self.month_selected = self.month
        self.year_selected = self.year
        for i in self.db.get_notes(self.date.year, self.month_selected, self.day_selected):
            print("test" + i.id + i.values)

    def get_month_data_(self):
        ret = []
        cal = calendar.Calendar()
        # row = 0
        for day in cal.itermonthdays2(self.date.year, self.date.month):
            if day[0] > 0:
                b = {'day_of_month': day[0],
                     # 'week_of_month': row,
                     'day_of_week': day[1],
                     'notes_count': self.db.count_textnotes(self._make_date(day[0])),
                     'images_count': self.db.count_images(self._make_date(day[0]))
                     }
                ret.append(b)
            # if day[1] == 6:
            #    row += 1
        return ret

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
