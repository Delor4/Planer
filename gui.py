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

def calendarWeeks():
    cal = calendar.Calendar()
    print("Tygodnie w lutym 2010:")
    for week in cal.monthdayscalendar(2010, 2):
        print(week)
    print("Tygodnie w marcu 2009:")
    for week in cal.monthdayscalendar(2009, 3):
        print(week)
#
# # loop for creating grid v2
# def calendarView():
for row in range(5):
    for column in range(7):
        Label(mainWindow, text = calendarWeeks(), borderwidth = 50).grid(row = row, column = column)



mainWindow.mainloop()