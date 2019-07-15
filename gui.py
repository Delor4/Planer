import controller
from controller import *
from tkinter import *
from tkinter import messagebox
import calendar
import datetime

mainWindow = Tk()

class PlanerApp:
    def __init__(self):
        self.state = controller.Calendar()
        self.mainWindow = Tk()

    def run(self):
        self.mainWindow.mainloop()

    # frames
    topMainFrame = Frame(mainWindow, width=50, height=1)
    # leftMainFrame = Frame(mainWindow, width=1, height=700, bg="red")
    # rightMainFrame = Frame(mainWindow, width=1, height=700, bg="red")
    bottomMainFrame = Frame(mainWindow)

    if __name__ == '__main__':
        run()


class PlanerMenu:
    def __init__(self):
        self.menuTopFrame = Frame(PlanerApp.mainWindow, width=1100, height=50)
        self.menuBottomFrame = Frame(PlanerApp.mainWindow)

    def prev_month(self):
        print("cofaj")
        self.month -= 1

    def next_month(self):
        print("naprzod")
        self.month += 4

    def about(self):
        aboutUs = open('about')
        try:
            textAbout = aboutUs.read()
        finally:
            textAbout.close()
        messagebox.showinfo("O nas", textAbout)


class Day:
    def __init__(self):
        self.day = 0
        print("Dzień tygodnia")

    def openDay(self):
        messagebox.showinfo("Dzień X", "To jest okno przykładowe")


dayObject = Day()
topMenu = PlanerMenu()
# calendarControl = Calendar()

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
helpMenu.add_command(label = "O nas", command = topMenu.about) # added showinfo window

#---------LAYOUT---------
# calendar
# main
cal = calendar.Calendar()
calendarControl = Calendar() # testowa implementacja controllera - utworzenie obiektu

row = 0

cal.year = datetime.date.today().year
cal.month = datetime.date.today().month

topMenu.menuTopFrame.pack(side = TOP)
topMenu.menuBottomFrame.pack(side = BOTTOM)

left = Button(topMenu.menuTopFrame, text='<', command=lambda: topMenu.prev_month(cal)) # trzeba zaimplementować controller
left.pack(side = LEFT)

right = Button(topMenu.menuTopFrame, text='>', command=lambda: topMenu.next_month(cal)) # trzeba zaimplementować controller
right.pack(side = LEFT)

# displaying calendar grid
for day in cal.itermonthdays2(cal.year, cal.month):
    if day[0] > 0:
        Label(topMenu.menuBottomFrame, text='col:{0}, row:{1}'.format(day[1], row), borderwidth=50).grid(row=row, column=day[1])
    if day[1] == 6:
        row += 1

PlanerApp.run()


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