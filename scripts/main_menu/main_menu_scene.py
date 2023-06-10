import customtkinter as ctk
from .. import title_bar as tbar
from ..settings import *


class MainMenuScene(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.title_bar = tbar.TitleBar(self, "Report Writer")
        self.title_bar.grid(row=0, column=0, columnspan=3, sticky="nsew")

        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=1)
        self.columnconfigure([0, 1, 2], weight=1)

        self.report_frame = ctk.CTkFrame(
            self,
        )
        self.report_frame.grid(row=1, column=0, columnspan=2, sticky="nsew", pady=(0, DEFAULT_PAD), padx=DEFAULT_PAD)

        self.template_frame = ctk.CTkFrame(
            self,
        )
        self.template_frame.grid(row=1, column=2, sticky="nsew", pady=(0, DEFAULT_PAD), padx=(0, DEFAULT_PAD))