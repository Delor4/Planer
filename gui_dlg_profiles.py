from tkinter import *
from tkinter import messagebox

import gui_base_dialog


class ProfilesDialog(gui_base_dialog.PlanerBaseModalDialog):
    def __init__(self, parent):
        gui_base_dialog.PlanerBaseModalDialog.__init__(self, parent)
        self.set_title(self.T("profiles_config_title"))  # Profiles config

        self.main_frame = None

        self.init_ui()

    def init_ui(self):
        self.main_frame = Frame(self.top)

        profiles_frame = self.create_profiles_frame(self.main_frame)
        add_profile_frame = self.create_add_profile_frame(self.main_frame)
        bottom_frame = self.create_bottom_frame(self.main_frame)

        profiles_frame.pack(fill=X, anchor=E)
        add_profile_frame.pack()
        bottom_frame.pack(fill=X, side=BOTTOM)
        self.main_frame.pack()

    def refresh(self):
        self.main_frame.pack_forget()
        self.main_frame.destroy()
        self.init_ui()

    # Main frames
    def create_profiles_frame(self, parent_frame):
        profiles_frame = Frame(parent_frame)
        for p in self.state.get_all_profiles():
            profile_frame = self.create_profile_frame(profiles_frame, p)
            profile_frame.pack(fill=X, anchor=E)
        return profiles_frame

    def create_add_profile_frame(self, parent_frame):
        add_profile_frame = Frame(parent_frame)
        Button(add_profile_frame, text=self.T("new_profile").capitalize(), command=self.on_new_profile).pack()
        return add_profile_frame

    def create_bottom_frame(self, parent_frame):
        bottom_frame = Frame(parent_frame)
        Button(bottom_frame, text=self.T("ok"), command=self.on_ok).pack(side=RIGHT)
        return bottom_frame

    # Profile subframe
    def create_profile_frame(self, parent_frame, p):
        profile_frame = Frame(parent_frame)
        name_label = Label(profile_frame, text="{0}: {1}".format(p['id'], p['name']))
        name_label.pack(side=LEFT)

        del_btn = Button(profile_frame, text=self.T("delete").capitalize(),
                         command=lambda pid=p['id']: self.on_delete_profile(pid))
        del_btn.pack(side=RIGHT, anchor=E)

        Button(profile_frame, text=self.T("edit").capitalize(),
               command=lambda pid=p['id']: self.on_edit_profile(pid)).pack(side=RIGHT)
        Button(profile_frame, text=self.T("select").capitalize(),
               command=lambda pid=p['id']: self.on_select_profile(pid)).pack(side=RIGHT)

        if self.state.get_curr_profile() == p['id']:
            name_label.config(bg="white")
            del_btn.configure(state=DISABLED)
        return profile_frame

    # Events handlers
    def on_select_profile(self, profile_id):
        self.state.set_current_profile(profile_id)
        self.refresh()

    def on_edit_profile(self, profile_id):
        text = self.get_user_text(self.T("enter_profile_name"),  # Wprowadź nazwę profilu:
                                  self.state.get_profile_name(profile_id),
                                  title=self.T("edit_profile_title"))  # Zmień profil
        if text is not None and len(text) > 0:
            self.state.update_profile(profile_id, text)
        self.refresh()

    def on_delete_profile(self, profile_id):
        if profile_id == self.state.get_curr_profile():
            messagebox.showinfo(self.T("caption_title"),
                                self.T("delete_error_curr_profile"))  # Aktywny profil nie może zostać usunięty.
        else:
            ynd = gui_base_dialog.YesNoDialog(self, self.T("delete_profile_prompt"), title=None)
            self.top.wait_window(ynd.top)
            if ynd.yes:
                self.state.delete_profile(profile_id)
        self.refresh()

    def on_new_profile(self):
        text = self.get_user_text(self.T("enter_profile_name"),  # Wprowadź nazwę profilu:
                                  title=self.T("new_profile_title"))  # Nowy profil
        if text is not None and len(text) > 0:
            self.state.make_profile(text)
        self.refresh()

    def on_ok(self):
        self.close_window()

    def get_user_text(self, prompt, text=None, title=None):
        td = gui_base_dialog.TextDialog(self, prompt, text=text, title=title)
        self.top.wait_window(td.top)
        if td.ok:
            return td.get_value()
