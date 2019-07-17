import calendar

cal = calendar.Calendar()
row = 0
for day in cal.itermonthdays2(2016, 1):
    if day[0] > 0:
        print("col:{0}, row:{1}".format(day[1], row))
    if day[1] == 6:
        row += 1

print(
    '\n'.join(
        ["SKS Team:",
         "Brodziak Sebastian",
         "Jaśkowski Krzysztof",
         "Kucharczyk Sebastian"
         ]
    )
)
