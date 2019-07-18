from tkinter import *

from tkinter import Toplevel


class ProfilesDialog:
    def __init__(self, app):
        self.state = app.state
        self.top = Toplevel(app.mainWindow)
        self.top.transient(app.mainWindow)
        self.top.grab_set()
        self.top.iconbitmap("planer.ico")
        # self.top.tk.call('wm', 'iconphoto', self.mainWindow._w, PhotoImage(file='planer.png'))
        self.top.title("Planer - Profile")
        self.main_frame = None
        self.init_ui()

    def refresh(self):
        self.main_frame.pack_forget()
        self.main_frame.destroy()
        self.init_ui()

    def on_new_profile(self):
        self.state.make_profile("Default profile name")
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
            l = Label(profile_frame, text="{0}: {1}".format(p['id'], p['name']))
            l.pack(side=LEFT)
            if self.state.get_curr_profile() == p['id']:
                l.config(bg="white")
            Button(profile_frame, text="Edit").pack(side=RIGHT, anchor=E)
            Button(profile_frame, text="Select", command=lambda id=p['id']: self.on_select_profile(id)).pack(side=RIGHT)
            profile_frame.pack(fill=X, anchor=E)

        Button(add_frame, text="+", command=self.on_new_profile).pack()
        Button(bottom_frame, text="Ok", command=self.on_exit).pack(side=RIGHT)

        profiles_frame.pack(fill=X)
        add_frame.pack()
        bottom_frame.pack(fill=X, side=BOTTOM)
        self.main_frame.pack()
