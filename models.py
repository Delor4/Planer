import typing
from datetime import date
from datetime import datetime
from pony.orm import *


class PlanerDB:

    def __init__(self, filename=':memory:', debug=False):
        self.first_run = False
        self.db = PlanerDB._open_database(filename, debug)
        self.curr_profile_id = self._init_db(self.db)
        self.hooks = self._init_hooks()

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
            _table_ = 'languages'
            id = PrimaryKey(int, auto=True)
            eng_name = Required(str)
            native_name = Optional(str)
            profiles = Set(Profile)

        class Config(db.Entity):
            _table_ = 'config'
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

    def _init_hooks(self):
        return {
            'on_before_create_image': [],
            'on_after_create_image': [],
            'on_before_update_image': [],
            'on_after_update_image': [],
            'on_before_delete_image': [],
            'on_after_delete_image': [],

            'on_before_delete_textnote': [],
            'on_after_delete_textnote': [],
            'on_before_delete_profile': [],
            'on_after_delete_profile': [],
        }

    def add_hook(self, hook_id: str, func: typing.Callable[[dict], bool]) -> bool:
        """
        Registering new hook.
        :param hook_id: name of hook
        :param func: Function to register.
                    Type: func(hook_data: dict) -> bool.
                    Returning False meaning not calling the next queue hooks.
        :return: True if hook registered.
        """
        if hook_id in self.hooks:
            self.hooks[hook_id].append(func)
            return True
        else:
            raise ValueError('Unknown hook.')
        return False

    def remove_hook(self, hook_id: str, func: typing.Callable[[dict], bool]) -> bool:
        """
        Remove registered hook.
        :param hook_id: name of hook
        :param func: registered func
        :return: True if hook removed.
        """
        if hook_id in self.hooks:
            self.hooks[hook_id].remove(func)
            return True
        else:
            raise ValueError('Unknown hook.')
        return False

    def _call_hook(self, hook_id: str, data: dict):
        data['hook'] = hook_id
        for func in self.hooks[hook_id]:
            if not func(data):
                return

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
    def _textnote_to_dict(self, tn):
        return {'id': tn.id, 'value': tn.value, 'geo_coord': tn.geo_coord, 'day': self._day_to_dict(tn.day)}

    @db_session
    def _image_to_dict(self, im):
        return {'id': im.id, 'path': im.path, 'geo_coord': im.geo_coord, 'day': self._day_to_dict(im.day)}

    @db_session
    def _day_to_dict(self, day):
        return {'id': day.id, 'date': day.date, 'profile': self._profile_to_dict(day.profile)}

    @db_session
    def _profile_to_dict(self, pr):
        return {'id': pr.id, 'name': pr.name, 'language': self._language_to_dict(pr.language)}

    @db_session
    def _language_to_dict(self, lng):
        return {'id': lng.id, 'eng_name': lng.eng_name, 'native_name': lng.native_name}

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
        :param day_date: selected date
        :return: dict{'id': int, 'value': str, 'geo_coord': Json}
        """
        for i in self._get_textnotes(day_date):
            yield self._textnote_to_dict(i)

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
        tn = self.db.TextNote[tx_id]
        if not tn.deleted:
            self._call_hook("on_before_delete_textnote", self._textnote_to_dict(tn))
            tmp = self._textnote_to_dict(tn)
            tn.deleted = True
            tn.updated_at = datetime.now()
            self._call_hook("on_after_delete_textnote", tmp)

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
            self._call_hook("on_before_create_image",
                            {'date': day_date, 'profile': self.db.Profile[self.curr_profile_id], 'path': path})
            n = self.db.Day(date=day_date, profile=self.db.Profile[self.curr_profile_id])
        i = self.db.Image(path=path, day=n)
        commit()
        self._call_hook("on_after_create_image", self._image_to_dict(i))

        return i.id

    @db_session
    def get_images(self, day_date: date):
        """
        Returns Images associated with date. (readonly values)  (generator)
        :param day_date: selected date
        :return: Image (readonly values)
         """
        for i in self._get_images(day_date):
            yield self._image_to_dict(i)

    @db_session
    def get_image(self, image_id: int):
        """
        Returns Image associated with id. (readonly values)
        :param image_id: id of image
        :return: Image (readonly values)
         """
        i = self.db.Image[image_id]
        return self._image_to_dict(i)

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
        self._call_hook("on_before_update_image", self._image_to_dict(n))
        if path is not None:
            n.path = path
            updated = True
        if geo_coord is not None:
            n.geo_coord = geo_coord
            updated = True
        if updated:
            n.updated_at = datetime.now()
        self._call_hook("on_after_update_image", self._image_to_dict(n))

    @db_session
    def delete_image(self, im_id: int) -> None:
        """
        Delete image's data from db.
        :param im_id: id of image to delete
        """
        im = self.db.Image[im_id]
        if not im.deleted:
            self._call_hook("on_before_delete_image", self._image_to_dict(im))
            tmp = self._image_to_dict(im)
            im.deleted = True
            im.updated_at = datetime.now()
            self._call_hook("on_after_delete_image", tmp)

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
    def get_profile_name(self, profile_id) -> str:
        """
        Returns the name of the selected profile.
        :return: Name of profile.
        """
        u = self.db.Profile[profile_id]
        return u.name

    @db_session
    def get_curr_profile_name(self) -> str:
        """
        Returns the name of the currently selected profile.
        :return: Name of profile.
        """
        return self.get_profile_name(self.get_curr_profile())

    @db_session
    def get_all_profiles(self):
        """
        Returns all profiles. (generator)
        :return: dict{'id': int, 'name': str}
         """
        for i in select(u for u in self.db.Profile):
            yield self._profile_to_dict(i)

    @db_session
    def delete_profile(self, p_id: int) -> None:
        """
        Delete p_id profile.
            Currently selected profile can't be deleted.
        """
        if p_id != self.get_curr_profile():
            pr = self.db.Profile[p_id]
            self._call_hook("on_before_delete_profile", self._profile_to_dict(pr))
            tmp = self._profile_to_dict(pr)
            # removing all days data
            for d in self.db.Day.select(lambda j: j.profile == pr):
                # removing textnotes
                for t in d.textnotes:
                    self.delete_textnote(t.id)
                # removing images
                for i in d.images:
                    self.delete_image(i.id)

            # removing all images
            self.db.Profile[p_id].delete()
            self._call_hook("on_after_delete_profile", tmp)

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
            yield self._language_to_dict(l)

    def is_first_run(self) -> bool:
        """
        Returns true for first run (with new database).
        """
        return self.first_run
