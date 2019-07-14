from tkinter import *
from tkinter import messagebox
import calendar
import datetime

# creating main window
mainWindow = Tk()

# frames
topMainFrame = Frame(mainWindow, width=1100, height=50)
# leftMainFrame = Frame(mainWindow, width=1, height=700, bg="red")
# rightMainFrame = Frame(mainWindow, width=1, height=700, bg="red")
bottomMainFrame = Frame(mainWindow)

bottomMainFrame.pack(side = BOTTOM)
topMainFrame.pack(side = TOP)

# menu options
class PlanerMenu:
    def prevMonth(self):
        print("cofaj")
        self.month -= 1

    def nextMonth(self):
        print("naprzod")
        self.month += 4

    def about(self):
        self.messagebox.showinfo("O nas", "SKS Team:\nBrodziak Sebastian\nJaśkowski Krzysztof\nKucharczyk Sebastian")

class Day:
    def __init__(self):
        self.day = 0
        print("Dzień tygodnia")

    def openDay(self):
        messagebox.showinfo("Dzień X", "To jest okno przykładowe")

dayObject = Day()

#---------MAIN MENU---------
mainMenu = Menu(mainWindow) # Menu method from Tkinter
mainWindow.config(menu = mainMenu)

subMenu = Menu(mainMenu)
mainMenu.add_cascade(label = "Plik", menu = subMenu)
subMenu.add_cascade(label = "Nowy")
subMenu.add_cascade(label = "Zapisz")
subMenu.add_cascade(label = "Wczytaj")
subMenu.add_separator()
subMenu.add_cascade(label = "Zamknij")

helpMenu = Menu(mainMenu)
mainMenu.add_cascade(label = "Pomoc", menu = helpMenu)
helpMenu.add_command(label = "O nas", command = PlanerMenu.about) # added showinfo window

#---------LAYOUT---------
# calendar
# main
cal = calendar.Calendar()
row = 0

cal.year = datetime.date.today().year
cal.month = datetime.date.today().month

# adding buttons for changing date

for day in cal.itermonthdays2(cal.year, cal.month):
    if day[0] > 0:
        Label(bottomMainFrame, text='col:{0}, row:{1}'.format(day[1], row), borderwidth=50).grid(row=row, column=day[1])
    if day[1] == 6:
        row += 1

left = Button(topMainFrame, text='<', command=lambda: PlanerMenu.prevMonth(cal))
left.pack(side = LEFT)

right = Button(topMainFrame, text='>', command=lambda: PlanerMenu.nextMonth(cal))
right.pack(side = LEFT)


mainWindow.mainloop()


# topMainFrame.pack(side = TOP)
# leftMainFrame.pack(side = LEFT)
# rightMainFrame.pack(side = RIGHT)
# bottomMainFrame.pack(side = BOTTOM)

# loop for creating grid v1
# for row in range(5):
#     for column in range(7):
#        Label(mainWindow, text = 'R%s/C%s'%(row, column), borderwidth = 50).grid(row = row, column = column)

# day button
# buttonDay = Button(mainWindow, text="Dzień", command=dayObject.openDay)
# buttonDay.pack()