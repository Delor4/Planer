from tkinter import *
from tkinter import messagebox
import calendar

#mainFrameWidth = 1000
#mainFrameHeight = 700

# creating main window
mainWindow = Tk()

# frames
topMainFrame = Frame(mainWindow, width = 1000, height = 1, bg = "red")
leftMainFrame = Frame(mainWindow, width = 1, height = 700, bg = "red")
rightMainFrame = Frame(mainWindow, width = 1, height = 700, bg = "red")
bottomMainFrame = Frame(mainWindow, width = 1000, height = 1, bg = "red")

# menu options
def about():
    messagebox.showinfo("O nas", "SKS Team:\nSebastian Kucharczyk\nKrzysztof Jaśkowski\nSebastian Brodziak")

# menu
menu = Menu(mainWindow)
mainWindow.config(menu=menu)
subMenu = Menu(menu)
menu.add_cascade(label="Plik", menu=subMenu)
subMenu.add_cascade(label="Nowy")
subMenu.add_cascade(label="Zapisz")
subMenu.add_cascade(label="Wczytaj")
subMenu.add_separator()
subMenu.add_cascade(label="Zamknij")
helpMenu = Menu(menu)
menu.add_cascade(label="Pomoc", menu=helpMenu)
helpMenu.add_command(label="O nas", command = about) # added showinfo window

#layout

# topMainFrame.pack(side = TOP)
# leftMainFrame.pack(side = LEFT)
# rightMainFrame.pack(side = RIGHT)
# bottomMainFrame.pack(side = BOTTOM)

# loop for creating grid v1
# for row in range(5):
#     for column in range(7):
#        Label(mainWindow, text = 'R%s/C%s'%(row, column), borderwidth = 50).grid(row = row, column = column)

buttonDay = Button()

#calendar
cal = calendar.Calendar()
row = 0
for day in cal.itermonthdays2(2016, 1):
    if day[0] > 0:
        print("col:{0}, row:{1}".format(day[1], row))
    if day[1] == 6:
        row += 1


mainWindow.mainloop()