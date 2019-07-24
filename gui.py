import controller
from tkinter import *

import tooltip

import gui_dlg_day
import gui_dlg_profiles
from gui_base_dialog import PlanerBaseDialog, CaptionDialog


class PlanerApp(PlanerBaseDialog):

    def __init__(self):
        self.app = self
        self.state = controller.Calendar()
        self.T = self.state.translate

        PlanerBaseDialog.__init__(self, self, window=Tk())

        self.lang = IntVar()
        self.profile = IntVar()

        self.menu = None
        self.nav_frame = None
        self.calendar_frame = None

        self.initial_dir = '.'

        self.init_ui()

    def init_ui(self):
        self.set_title(self.state.get_curr_profile_name())

        self.lang.set(self.state.get_language())
        self.profile.set(self.state.get_curr_profile())

        self.menu = self.create_main_menu(self.top)
        self.nav_frame = self.create_nav_frame(self.top)
        self.calendar_frame = self.create_calendar_frame(self.top)

    def refresh(self):
        self.menu.destroy()
        self.nav_frame.destroy()
        self.calendar_frame.destroy()
        self.init_ui()

    def run(self):
        self.top.mainloop()

    # Menu
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
        file_menu.add_command(label=self.T("close").capitalize(), command=self.close_window)
        return file_menu

    def create_profiles_submenu(self, menu):
        profiles_menu = Menu(menu)
        menu.add_cascade(label=self.T("profile").capitalize(), menu=profiles_menu)

        for prof in self.state.get_all_profiles():
            profiles_menu.add_radiobutton(label="{0}: {1}".format(str(prof['id']), prof['name']),
                                          var=self.profile,
                                          value=prof['id'],
                                          command=lambda pid=prof['id']: self.on_change_profile(pid))
        profiles_menu.add_separator()
        profiles_menu.add_command(label=self.T("configure").capitalize(), command=self.on_profiles_configure)

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
                                      var=self.lang,
                                      value=lang['id'],
                                      command=lambda lid=lang['id']: self.on_change_language(lid))

        return lang_menu

    def create_help_menu(self, menu):
        help_menu = Menu(menu)
        menu.add_cascade(label=self.T("help").capitalize(), menu=help_menu)
        help_menu.add_command(label=self.T("about").capitalize(), command=self.on_about)
        return help_menu

    # NavFrame
    def create_nav_frame(self, parent_frame):

        menu_top_frame = Frame(parent_frame, width=1100, height=50) # tło pod nazwą miesiąca
        menu_top_frame.pack(side=TOP)

        left = Button(menu_top_frame, text='<', command=self.on_prev_month, highlightcolor="red")

        left.pack(side=LEFT)

        Label(menu_top_frame,
              text="{1} {0}".format(self.state.get_year(),
                                    self.T("month_" + str(self.state.get_month())).capitalize()), width=15).pack(side=LEFT)

        right = Button(menu_top_frame, text='>', command=self.on_next_month)
        right.pack(side=LEFT)

        return menu_top_frame

    # Calendar Frame
    def create_calendar_frame(self, parent_frame):

        menu_bottom_frame = Frame(parent_frame) # TŁO POD CAŁYM PLANEREM

        menu_bottom_frame.pack(side=BOTTOM)

        # displaying week days names bar
        for day_nr in range(7):
            day_label = Label(menu_bottom_frame, text=self.T("weekday_" + str(day_nr)).upper()) # tło pod dniami tygodnia

            day_label.grid(row=0, column=day_nr)

        # displaying calendar grid
        for day in self.state.get_month_data():
            day_frame = LabelFrame(menu_bottom_frame, text=day['day_of_month'])
            day_frame.grid(row=day['week_of_month'] + 1, column=day['day_of_week'])
            label = Label(day_frame,
                          text='day:{2}\nnotes: {3}, images:{4}'.format(day['day_of_week'],
                                                                        day['week_of_month'],
                                                                        day['day_of_month'],
                                                                        day['notes_count'],
                                                                        day['images_count']),
                          borderwidth=50,
                          ) # tło pod planerem

            label.grid()

            label.bind("<Button-1>", lambda event, d=day['day_of_month']: self.on_day_click(event, d))

            if day['notes_count'] > 0:
                self.add_tooltip_for_day(day_frame, day['day_of_month'])
        return menu_bottom_frame

    def add_tooltip_for_day(self, form, day):
        text = []
        for n in self.state.get_textnotes(day):
            text.append(n['value'])
        tooltip.Tooltip(form, text="\n------\n".join(text))

    # Events handlers
    def on_prev_month(self):
        self.state.prev_month()
        self.refresh()

    def on_next_month(self):
        self.state.next_month()
        self.refresh()

    def on_change_profile(self, p_id):
        self.state.set_current_profile(p_id)
        self.refresh()

    def on_profiles_configure(self):
        return self.show_profiles_dlg()

    def on_change_language(self, l_id):
        self.state.set_language(l_id)
        self.refresh()

    def on_about(self):
        team = list()
        for line in open('about', encoding="utf-8"):
            team.append(line.strip())

        text = [self.app_name, ""]
        text.extend(team)

        CaptionDialog(self, title=self.T("about_title"), caption="\n".join(text))

    def on_day_click(self, _, day):
        self.show_day_dlg(day)

    # Helper methods
    def show_day_dlg(self, day):
        d = gui_dlg_day.DayDialog(self, day)
        self.top.wait_window(d.top)
        self.refresh()

    def show_profiles_dlg(self):
        d = gui_dlg_profiles.ProfilesDialog(self)
        self.top.wait_window(d.top)
        self.refresh()


if __name__ == '__main__':
    PlanerApp().run()
