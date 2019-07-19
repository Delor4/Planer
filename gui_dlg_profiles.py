from tkinter import *

from tkinter import Toplevel


class ProfilesDialog:
    def __init__(self, app):
        self.state = app.state
        self.T = app.T
        self.top = Toplevel(app.mainWindow)
        self.top.transient(app.mainWindow)
        self.top.grab_set()
        app.set_icon(self.top)
        self.top.title("Planer - {}".format(self.T("profiles_config_title")))  # Profiles config
        self.main_frame = None
        self.init_ui()

    def refresh(self):
        self.main_frame.pack_forget()
        self.main_frame.destroy()
        self.init_ui()

    def on_new_profile(self):
        self.state.make_profile(self.T("new_profile_name"))  # Default profile name
        self.refresh()

    def on_select_profile(self, profile_id):
        self.state.set_current_profile(profile_id)
        self.refresh()

    def on_exit(self):
        self.top.destroy()

    def init_ui(self):
        self.main_frame = Frame(self.top)

        profiles_frame = Frame(self.main_frame)
        add_frame = Frame(self.main_frame)
        bottom_frame = Frame(self.main_frame)

        for p in self.state.get_all_profiles():
            profile_frame = Frame(profiles_frame)
            name_label = Label(profile_frame, text="{0}: {1}".format(p['id'], p['name']))
            name_label.pack(side=LEFT)
            if self.state.get_curr_profile() == p['id']:
                name_label.config(bg="white")
            Button(profile_frame, text=self.T("delete").capitalize()).pack(side=RIGHT, anchor=E)
            Button(profile_frame, text=self.T("edit").capitalize()).pack(side=RIGHT)
            Button(profile_frame, text=self.T("select").capitalize(),
                   command=lambda id=p['id']: self.on_select_profile(id)).pack(side=RIGHT)
            profile_frame.pack(fill=X, anchor=E)

        Button(add_frame, text=self.T("new_profile").capitalize(), command=self.on_new_profile).pack()
        Button(bottom_frame, text=self.T("ok"), command=self.on_exit).pack(side=RIGHT)

        profiles_frame.pack(fill=X)
        add_frame.pack()
        bottom_frame.pack(fill=X, side=BOTTOM)
        self.main_frame.pack()
