import controller
import datetime

c = controller.Calendar()

print(c.date)
c.next_month()
c.next_month()
c.next_month()
print(c.date)
c.get_day_data(2)
c.prev_month()
print(c.date)

c.prev_month()
print(c.date)
c.prev_month()
print(c.date)
c.prev_month()
print(c.date)
c.prev_month()
print(c.date)
c.prev_month()
print(c.date)
c.prev_month()
print(c.date)
c.prev_month()
print(c.date)

def test_list():
    a = []
    a.append({'a': "ff"})
    a.append({'a': "gg"})
    a.append({'a': "hh"})
    return a


c.db.add_textnote(datetime.date(c.date.year, c.date.month, 5), "Lorem ipsum dolor sit amet ...")
c.db.add_textnote(datetime.date(c.date.year, c.date.month, 5), "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Proin nibh augue, suscipit a, scelerisque sed, lacinia in, mi.")
c.db.add_textnote(datetime.date(c.date.year, c.date.month, 5), "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Proin nibh augue, suscipit a, scelerisque sed, lacinia in, mi. Cras vel lorem. Etiam pellentesque aliquet tellus. Phasellus pharetra nulla ac diam. Quisque semper justo at risus. Donec venenatis, turpis vel hendrerit interdum, dui ligula ultricies purus, sed posuere libero dui id orci. Nam congue, pede vitae dapibus aliquet, elit magna vulputate arcu, vel tempus metus leo non est. Etiam sit amet lectus quis est congue mollis. Phasellus congue lacus eget neque. Phasellus ornare, ante vitae consectetuer consequat, purus sapien ultricies dolor, et mollis pede metus eget nisi. Praesent sodales velit quis augue. Cras suscipit, urna at aliquam rhoncus, urna quam viverra nisi, in interdum massa nibh nec erat.")
c.db.add_image(datetime.date(c.date.year, c.date.month, 5), "image1.jpg")
c.db.add_image(datetime.date(c.date.year, c.date.month, 5), "image2.jpg")
c.db.add_image(datetime.date(c.date.year, c.date.month, 5), "image3.jpg")
for t in c.get_month_data_mock():
    print(t)

print("ooo")
for t in c.get_month_data():
    print(t)

no, im = c.get_day_data(5)

print(no,im)
