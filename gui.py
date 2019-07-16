import controller
from tkinter import *
from tkinter import messagebox


class PlanerApp:
    def __init__(self):
        self.state = controller.Calendar()
        self.mainWindow = Tk()
        self.menu = PlanerApp.Menu(self.mainWindow)
        # frames
        self.topMainFrame = Frame(self.mainWindow, width=50, height=1)
        # leftMainFrame = Frame(mainWindow, width=1, height=700, bg="red")
        # rightMainFrame = Frame(mainWindow, width=1, height=700, bg="red")
        self.bottomMainFrame = Frame(self.mainWindow)
        self.topFrame = PlanerApp.NavFrame(self.mainWindow, self)
        self.bottomFrame = PlanerApp.CalFrame(self)

    def run(self):
        self.mainWindow.mainloop()

    def prev_month(self):
        print("cofaj")
        self.state.prev_month()
        self.calendar_refresh()

    def next_month(self):
        print("naprzod")
        self.state.next_month()
        self.calendar_refresh()

    def calendar_refresh(self):
        self.bottomFrame.forget()
        self.bottomFrame.destroy()
        self.bottomFrame = PlanerApp.CalFrame(self)

    class Menu:
        def __init__(self, window):
            self.mainMenu(window)

        def about(self):
            aboutUs = open('about')
            try:
                textAbout = aboutUs.read()
            finally:
                textAbout.close()
            messagebox.showinfo("O nas", textAbout)

        def mainMenu(self, window):
            # ---------MAIN MENU---------
            mainMenu = Menu(window)  # Menu method from Tkinter
            window.config(menu=mainMenu)

            subMenu = Menu(mainMenu)
            mainMenu.add_cascade(label="Plik", menu=subMenu)
            subMenu.add_cascade(label="Nowy")
            subMenu.add_cascade(label="Zapisz")
            subMenu.add_cascade(label="Wczytaj")
            subMenu.add_separator()
            subMenu.add_cascade(label="Zamknij")

            helpMenu = Menu(mainMenu)
            mainMenu.add_cascade(label="Pomoc", menu=helpMenu)
            helpMenu.add_command(label="O nas", command=self.about)  # added showinfo window
            return mainMenu

    class NavFrame:
        def __init__(self, window, parent):
            menuTopFrame = Frame(window, width=1100, height=50)
            menuTopFrame.pack(side=TOP)

            left = Button(menuTopFrame, text='<', command=lambda: parent.prev_month())
            left.pack(side=LEFT)

            right = Button(menuTopFrame, text='>', command=lambda: parent.next_month())
            right.pack(side=LEFT)

            self.topFrame = menuTopFrame

        def forget(self):
            self.topFrame.pack_forget()

        def destroy(self):
            self.topFrame.destroy()

    class CalFrame:
        def __init__(self, parent):
            menuBottomFrame = Frame(parent.mainWindow)
            menuBottomFrame.pack(side=BOTTOM)

            # displaying calendar grid
            for day in parent.state.get_month_data():
                Label(menuBottomFrame,
                      text='col:{0}, row:{1}\nday:{2}\nnotes: {3}, images:{4}'.format(day['day_of_week'],
                                                                                      day['week_of_month'],
                                                                                      day['day_of_month'],
                                                                                      day['notes_count'],
                                                                                      day['images_count']),
                      borderwidth=50).grid(row=day['week_of_month'], column=day['day_of_week'])

            self.bottomFrame = menuBottomFrame

        def forget(self):
            self.bottomFrame.pack_forget()

        def destroy(self):
            self.bottomFrame.destroy()


if __name__ == '__main__':
    PlanerApp().run()
