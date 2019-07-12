from tkinter import *


root = Tk()

topFrame = Frame(root, width=1000, height=800)
topFrame.pack()

menu = Menu(root)
root.config(menu=menu)
subMenu = Menu(menu)
menu.add_cascade(label="Plik", menu=subMenu)
subMenu.add_cascade(label="Nowy")
subMenu.add_cascade(label="Zapisz")
subMenu.add_cascade(label="Wczytaj")
subMenu.add_separator()
subMenu.add_cascade(label="Zamknij")
helpMenu = Menu(menu)
menu.add_cascade(label="Pomoc", menu=helpMenu)
helpMenu.add_cascade(label="O nas")
root.mainloop()