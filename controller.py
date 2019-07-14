import calendar
import datetime
import models

db = models.PlanerDB()


class Calendar:
    def __init__(self, parent):

        self.parent = parent
        self.cal = calendar.Calendar
        self.day_selected = datetime.date.today().day
        self.year = datetime.date.today().year
        self.month = datetime.date.today().month
        self.month_selected = self.month
        self.year_selected = self.year
        self.refresh(self.year, self.month)

    def prev_month(self):  # ustawienie poprzedniego miesiąca
        if self.month > 1:
            self.month -= 1
        else:
            self.month = 12
            self.month -= 1

            self.refresh(self.year, self.month)

    def next_month(self):  # ustawienie następnego miesiąca
        if self.month < 12:
            self.month += 1
        else:
            self.month = 1
            self.month += 1
            self.refresh(self.year, self.month)

    def get_day_data(self, day):
        self.day_selected = day
        self.month_selected = self.month
        self.year_selected = self.year
        for i in db.get_notes(self.year_selected, self.month_selected, self.day_selected):
            print("test" + i.id + i.values)

    def get_month_data(self, month):
        self.month_selected = month
        self.year_selected = self.year

    def refresh(self, y, m):
        self.year_selected = y
        self.month_selected = m
