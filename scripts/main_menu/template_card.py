import customtkinter as ctk
from ..components import ListCard
from ..containers import ReportTemplate
from ..settings import *
from ..app_engine import AppEngine
from tkinter import Menu


class TemplateCard(ListCard):
    def __init__(self, master, app_engine: AppEngine, template: ReportTemplate, command=None):
        super().__init__(master, command=command)
        self.card_data = template

        title_text = f"{self.card_data.template_title}"
        if "@" in self.card_data.id:
            title_text += "*"

        title_label = ctk.CTkLabel(self,
                                   fg_color="transparent",
                                   text=title_text,
                                   font=ctk.CTkFont(**NORMAL_LABEL_FONT),
                                   anchor="nw",
                                   padx=0,
                                   pady=0)
        title_label.grid(row=0, column=0, columnspan=3, sticky="ew", padx=DEFAULT_PAD,
                         pady=(SMALL_PAD, DEFAULT_PAD))

        if self.card_data.owner is None:
            owner_string = "Created by: Unknown"
        elif self.card_data.owner.id == app_engine.get_user_id():
            owner_string = "Created by: Me"
        else:
            owner_string = f"Created and shared by: {self.card_data.owner.forename} " + \
                           f"{self.card_data.owner.surname}"

        self.owner_label = ctk.CTkLabel(self,
                                        fg_color="transparent",
                                        text=owner_string,
                                        font=ctk.CTkFont(**SMALL_LABEL_FONT, slant="italic"),
                                        anchor="nw",
                                        padx=0,
                                        pady=0)
        self.owner_label.grid(row=1, column=0, sticky="ew", padx=(DEFAULT_PAD, DEFAULT_PAD // 2),
                              pady=(0, DEFAULT_PAD))

        self.rowconfigure([0], weight=0)
        self.columnconfigure([0], weight=1, uniform="columns")
        self.bind_frame()
