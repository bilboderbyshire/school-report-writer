import customtkinter as ctk
from .. import title_bar as tbar
from ..settings import *
from ..components import Separator, SmallLabelButton
from ..database import RUNNING_DB


class TemplateScene(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color=ROOT_BG)

        self.prev_scene_string = None

        self.title_bar = tbar.TitleBar(self, "Templates", refresh_command=None, back_command=self.go_back)
        self.title_bar.grid(row=0, column=0, columnspan=4, sticky="nsew", pady=(DEFAULT_PAD, 0), padx=DEFAULT_PAD)

        title_sep = Separator(self, "hor")
        title_sep.grid(row=2, column=0, columnspan=4, sticky="nsew", padx=DEFAULT_PAD * 3, pady=DEFAULT_PAD)

        self.rowconfigure([0, 1, 2], weight=0)
        # self.rowconfigure(2, weight=1)
        self.columnconfigure([0, 1, 3], weight=1)

    def previous_scene(self, name_of_prev_frame: str):
        self.prev_scene_string = name_of_prev_frame

    def go_back(self):
        self.master.show_frame(self.prev_scene_string)
