from datetime import date
from pony.orm import *

db = Database()


class Note(db.Entity):
    _table_ = 'note'
    id = PrimaryKey(int, column='note_id', auto=True)
    date = Required(date, column='note_date', index='date_index')
    textnotes = Set('TextNote')
    images = Set('Image')


class TextNote(db.Entity):
    _table_ = 'text_note'
    id = PrimaryKey(int, column='text_note_id', auto=True)
    note = Required(Note, column='note_id')
    value = Required(LongStr, column='text_note_value')
    geo_coord = Optional(Json)


class Image(db.Entity):
    _table_ = 'image'
    id = PrimaryKey(int, column='image_id', auto=True)
    note = Required(Note)
    path = Required(str, column='image_path')
    geo_coord = Optional(Json)


@db_session
def add_textnote(day_date, note):
    """ Adding new text note to date. """
    n = Note.get(date=day_date)
    if n is None:
        n = Note(date=day_date)
    TextNote(value=note, note=n)


@db_session
def get_notes(day_date):
    """ Returns textnotes associated with date. (readonly values) (generator) """
    n = Note.get(date=day_date)
    for i in TextNote.select(lambda i: i.note == n):
        _, _, _ = i.id, i.value, i.geo_coord  # for writing to cache
        yield i


@db_session
def has_textnotes(day_date):
    n = Note.get(date=day_date)
    if n is None or len(n.textnotes) == 0:
        return False
    return True


@db_session
def update_textnote(id, value=None, geo_coord=None):
    """ Update value and/or geo coordinates of Textnote. """
    n = TextNote[id]
    if value is not None:
        n.value = value
    if geo_coord is not None:
        n.geo_coord = geo_coord

@db_session
def delete_textnote(id):
    TextNote[id].delete()

@db_session
def add_image(day_date, path):
    """ Adding new image path to given date. """
    n = Note.get(date=day_date)
    if n is None:
        n = Note(date=day_date)
    Image(path=path, note=n)


@db_session
def get_images(day_date):
    """ Returns Images associated with date. (readonly values)  (generator) """
    n = Note.get(date=day_date)
    for i in Image.select(lambda i: i.note == n):
        _, _, _ = i.id, i.path, i.geo_coord  # for writing to cache
        yield i


@db_session
def has_images(day_date):
    n = Note.get(date=day_date)
    if n is None or len(n.images) == 0:
        return False
    return True


@db_session
def update_image(id, path=None, geo_coord=None):
    """ Update path and/or geo coordinates of Image. """
    n = Image[id]
    if path is not None:
        n.path = path
    if geo_coord is not None:
        n.geo_coord = geo_coord


@db_session
def delete_image(id):
    Image[id].delete()


# set_sql_debug(True)

db.bind(provider='sqlite', filename=':memory:')
# db.bind(provider='sqlite', filename='notes.sqlite', create_db=True)

db.generate_mapping(create_tables=True)
