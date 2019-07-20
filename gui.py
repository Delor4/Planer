import controller
from tkinter import *
from tkinter import messagebox

import tooltip

import gui_dlg_day
import gui_dlg_profiles
from gui_base_dialog import PlanerBaseDialog


class PlanerApp(PlanerBaseDialog):

    def __init__(self):
        self.app = self
        self.state = controller.Calendar()
        self.T = self.state.translate

        PlanerBaseDialog.__init__(self, self, window=Tk())

        self.lang = IntVar()
        self.profile = IntVar()

        self.menu = None
        self.top_main_frame = None
        self.bottom_main_frame = None
        self.top_frame = None
        self.bottom_frame = None

        self.initial_dir = '.'

        self.init_ui()

    def init_ui(self):
        self.set_title(self.state.get_curr_profile_name())

        self.lang.set(self.state.get_language())
        self.profile.set(self.state.get_curr_profile())

        self.menu = PlanerApp.Menu(self.top, self)
        # frames
        self.top_main_frame = Frame(self.top, width=50, height=1)
        # leftMainFrame = Frame(top, width=1, height=700, bg="red")
        # rightMainFrame = Frame(top, width=1, height=700, bg="red")
        self.bottom_main_frame = Frame(self.top)
        self.top_frame = PlanerApp.NavFrame(self.top, self)
        self.bottom_frame = PlanerApp.CalFrame(self)

    def refresh(self):
        self.menu.menu.destroy()
        self.top_frame.destroy()
        self.bottom_frame.destroy()
        self.init_ui()

    def run(self):
        self.top.mainloop()

    def prev_month(self):
        self.state.prev_month()
        self.refresh()

    def next_month(self):
        self.state.next_month()
        self.refresh()

    def calendar_refresh(self):
        self.bottom_frame.forget()
        self.bottom_frame.destroy()
        self.bottom_frame = PlanerApp.CalFrame(self)

    def show_day_dlg(self, day):
        d = gui_dlg_day.DayDialog(self, day)
        self.top.wait_window(d.top)
        self.refresh()

    def show_profiles_dlg(self):
        d = gui_dlg_profiles.ProfilesDialog(self)
        self.top.wait_window(d.top)
        self.refresh()

    class Menu:
        def __init__(self, window, parent):
            self.parent = parent
            self.state = parent.state
            self.T = parent.T
            self.menu = self.create_main_menu(window)

        def about(self):
            team = list()
            for line in open('about'):
                team.append(line.strip().encode('windows-1250').decode('utf-8'))

            text = [self.parent.app_name, ""]
            text.extend(team)

            messagebox.showinfo(self.T("about_title"), "\n".join(text))
            # messagebox.showinfo(self.T("about_title"),
            #                    "SKS Team:\nBrodziak Sebastian\nJaśkowski Krzysztof\nKucharczyk Sebastian")

        def on_change_profile(self, p_id):
            self.state.set_current_profile(p_id)
            self.parent.refresh()

        def on_change_language(self, l_id):
            self.state.set_language(l_id)
            self.parent.refresh()

        def create_main_menu(self, window):
            # ---------MAIN MENU---------

            main_menu = Menu(window)
            window.config(menu=main_menu)

            self.create_file_menu(main_menu)
            self.create_options_menu(main_menu)
            self.create_help_menu(main_menu)

            return main_menu

        def create_file_menu(self, menu):
            file_menu = Menu(menu)
            menu.add_cascade(label=self.T("file").capitalize(), menu=file_menu)

            self.create_profiles_submenu(file_menu)

            file_menu.add_separator()
            file_menu.add_command(label=self.T("close").capitalize(), command=self.parent.close_window)
            return file_menu

        def create_profiles_submenu(self, menu):
            profiles_menu = Menu(menu)
            menu.add_cascade(label=self.T("profile").capitalize(), menu=profiles_menu)

            for prof in self.state.get_all_profiles():
                profiles_menu.add_radiobutton(label="{0}: {1}".format(str(prof['id']), prof['name']),
                                              var=self.parent.profile, value=prof['id'],
                                              command=lambda pid=prof['id']: self.on_change_profile(pid))
            profiles_menu.add_separator()
            profiles_menu.add_command(label=self.T("configure").capitalize(), command=self.parent.show_profiles_dlg)

            return profiles_menu

        def create_options_menu(self, menu):
            options_menu = Menu(menu)
            menu.add_cascade(label=self.T("options").capitalize(), menu=options_menu)

            self.create_lang_submenu(options_menu)
            return options_menu

        def create_lang_submenu(self, menu):
            lang_menu = Menu(menu)
            menu.add_cascade(label=self.T("language").capitalize(), menu=lang_menu)

            for lang in self.state.get_all_languages():
                lang_menu.add_radiobutton(label="{0} ({1})".format(lang['native_name'], lang['eng_name']),
                                          var=self.parent.lang, value=lang['id'],
                                          command=lambda lid=lang['id']: self.on_change_language(lid))

            return lang_menu

        def create_help_menu(self, menu):
            help_menu = Menu(menu)
            menu.add_cascade(label=self.T("help").capitalize(), menu=help_menu)
            help_menu.add_command(label=self.T("about").capitalize(), command=self.about)
            return help_menu

    class NavFrame:
        def __init__(self, window, parent):
            self.state = parent.state
            self.T = parent.T

            menu_top_frame = Frame(window, width=1100, height=50)
            menu_top_frame.pack(side=TOP)

            left = Button(menu_top_frame, text='<', command=lambda: parent.prev_month(), highlightcolor="red")
            left.pack(side=LEFT)

            Label(menu_top_frame,
                  text="{1} {0}".format(self.state.get_year(),
                                        self.T("month_" + str(self.state.get_month())).capitalize())).pack(
                side=LEFT)

            right = Button(menu_top_frame, text='>', command=lambda: parent.next_month())
            right.pack(side=LEFT)

            self.topFrame = menu_top_frame

        def forget(self):
            self.topFrame.pack_forget()

        def destroy(self):
            self.topFrame.destroy()

    class CalFrame:
        def __init__(self, parent):
            self.parent = parent
            self.T = self.parent.T
            self.state = parent.state

            menu_bottom_frame = Frame(parent.top)
            menu_bottom_frame.pack(side=BOTTOM)

            # displaying week days bar
            for day_nr in range(7):
                day_label = Label(menu_bottom_frame, text=self.T("weekday_" + str(day_nr)).upper())
                day_label.grid(row=0, column=day_nr)

            # displaying calendar grid
            for day in parent.state.get_month_data():
                form = LabelFrame(menu_bottom_frame, text=day['day_of_month'])
                form.grid(row=day['week_of_month'] + 1, column=day['day_of_week'])
                label = Label(form,
                              text='day:{2}\nnotes: {3}, images:{4}'.format(day['day_of_week'],
                                                                            day['week_of_month'],
                                                                            day['day_of_month'],
                                                                            day['notes_count'],
                                                                            day['images_count']),
                              borderwidth=50, bg="white")
                label.grid()

                label.bind("<Button-1>", lambda event, d=day['day_of_month']: self.on_day_click(event, d))

                if day['notes_count'] > 0:
                    self.add_tooltip_for_day(form, day['day_of_month'])
            self.bottomFrame = menu_bottom_frame

        def add_tooltip_for_day(self, form, day):
            text = []
            for n in self.state.get_textnotes(day):
                text.append(n['value'])
            tooltip.Tooltip(form, text="\n------\n".join(text))

        def on_day_click(self, _, day):
            self.parent.show_day_dlg(day)

        def forget(self):
            self.bottomFrame.pack_forget()

        def destroy(self):
            self.bottomFrame.destroy()


if __name__ == '__main__':
    PlanerApp().run()
