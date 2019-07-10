import models
import datetime


print("********************")

dat = datetime.datetime(2014, 5, 9)
# adding some data to DB
models.add_image(dat, "/fff/tt/image.jpeg")
models.add_image(dat, "/fff/tt/image2.jpeg")
models.add_textnote(dat, "test note")
models.add_textnote(dat, "test note2")
models.add_textnote(dat, "test note3")
models.add_textnote(dat, "test note4")

print("Added textnotes:")
for i in models.get_notes(dat):
    print(i.id, '"' + i.value + '"', i.geo_coord)
    print("    ", i.note.id, i.note.date)

print("Added images:")
for i in models.get_images(dat):
    print(i.id, i.path, i.geo_coord)
    print("    ", i.note.id, i.note.date)

# update values in textnotes
for i in models.get_notes(dat):
    models.update_textnote(i.id, value=i.value+" dopisek")

print("Changed textnotes:")
for i in models.get_notes(dat):
    print(i.id, '"' + i.value + '"')

print("Date " + str(dat) + " has images:", models.has_images(dat))
dat2 = datetime.datetime(2003, 5, 6)
print("Date " + str(dat2) + " has images:", models.has_images(dat2))

