from datetime import date
from datetime import datetime
from pony.orm import *


class PlanerDB:

    def __init__(self, filename=':memory:', debug=False):
        self.first_run = False
        self.db = PlanerDB._open_database(filename, debug)
        self.curr_profile_id = self._init_db(self.db)

    @staticmethod
    def _define_entities(db):
        class Day(db.Entity):
            _table_ = 'days'
            id = PrimaryKey(int, column='day_id', auto=True)
            date = Required(date, column='day_date', index='date_index')
            textnotes = Set('TextNote')
            images = Set('Image')
            profile = Required('Profile')

        class TextNote(db.Entity):
            _table_ = 'text_notes'
            id = PrimaryKey(int, column='text_note_id', auto=True)
            day = Required(Day, column='note_id')
            value = Required(LongStr, column='text_note_value')
            geo_coord = Optional(Json)
            created_at = Required(datetime, default=lambda: datetime.now())
            updated_at = Required(datetime, default=lambda: datetime.now())
            deleted = Required(bool, default=False)

        class Image(db.Entity):
            _table_ = 'images'
            id = PrimaryKey(int, column='image_id', auto=True)
            day = Required(Day)
            path = Required(str, column='image_path')
            geo_coord = Optional(Json)
            created_at = Required(datetime, default=lambda: datetime.now())
            updated_at = Required(datetime, default=lambda: datetime.now())
            deleted = Required(bool, default=False)

        class Profile(db.Entity):
            _table_ = 'profiles'
            id = PrimaryKey(int, column='profile_id', auto=True)
            name = Required(str, column='profile_name')
            days = Set(Day)
            language = Required('Language', default=1)
            config = Optional('Config')

        class Language(db.Entity):
            id = PrimaryKey(int, auto=True)
            eng_name = Required(str)
            native_name = Optional(str)
            profiles = Set(Profile)

        class Config(db.Entity):
            id = PrimaryKey(int, auto=True)
            profile = Required(Profile)

    @staticmethod
    def _open_database(filename=':memory:', debug=False):
        db = Database()
        PlanerDB._define_entities(db)
        set_sql_debug(debug)
        db.bind(provider='sqlite', filename=filename, create_db=True)
        db.generate_mapping(create_tables=True)
        return db

    @db_session
    def _init_db(self, db) -> int:
        """
        Init database (make default profile if needed).
        :return: Id of default profile.
        """
        langs = select(l for l in db.Language)
        if langs.count() == 0:
            db.Language(eng_name="english", native_name="english")
            db.Language(eng_name="polish", native_name="polski")
            db.commit()
            self.first_run = True

        profiles = select(u.id for u in db.Profile)
        if profiles.count() == 0:
            u = db.Profile(name='Default profile')
            commit()
            db.Config(id=1, profile=u)
            return u.id

        return db.Config[1].profile.id

    @db_session
    def _get_day(self, day_date: date):
        return self.db.Day.get(date=day_date, profile=self.db.Profile[self.curr_profile_id])

    @db_session
    def _get_textnotes(self, day_date: date):
        return self.db.TextNote.select(lambda j: (j.day == self._get_day(day_date)) and (j.deleted is False))

    @db_session
    def _get_images(self, day_date: date):
        return self.db.Image.select(lambda j: (j.day == self._get_day(day_date)) and (j.deleted is False))

    @db_session
    def add_textnote(self, day_date: date, note: str) -> int:
        """
        Adding new textnote to day.
        :return: id of added textnote
        :param day_date: selected day
        :param note: text to add
        """
        n = self._get_day(day_date)
        if n is None:
            n = self.db.Day(date=day_date, profile=self.db.Profile[self.curr_profile_id])
        i = self.db.TextNote(value=note, day=n)
        commit()
        return i.id

    @db_session
    def get_notes(self, day_date: date):
        """
        Returns textnotes associated with date. (generator)
        :param day_date: selected day
        :return: TextNote (readonly values)
        """
        for i in self._get_textnotes(day_date):
            _, _, _ = i.id, i.value, i.geo_coord  # for writing to cache
            yield i

    @db_session
    def has_textnotes(self, day_date: date) -> bool:
        """
        Checks if selected date has any textnote.
        :param day_date: selected day
        :return: bool
        """
        if self._get_day(day_date) is None or len(self._get_textnotes(day_date)) == 0:
            return False
        return True

    @db_session
    def count_textnotes(self, day_date: date) -> int:
        """
        Count textnotes attached to selected date.
        :param day_date: selected day
        :return: int
        """
        return len(self._get_textnotes(day_date))

    @db_session
    def update_textnote(self, tx_id: int, value: str = None, geo_coord: Json = None) -> None:
        """
        Update value and/or geo coordinates of Textnote.
        :param tx_id: id of textnote
        :param value: text to update (None means no value changes)
        :param geo_coord: json (None means no value changes)
        """
        n = self.db.TextNote[tx_id]
        if n.deleted:
            return
        updated = False
        if value is not None:
            n.value = value
            updated = True
        if geo_coord is not None:
            n.geo_coord = geo_coord
            updated = True
        if updated:
            n.updated_at = datetime.now()

    @db_session
    def delete_textnote(self, tx_id: int) -> None:
        """
        Delete selected textnote.
        :param tx_id: id of textnote
        """
        if not self.db.TextNote[tx_id].deleted:
            self.db.TextNote[tx_id].deleted = True
            self.db.TextNote[tx_id].updated_at = datetime.now()

    @db_session
    def add_image(self, day_date: date, path: str) -> int:
        """
        Adding new image path to given date.
        :param day_date:
        :param path: Path to image file (relative to app images folder).
        :return: id of added image
        """
        n = self._get_day(day_date)
        if n is None:
            n = self.db.Day(date=day_date, profile=self.db.Profile[self.curr_profile_id])
        i = self.db.Image(path=path, day=n)
        commit()
        return i.id

    @db_session
    def get_images(self, day_date: date):
        """
        Returns Images associated with date. (readonly values)  (generator)
        :param day_date: selected date
        :return: Image (readonly values)
         """
        for i in self._get_images(day_date):
            _, _, _ = i.id, i.path, i.geo_coord  # for writing to cache
            yield i

    @db_session
    def get_image(self, image_id: int):
        """
        Returns Image associated with id. (readonly values)
        :param image_id: id of image
        :return: Image (readonly values)
         """
        i = self.db.Image[image_id]
        _, _, _ = i.id, i.path, i.geo_coord  # for writing to cache
        return i

    @db_session
    def has_images(self, day_date: date) -> bool:
        """
        Checks wheter selected date has any image.
        :param day_date: selected day
        :return: bool
        """
        if self._get_day(day_date) is None or len(self._get_images(day_date)) == 0:
            return False
        return True

    @db_session
    def count_images(self, day_date: date) -> int:
        """
        Count images attached to selected date.
        :param day_date: selected day
        :return: int
        """
        return len(self._get_images(day_date))

    @db_session
    def update_image(self, im_id: int, path: str = None, geo_coord: Json = None) -> None:
        """
        Update path and/or geo coordinates of Image.
        :param im_id: id of image.
        :param path: Path to image file (relative to app images folder) (None means no value changes)
        :param geo_coord: json (None means no change value)
        """
        n = self.db.Image[im_id]
        if n.deleted:
            return
        updated = False
        if path is not None:
            n.path = path
            updated = True
        if geo_coord is not None:
            n.geo_coord = geo_coord
            updated = True
        if updated:
            n.updated_at = datetime.now()

    @db_session
    def delete_image(self, im_id: int) -> None:
        """
        Delete image's data from db.
        :param im_id: id of image to delete
        """
        if not self.db.Image[im_id].deleted:
            self.db.Image[im_id].deleted = True
            self.db.Image[im_id].updated_at = datetime.now()

    @db_session
    def make_profile(self, name: str) -> int:
        """
        Make new profile.
        :param name: Name of profile.
        :return: id of new profile.
        """
        u = self.db.Profile(name=name)
        commit()
        return u.id

    @db_session
    def update_profile(self, profile_id: int, name: str = None) -> int:
        """
        Change name of profile.
        :param profile_id: Id of profile.
        :param name: New name. (None means no changes)
        :return: Id of changed profile.
        """
        u = self.db.Profile[profile_id]
        if name is not None:
            u.name = name
        commit()
        return u.id

    @db_session
    def set_curr_profile(self, profile_id: int) -> int:
        """
        Sets the current profile.
        :param profile_id: Id of profile.
        :return: Id of previous profile.
        """
        u = self.db.Profile[profile_id]
        tmp = self.curr_profile_id

        self.curr_profile_id = u.id
        self.db.Config[1].profile = u

        return tmp

    def get_curr_profile(self) -> int:
        """
        Returns id of currently selected profile.
        :return: id of profile.
        """
        return self.curr_profile_id

    @db_session
    def get_curr_profile_name(self) -> str:
        """
        Returns the name of the currently selected profile.
        :return: Name of profile.
        """
        u = self.db.Profile[self.get_curr_profile()]
        return u.name

    @db_session
    def get_all_profiles(self):
        """
        Returns all profiles. (generator)
        :return: dict{'id': int, 'name': str}
         """
        for i in select(u for u in self.db.Profile):
            yield {'id': i.id, 'name': i.name}

    @db_session
    def get_language(self) -> int:
        """
        Returns id of currently selected language.
        :return: id of language.
        """
        u = self.db.Profile[self.get_curr_profile()]
        return u.language.id

    @db_session
    def set_language(self, lang_id: int) -> int:
        """
        Sets the current language.
        :param lang_id: Id of language.
        :return: Id of previous language.
        """
        old_l = self.get_language()
        self.db.Profile[self.get_curr_profile()].language = self.db.Language[lang_id]
        return old_l

    @db_session
    def get_all_languages(self):
        """
        Returns all languages. (generator)
        :return: dict{'id': int, 'eng_name': str, 'native_name': str}
         """
        langs = select(l for l in self.db.Language)
        for l in langs:
            yield {'id': l.id, 'eng_name': l.eng_name, 'native_name': l.native_name}

    def is_first_run(self) -> bool:
        """
        Returns true for first run (with new database).
        """
        return self.first_run
