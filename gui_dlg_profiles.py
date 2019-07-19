from tkinter import *

import gui_base_dialog


class ProfilesDialog(gui_base_dialog.PlanerBaseModalDialog):
    def __init__(self, parent):
        gui_base_dialog.PlanerBaseModalDialog.__init__(self, parent)
        self.set_title(self.T("profiles_config_title"))  # Profiles config

        self.main_frame = None
        self.input_ok = False
        self.input_top = None
        self.init_ui()

    def refresh(self):
        self.main_frame.pack_forget()
        self.main_frame.destroy()
        self.init_ui()

    def on_new_profile(self):
        text = self.get_user_text(self.T("enter_profile_name"),  # Wprowadź nazwę profilu:
                                  title=self.T("new_profile_title")) # Nowy profil
        if text is not None and len(text) > 0:
            self.state.make_profile(text)
        self.refresh()

    def on_select_profile(self, profile_id):
        self.state.set_current_profile(profile_id)
        self.refresh()

    def on_edit_profile(self, profile_id):
        text = self.get_user_text(self.T("enter_profile_name"), # Wprowadź nazwę profilu:
                                  self.state.get_profile_name(profile_id),
                                  title=self.T("edit_profile_title"))  # Zmień profil
        if text is not None and len(text) > 0:
            self.state.update_profile(profile_id, text)
        self.refresh()

    def on_exit(self):
        self.close_window()

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
            Button(profile_frame, text=self.T("edit").capitalize(),
                   command=lambda pid=p['id']: self.on_edit_profile(pid)).pack(side=RIGHT)
            Button(profile_frame, text=self.T("select").capitalize(),
                   command=lambda pid=p['id']: self.on_select_profile(pid)).pack(side=RIGHT)
            profile_frame.pack(fill=X, anchor=E)

        Button(add_frame, text=self.T("new_profile").capitalize(), command=self.on_new_profile).pack()
        Button(bottom_frame, text=self.T("ok"), command=self.on_exit).pack(side=RIGHT)

        profiles_frame.pack(fill=X)
        add_frame.pack()
        bottom_frame.pack(fill=X, side=BOTTOM)
        self.main_frame.pack()

    def get_user_text(self, prompt, text=None, title=None):
        opts = TextDialog.Opts()
        td = TextDialog(self, opts, prompt, text=text, title=title)
        self.top.wait_window(td.top)
        if opts.ok:
            return opts.value.get()


class TextDialog(gui_base_dialog.PlanerBaseModalDialog):
    class Opts:
        def __init__(self):
            self.value = StringVar()
            self.ok = False

    def __init__(self, parent, opts: Opts, prompt: str, text: str = None, title: str = None):
        gui_base_dialog.PlanerBaseModalDialog.__init__(self, parent, title=title)
        self.opts = opts

        self.opts.ok = False
        if text is not None:
            self.opts.value.set(text)

        self.init_ui(prompt)

    def init_ui(self, prompt: str):
        Label(self.top, text=prompt).pack(anchor=W)
        e = Entry(self.top, textvariable=self.opts.value)
        e.pack(fill=X)
        e.bind('<Return>', lambda event: self.on_input_ok())
        Button(self.top, text=self.T("ok"), command=self.on_input_ok).pack(anchor=E)

    def on_input_ok(self):
        self.opts.ok = True
        self.close_window()
