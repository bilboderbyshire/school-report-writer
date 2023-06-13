from tkinter import Misc
import customtkinter as ctk
from .settings import *
import os
from .login_window import LoginWindow
from .main_menu import MainMenuScene


class ReportWriter(ctk.CTk):
    def __init__(self):
        super().__init__(fg_color=ROOT_BG)

        ctk.set_default_color_theme(os.path.join(os.getcwd(), "scripts/app-theme.json"))
        ctk.set_appearance_mode("dark")

        self.update_idletasks()

        ws = self.winfo_screenwidth()
        hs = self.winfo_screenheight()

        x = int((ws / 2) - (WIDTH / 2))
        y = int((hs / 2) - (HEIGHT / 2)) - 100

        self.geometry(f"{GEOMETRY}+{x}+{y}")
        self.title(WINDOW_TITLE)
        self.iconbitmap(default=os.path.join(os.getcwd(), "images/app-logo.ico"))

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self.frames = {}
        self.__setup_frames()
        self.__login()

    def __login(self):
        user_accepted = ctk.BooleanVar(value=False)
        LoginWindow(self, user_accepted)
        if user_accepted.get():
            self.show_frame("main-menu")
            self.frames["main-menu"].refresh_frames()
        else:
            self.destroy()

    def __setup_frames(self):
        current_frame_list = {"main-menu": MainMenuScene}
        for name, frame in current_frame_list.items():
            new_frame = frame(self)
            self.frames[name] = new_frame
            new_frame.grid(row=0, column=0, sticky="nsew")

    def show_frame(self, frame_to_show) -> Misc:
        frame = self.frames[frame_to_show]
        frame.tkraise()
        return frame
