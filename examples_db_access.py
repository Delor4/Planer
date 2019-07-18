import models
import datetime

print("********************")
# db = models.PlanerDB('notes.sqlite') # db in file
db = models.PlanerDB()  # db in memory

dat = datetime.datetime(2014, 5, 9)

# adding some data to DB
db.add_image(dat, "/fff/tt/image.jpeg")
img = db.add_image(dat, "/fff/tt/image2.jpeg")
db.add_textnote(dat, "test note")
db.add_textnote(dat, "test note2")
note = db.add_textnote(dat, "test note3")
db.add_textnote(dat, "test note4")

print("Dodane notki:")
for i in db.get_notes(dat):
    print(i.id, '"' + i.value + '"', i.geo_coord)
    print("    ", i.day.id, i.day.date)

print("Dodane obrazy:")
for i in db.get_images(dat):
    print(i.id, i.path, i.geo_coord)
    print("    ", i.day.id, i.day.date)

# update values in textnotes
for i in db.get_notes(dat):
    db.update_textnote(i.id, value=i.value + " dopisek")

# update values in images
for i in db.get_images(dat):
    gc = i.geo_coord.copy()  # shallow copy because it's read only values
    gc['latitude'] = 'unknown'
    gc['longitude'] = 'unknown'
    db.update_image(i.id, geo_coord=gc)

print("Zmienione notki:")
for i in db.get_notes(dat):
    print(i.id, '"' + i.value + '"')

print("Zmienione obrazy:")
for i in db.get_images(dat):
    print(i.id, i.path, i.geo_coord)

print("Pod datą " + str(dat) + " są obrazy?:", db.has_images(dat))
dat2 = datetime.datetime(2003, 5, 6)
print("Pod datą " + str(dat2) + " są obrazy?:", db.has_images(dat2))

pr = db.make_profile("Nowy profil")
old = db.set_curr_profile(pr)

db.add_textnote(dat, "test note in another profile")

print("Notki profilu '{0}':".format(db.get_curr_profile_name()))
for i in db.get_notes(dat):
    print(i.id, '"' + i.value + '"', i.geo_coord)
    print("    ", i.day.id, i.day.date)

db.set_curr_profile(old)

print("Profil przed zmianą nazwy '{0}'".format(db.get_curr_profile_name()))
db.update_profile(old, "Stary profil")
print("Profil po zmianie nazwy '{0}'".format(db.get_curr_profile_name()))

print("Notki w profilu '{0}':".format(db.get_curr_profile_name()))
for i in db.get_notes(dat):
    print(i.id, '"' + i.value + '"', i.geo_coord)

db.delete_textnote(note)
print("Notki po usunięciu id '{0}':".format(note))
for i in db.get_notes(dat):
    print(i.id, '"' + i.value + '"', i.geo_coord)

db.delete_image(img)
print("Obrazy po usunięciu id '{0}':".format(img))
for i in db.get_images(dat):
    print(i.id, i.path, i.geo_coord)

print("Lista profili:")
for i in db.get_all_profiles():
    print(i.id, i.name)

print("Lista języków:")
for l in db.get_all_languages():
    print(l['id'], l['eng_name'], l['native_name'])

print("Aktulny język: {}".format(db.get_language()))

db.set_language(2)
print("Język po zmianie: {}".format(db.get_language()))
