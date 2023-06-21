import customtkinter as ctk
from ..settings import *


class UserVariablesButtonFrame(ctk.CTkFrame):
    def __init__(self,
                 master):
        super().__init__(master,
                         fg_color="transparent")

        title_label = ctk.CTkLabel(
            self,
            font=ctk.CTkFont(**NORMAL_LABEL_FONT),
            anchor="w",
            fg_color="transparent",
            text="Create variables")

        title_label.grid(row=0, column=0, columnspan=3, sticky="nw", pady=(5, 6))

        self.rowconfigure(0, weight=0)
        self.columnconfigure(0, weight=2, uniform="columns")
        self.columnconfigure(1, weight=1, uniform="columns")
