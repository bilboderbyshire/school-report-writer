import customtkinter as ctk
from ..components import ListCard
from ..containers import ReportTemplate
from ..settings import *
from ..database import RUNNING_DB


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

        if self.template_data.owner is None:
            owner_string = "Created by: Unknown"
        elif self.template_data.owner.id == RUNNING_DB.get_users_id()[1]:
            owner_string = "Created by: Me"
        else:
            owner_string = f"Created and shared by: {self.template_data.owner.forename} " + \
                           f"{self.template_data.owner.surname}"

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
