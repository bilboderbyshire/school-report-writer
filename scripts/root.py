import customtkinter as ctk
from .settings import *
import os
from .login_window import LoginWindow
from .main_menu import MainMenuScene
from .template_edit_add import TemplateScene
from .write_report import ReportScene
from .database import ReportWriterInstance
from .app_engine import AppEngine
from typing import Type, Literal


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
        self.minsize(WIDTH, HEIGHT)

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self.frames: dict[str, MainMenuScene | TemplateScene | ReportScene] = {}
        self.db_instance = ReportWriterInstance()
        self.app_engine: AppEngine | None = None
        self.__setup_frames()
        new_frame = self.show_frame("write-report-scene")
        new_frame.fill_frames()
        # self.__login()

    def __login(self):
        user_accepted = ctk.BooleanVar(value=False)
        LoginWindow(self, user_accepted, self.db_instance)
        if user_accepted.get():
            self.app_engine = AppEngine(self.db_instance)
            self.__setup_frames()

            new_frame = self.show_frame("main-menu")
            new_frame.fill_frames()

        else:
            self.destroy()

    def __setup_frames(self):
        current_frame_list: dict[str, Type[MainMenuScene | TemplateScene | ReportScene]] = {
            "main-menu": MainMenuScene,
            "template-scene": TemplateScene,
            "write-report-scene": ReportScene
        }
        for name, frame in current_frame_list.items():
            new_frame = frame(self, self.app_engine)
            self.frames[name] = new_frame
            new_frame.grid(row=0, column=0, sticky="nsew")

    def show_frame(self, frame_to_show: Literal["main-menu", "template-scene", "write-report-scene"]) \
            -> TemplateScene | MainMenuScene | ReportScene:
        frame = self.frames[frame_to_show]
        frame.tkraise()
        return frame

    def get_frame(self, frame_name: Literal["main-menu", "template-scene", "write-report-scene"]) \
            -> TemplateScene | MainMenuScene | ReportScene:
        frame = self.frames[frame_name]
        return frame
