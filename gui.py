import controller
from tkinter import *
from tkinter import messagebox
import gui_dlg_day
import gui_dlg_profiles


class PlanerApp:
    def __init__(self):
        self.state = controller.Calendar()
        self.mainWindow = Tk()
        self.T = self.state.translate
        self.mainWindow.iconbitmap("planer.ico")
        # self.mainWindow.tk.call('wm', 'iconphoto', self.mainWindow._w, PhotoImage(file='planer.png'))
        self.mainWindow.title("Planer")
        self.menu = PlanerApp.Menu(self.mainWindow, self)
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
        # print("cofaj")
        self.state.prev_month()
        self.calendar_refresh()

    def next_month(self):
        # print("naprzod")
        self.state.next_month()
        self.calendar_refresh()

    def calendar_refresh(self):
        self.bottomFrame.forget()
        self.bottomFrame.destroy()
        self.bottomFrame = PlanerApp.CalFrame(self)

    def show_day_dlg(self, day):
        d = gui_dlg_day.DayDialog(self, day)
        self.mainWindow.wait_window(d.top)
        self.calendar_refresh()

    def show_profiles_dlg(self):
        d = gui_dlg_profiles.ProfilesDialog(self)
        self.mainWindow.wait_window(d.top)
        self.calendar_refresh()

    class Menu:
        def __init__(self, window, parent):
            self.parent = parent
            self.T = parent.T
            self.mainMenu(window)

        def about(self):
            # title.name = "About" # title as parameter
            #
            # self.aboutUs = open('about')
            # try:
            #     message.file = self.aboutUs.read() # message as parameter
            # finally:
            #     message.file.close()
            #
            #  with open('about') as file:
            #      for line in file:
            #          print(line.strip().split())
            # title.name = "About"
            # message.info = "SKS Team:\nBrodziak Sebastian\nJaśkowski Krzysztof\nKucharczyk Sebastian"
            messagebox.showinfo("About", "SKS Team:\nBrodziak Sebastian\nJaśkowski Krzysztof\nKucharczyk Sebastian")

        def mainMenu(self, window):
            # ---------MAIN MENU---------
            mainMenu = Menu(window)  # Menu method from Tkinter
            window.config(menu=mainMenu)

            subMenu = Menu(mainMenu)
            mainMenu.add_cascade(label=self.T("Plik"), menu=subMenu)
            subMenu.add_cascade(label=self.T("Profile"), command=self.parent.show_profiles_dlg)
            subMenu.add_separator()
            subMenu.add_cascade(label=self.T("Zamknij"))

            helpMenu = Menu(mainMenu)
            mainMenu.add_cascade(label=self.T("Pomoc"), menu=helpMenu)
            helpMenu.add_command(label=self.T("O nas"), command=self.about)  # added showinfo window
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
            self.parent = parent
            self.T = self.parent.T

            menuBottomFrame = Frame(parent.mainWindow)
            menuBottomFrame.pack(side=BOTTOM)

            # displaying week days bar
            # week_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            # monday = Label(parent.mainWindow, text=week_days[0])
            # monday.grid(row=0, column=0)

            monLabel = Label(menuBottomFrame, text=self.T("monday").upper())
            tueLabel = Label(menuBottomFrame, text=self.T("tuesday").upper())
            wedLabel = Label(menuBottomFrame, text=self.T("wednesday").upper())
            thuLabel = Label(menuBottomFrame, text=self.T("thursday").upper())
            friLabel = Label(menuBottomFrame, text=self.T("friday").upper())
            satLabel = Label(menuBottomFrame, text=self.T("saturday").upper())
            sunLabel = Label(menuBottomFrame, text=self.T("sunday").upper())

            monLabel.grid(row=0, column=0)
            tueLabel.grid(row=0, column=1)
            wedLabel.grid(row=0, column=2)
            thuLabel.grid(row=0, column=3)
            friLabel.grid(row=0, column=4)
            satLabel.grid(row=0, column=5)
            sunLabel.grid(row=0, column=6)

            # displaying calendar grid
            for day in parent.state.get_month_data():
                form = LabelFrame(menuBottomFrame, text=day['day_of_month'])
                form.grid(row=day['week_of_month'] + 1, column=day['day_of_week'])
                label = Label(form,
                              text='day:{2}\nnotes: {3}, images:{4}'.format(day['day_of_week'],
                                                                            day['week_of_month'],
                                                                            day['day_of_month'],
                                                                            day['notes_count'],
                                                                            day['images_count']),
                              borderwidth=50)
                label.grid()

                label.bind("<Button-1>", lambda event, d=day['day_of_month']: self.mouseEventLMB(event, d))
            self.bottomFrame = menuBottomFrame

        def mouseEventLMB(self, event, day):
            self.parent.show_day_dlg(day)

        def forget(self):
            self.bottomFrame.pack_forget()

        def destroy(self):
            self.bottomFrame.destroy()


if __name__ == '__main__':
    PlanerApp().run()
