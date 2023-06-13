import customtkinter as ctk
from ..components import ListCard
from ..containers import ReportTemplate
from ..settings import *


class TemplateCard(ListCard):
    def __init__(self, master, template: ReportTemplate, command=None):
        super().__init__(master, command=command)

        self.template_data = template

        self.title_label = ctk.CTkLabel(self,
                                        fg_color="transparent",
                                        text=f"{self.template_data.template_title}",
                                        font=ctk.CTkFont(**NORMAL_LABEL_FONT),
                                        anchor="nw",
                                        padx=0,
                                        pady=0)
        self.title_label.grid(row=0, column=0, columnspan=3, sticky="ew", padx=DEFAULT_PAD,
                              pady=(SMALL_PAD, DEFAULT_PAD))

        self.rowconfigure([0], weight=0)
        self.columnconfigure([0, 1, 2], weight=1, uniform="columns")
        self.bind_frame()
