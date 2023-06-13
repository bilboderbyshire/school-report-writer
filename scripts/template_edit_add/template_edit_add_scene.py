import customtkinter as ctk
from .. import title_bar as tbar
from ..settings import *
from ..components import Separator, InvisibleEntry
from ..database import RUNNING_DB
from .section_scrollframe import SectionScrollableFrame


class TemplateScene(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color=ROOT_BG)

        self.prev_scene_string = None
        self.__build_frame()

    def __build_frame(self):

        self.title_bar = tbar.TitleBar(self, "Templates", refresh_command=None, back_command=self.go_back)
        self.title_bar.grid(row=0, column=0, columnspan=4, sticky="nsew", pady=(DEFAULT_PAD, 0), padx=DEFAULT_PAD)

        title_sep = Separator(self, "hor")
        title_sep.grid(row=2, column=0, columnspan=4, sticky="nsew", padx=DEFAULT_PAD * 3, pady=DEFAULT_PAD)

        self.name_entry = InvisibleEntry(self, placeholder_text="My new template")
        self.name_entry.grid(row=3, column=0, columnspan=2, sticky="ew", padx=DEFAULT_PAD*2, pady=DEFAULT_PAD)

        self.section_frame = SectionScrollableFrame(self)
        self.section_frame.grid(row=4, rowspan=2, column=0, sticky="nsew", padx=DEFAULT_PAD, pady=(0, DEFAULT_PAD))

        self.pieces_frame = ctk.CTkFrame(self)
        self.pieces_frame.grid(row=4, rowspan=2, column=1, sticky="nsew", padx=(0, DEFAULT_PAD),
                               pady=(0, DEFAULT_PAD))

        self.piece_info_frame = ctk.CTkFrame(self)
        self.piece_info_frame.grid(row=4, column=2, sticky="nsew", padx=(0, DEFAULT_PAD), pady=(0, DEFAULT_PAD))

        self.edit_piece_frame = ctk.CTkFrame(self)
        self.edit_piece_frame.grid(row=5, column=2, sticky="nsew", padx=(0, DEFAULT_PAD), pady=(0, DEFAULT_PAD))

        self.rowconfigure([0, 1, 2, 3], weight=0)
        self.rowconfigure([4, 5], weight=1, uniform="rows")
        self.columnconfigure(0, weight=1, uniform="columns")
        self.columnconfigure([1, 2], weight=2, uniform="columns")

    def fill_frames(self):
        self.section_frame.build_section_frame(4)
        self.section_frame.check_scrollbar_needed()
        self.change_cursor("arrow")

    def refresh_frames(self):
        self.change_cursor("watch")
        self.section_frame.loading_frame()

        self.after(600, self.fill_frames)

    def check_if_scroll_needed(self):
        self.section_frame.check_scrollbar_needed()

    def change_cursor(self, cursor: str) -> None:
        for i in self.winfo_children():
            i.configure(cursor=cursor)

    def previous_scene(self, name_of_prev_frame: str):
        self.prev_scene_string = name_of_prev_frame

    def go_back(self):
        self.master.show_frame(self.prev_scene_string)
