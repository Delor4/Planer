from datetime import date
from pony.orm import *

db = Database()


class Note(db.Entity):
    _table_ = 'notes'
    id = PrimaryKey(int, column='note_id', auto=True)
    date = Required(date, column='note_date', index='date_index')
    textnotes = Set('TextNote')
    images = Set('Image')
    profile = Required('Profile')


class TextNote(db.Entity):
    _table_ = 'text_notes'
    id = PrimaryKey(int, column='text_note_id', auto=True)
    note = Required(Note, column='note_id')
    value = Required(LongStr, column='text_note_value')
    geo_coord = Optional(Json)


class Image(db.Entity):
    _table_ = 'images'
    id = PrimaryKey(int, column='image_id', auto=True)
    note = Required(Note)
    path = Required(str, column='image_path')
    geo_coord = Optional(Json)


class Profile(db.Entity):
    _table_ = 'profiles'
    id = PrimaryKey(int, column='profile_id', auto=True)
    name = Required(str, column='profile_name')
    notes = Set(Note)


@db_session
def add_textnote(day_date: date, note: str) -> None:
    """
    Adding new textnote to date.
    :param day_date: selected day
    :param note: text to add
    """
    n = Note.get(date=day_date, profile=Profile[curr_profile_id])
    if n is None:
        n = Note(date=day_date, profile=Profile[curr_profile_id])
    TextNote(value=note, note=n)


@db_session
def get_notes(day_date: date) -> TextNote:
    """
    Returns textnotes associated with date. (generator)
    :param day_date: selected day
    :return: TextNote (readonly values)
    """
    n = Note.get(date=day_date, profile=Profile[curr_profile_id])
    for i in TextNote.select(lambda j: j.note == n):
        _, _, _ = i.id, i.value, i.geo_coord  # for writing to cache
        yield i


@db_session
def has_textnotes(day_date: date) -> bool:
    """
    Checks if selected date has any textnote.
    :param day_date: selected day
    :return: bool
    """
    n = Note.get(date=day_date, profile=Profile[curr_profile_id])
    if n is None or len(n.textnotes) == 0:
        return False
    return True


@db_session
def update_textnote(tx_id: int, value: str = None, geo_coord: Json = None) -> None:
    """
    Update value and/or geo coordinates of Textnote.
    :param tx_id: id of textnote
    :param value: text to update (None means no value changes)
    :param geo_coord: json (None means no value changes)
    """
    n = TextNote[tx_id]
    if value is not None:
        n.value = value
    if geo_coord is not None:
        n.geo_coord = geo_coord


@db_session
def delete_textnote(tx_id: int) -> None:
    """
    Delete selected textnote.
    :param tx_id: id of textnote
    """
    TextNote[tx_id].delete()


@db_session
def add_image(day_date: date, path: str) -> None:
    """
    Adding new image path to given date.
    :param day_date:
    :param path: Path to image file (relative to app images folder).
    """
    n = Note.get(date=day_date, profile=Profile[curr_profile_id])
    if n is None:
        n = Note(date=day_date, profile=Profile[curr_profile_id])
    Image(path=path, note=n)


@db_session
def get_images(day_date: date) -> Image:
    """
    Returns Images associated with date. (readonly values)  (generator)
    :param day_date: selected date
    :return: Image (readonly values)
     """
    n = Note.get(date=day_date, profile=Profile[curr_profile_id])
    for i in Image.select(lambda j: j.note == n):
        _, _, _ = i.id, i.path, i.geo_coord  # for writing to cache
        yield i


@db_session
def has_images(day_date: date) -> bool:
    """
    Checks wheter selected date has any image.
    :param day_date: selected day
    :return: bool
    """
    n = Note.get(date=day_date, profile=Profile[curr_profile_id])
    if n is None or len(n.images) == 0:
        return False
    return True


@db_session
def update_image(im_id: int, path: str = None, geo_coord: Json = None) -> None:
    """
    Update path and/or geo coordinates of Image.
    :param im_id: id of image.
    :param path: Path to image file (relative to app images folder) (None means no value changes)
    :param geo_coord: json (None means no change value)
    """
    n = Image[im_id]
    if path is not None:
        n.path = path
    if geo_coord is not None:
        n.geo_coord = geo_coord


@db_session
def delete_image(im_id: int) -> None:
    """
    Delete image.
    :param im_id: id of image to delete
    """
    Image[im_id].delete()


@db_session
def init_db() -> int:
    """
    Init database.
    :return: Id of default profile.
    """
    profiles = select(u.id for u in Profile)
    if profiles.count() == 0:
        u = Profile(name='Default profile')
        commit()
        return u.id
    for i in profiles:
        return i


@db_session
def make_profile(name: str) -> int:
    """
    Make new profile.
    :param name: Name of profile.
    :return: id of new profile.
    """
    u = Profile(name=name)
    commit()
    return u.id


@db_session
def update_profile(profile_id: int, name: str = None) -> int:
    """
    Change name of profile.
    :param profile_id: Id of profile.
    :param name: New name. (None means no changes)
    :return: Id of changed profile.
    """
    u = Profile[profile_id]
    if name is not None:
        u.name = name
    commit()
    return u.id


@db_session
def set_curr_profile(profile_id: int) -> int:
    """
    Sets the current profile.
    :param profile_id: Id of profile.
    :return: Id of previous profile.
    """
    u = Profile[profile_id]
    global curr_profile_id
    tmp = curr_profile_id
    curr_profile_id = u.id
    return tmp


def get_curr_profile() -> int:
    """
    Returns currently selected profile.
    :return: id of profile.
    """
    return curr_profile_id


@db_session
def get_curr_profile_name() -> str:
    """
    Returns currently selected profile's name.
    :return: Name of profile.
    """
    u = Profile[get_curr_profile()]
    return u.name


# set_sql_debug(True)


db.bind(provider='sqlite', filename=':memory:')
# db.bind(provider='sqlite', filename='notes.sqlite', create_db=True)

db.generate_mapping(create_tables=True)

curr_profile_id = init_db()
