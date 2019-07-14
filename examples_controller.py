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


# c.prev_month()
# print(c.date)

def test_list():
    a = []
    a.append({'a': "ff"})
    a.append({'a': "gg"})
    a.append({'a': "hh"})
    return a


c.db.add_textnote(datetime.date(c.date.year, c.date.month, 5), "gfgfg")

for t in c.get_month_data():
    print(t)

print("ooo")
for t in c.get_month_data_g():
    print(t)

no, im = c.get_day_data(5)

print(no,im)
