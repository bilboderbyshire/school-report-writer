import customtkinter as ctk
from ..settings import *
from ..database import RUNNING_DB
import os
from .login_frame import LoginFrame


class LoginWindow(ctk.CTkToplevel):
    def __init__(self, master):
        super().__init__(master, fg_color=ROOT_BG)
        self.geometry(f"{LOGIN_GEOMETRY}")

        self.user_accepted = ctk.BooleanVar(value=False)
        self.resizable(False, False)

        self.title("Login")

        # CTk.Toplevel source code applies default iconbitmap after 200ms (for some reason), this overrides any icon
        #  change made during initialisation of login window. This code overrides their override by rendering my icon
        #  50ms after theirs.
        self.after(250, lambda: self.iconbitmap(os.path.join(os.getcwd(), "images/app-logo.ico")))

        self.frames = {}
        self.__setup_frames()
        self.show_frame(LoginFrame)

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.focus_force()
        self.wait_window()

    def __setup_frames(self):
        current_frame_list = [LoginFrame]
        for frame in current_frame_list:
            new_frame = frame(self, self.user_accepted)
            self.frames[frame] = new_frame
            new_frame.grid(row=0, column=0, sticky="nsew")

    def show_frame(self, frame_to_show):
        frame = self.frames[frame_to_show]
        frame.tkraise()

    def login(self):
        self.destroy()
