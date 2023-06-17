import customtkinter as ctk
from ..settings import *
from ..database import ReportWriterInstance
import os
from .login_frame import LoginFrame
from .register_frame import RegisterFrame
from typing import Type


class LoginWindow(ctk.CTkToplevel):
    def __init__(self, master, user_accepted: ctk.BooleanVar, db_instance: ReportWriterInstance):
        super().__init__(master, fg_color=ROOT_BG)

        self.db_instance = db_instance

        self.update_idletasks()
        ws = self.winfo_screenwidth()
        hs = self.winfo_screenheight()

        x = int((ws / 2) - (LOGIN_WIDTH / 2))
        y = int((hs / 2) - (LOGIN_HEIGHT / 2)) - 100

        self.geometry(f"{LOGIN_GEOMETRY}+{x}+{y}")

        self.user_accepted = user_accepted
        self.resizable(False, False)

        self.title("Login")

        # CTk.Toplevel source code applies default iconbitmap after 200ms (for some reason), this overrides any icon
        #  change made during initialisation of login window. This code overrides their override by rendering my icon
        #  50ms after theirs.
        self.after(250, lambda: self.iconbitmap(os.path.join(os.getcwd(), "images/app-logo.ico")))

        self.frames: dict[str, LoginFrame | RegisterFrame] = {}
        self.__setup_frames()

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.after(100, self.show_frame, "login")

        self.wait_window()

    def __setup_frames(self):
        current_frame_list: dict[str, Type[LoginFrame | RegisterFrame]] = {
            "login": LoginFrame,
            "register": RegisterFrame
        }
        for name, frame in current_frame_list.items():
            new_frame = frame(self, self.user_accepted, self.db_instance)
            self.frames[name] = new_frame
            new_frame.grid(row=0, column=0, sticky="nsew")

    def show_frame(self, frame_to_show: str):
        frame = self.frames[frame_to_show]
        frame.tkraise()
        frame.set_focus()
        return frame
