import platform

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
        PlanerApp.set_icon(self.mainWindow)
        self.lang = IntVar()

        self.menu = None
        self.topMainFrame = None
        self.bottomMainFrame = None
        self.topFrame = None
        self.bottomFrame = None
        self.init_ui()

    def close_window(self):
        self.mainWindow.destroy()

    def init_ui(self):
        self.mainWindow.title("Planer - {}".format(self.state.get_curr_profile_name()))
        self.lang.set(self.state.get_language())
        self.menu = PlanerApp.Menu(self.mainWindow, self)
        # frames
        self.topMainFrame = Frame(self.mainWindow, width=50, height=1)
        # leftMainFrame = Frame(mainWindow, width=1, height=700, bg="red")
        # rightMainFrame = Frame(mainWindow, width=1, height=700, bg="red")
        self.bottomMainFrame = Frame(self.mainWindow)
        self.topFrame = PlanerApp.NavFrame(self.mainWindow, self)
        self.bottomFrame = PlanerApp.CalFrame(self)

    def refresh(self):
        self.menu.menu.destroy()
        self.topFrame.destroy()
        self.bottomFrame.destroy()
        self.init_ui()

    @staticmethod
    def set_icon(window):
        if platform.system() == 'Windows':
            window.iconbitmap("planer.ico")
        elif platform.system() == 'Linux':
            window.tk.call('wm', 'iconphoto', window._w, PhotoImage(file='planer.png'))

    def run(self):
        self.mainWindow.mainloop()

    def prev_month(self):
        self.state.prev_month()
        self.refresh()

    def next_month(self):
        self.state.next_month()
        self.refresh()

    def calendar_refresh(self):
        self.bottomFrame.forget()
        self.bottomFrame.destroy()
        self.bottomFrame = PlanerApp.CalFrame(self)

    def show_day_dlg(self, day):
        d = gui_dlg_day.DayDialog(self, day)
        self.mainWindow.wait_window(d.top)
        self.refresh()

    def show_profiles_dlg(self):
        d = gui_dlg_profiles.ProfilesDialog(self)
        self.mainWindow.wait_window(d.top)
        self.refresh()

    class Menu:
        def __init__(self, window, parent):
            self.parent = parent
            self.state = parent.state
            self.T = parent.T
            self.menu = self.mainMenu(window)

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

        def on_change_language(self, l_id):
            self.state.set_language(l_id)
            self.parent.refresh()

        def create_lang_submenu(self, menu):
            for lang in self.state.get_all_languages():
                menu.add_radiobutton(label="{0} ({1})".format(lang['native_name'], lang['eng_name']),
                                     var=self.parent.lang, value=lang['id'],
                                     command=lambda lid=lang['id']: self.on_change_language(lid))

        def mainMenu(self, window):
            # ---------MAIN MENU---------

            mainMenu = Menu(window)
            window.config(menu=mainMenu)

            subMenu = Menu(mainMenu)
            mainMenu.add_cascade(label=self.T("File").capitalize(), menu=subMenu)
            subMenu.add_cascade(label=self.T("Profile").capitalize(), command=self.parent.show_profiles_dlg)

            subMenu.add_separator()
            subMenu.add_command(label=self.T("Close").capitalize(), command=self.parent.close_window)

            optMenu = Menu(mainMenu)
            mainMenu.add_cascade(label=self.T("Options").capitalize(), menu=optMenu)

            langMenu = Menu(optMenu)
            optMenu.add_cascade(label=self.T("Language").capitalize(), menu=langMenu)
            self.create_lang_submenu(langMenu)

            helpMenu = Menu(mainMenu)
            mainMenu.add_cascade(label=self.T("Help").capitalize(), menu=helpMenu)
            helpMenu.add_command(label=self.T("About").capitalize(), command=self.about)  # added showinfo window
            return mainMenu

    class NavFrame:
        def __init__(self, window, parent):
            self.state = parent.state
            self.T = parent.T

            menuTopFrame = Frame(window, width=1100, height=50)
            menuTopFrame.pack(side=TOP)

            left = Button(menuTopFrame, text='<', command=lambda: parent.prev_month(), highlightcolor="red")
            left.pack(side=LEFT)

            Label(menuTopFrame,
                  text="{1} {0}".format(self.state.get_year(), self.T("month_" + str(self.state.get_month())))).pack(
                side=LEFT)

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
            for day_nr in range(7):
                dayLabel = Label(menuBottomFrame, text=self.T("weekday_"+str(day_nr)).upper())
                dayLabel.grid(row=0, column=day_nr)

            # displaying calendar grid
            for day in parent.state.get_month_data():
                form = LabelFrame(menuBottomFrame, text=day['day_of_month'], )
                form.grid(row=day['week_of_month'] + 1, column=day['day_of_week'])
                label = Label(form,
                              text='day:{2}\nnotes: {3}, images:{4}'.format(day['day_of_week'],
                                                                            day['week_of_month'],
                                                                            day['day_of_month'],
                                                                            day['notes_count'],
                                                                            day['images_count']),
                              borderwidth=50, bg="white")
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
