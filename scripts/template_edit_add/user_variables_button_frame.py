import customtkinter as ctk
from ..settings import *
from ..components import SmallEntry


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

        self.create_variable_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.create_variable_frame.grid(row=1, column=0, sticky="nsew", padx=(0, SMALL_PAD), pady=(0, SMALL_PAD))

        self.variable_name_label = ctk.CTkLabel(
            self.create_variable_frame,
            fg_color="transparent",
            text="Variable name",
            font=ctk.CTkFont(**SMALL_LABEL_FONT, slant="italic"),
            anchor="w"
        )
        self.variable_name_label.grid(row=0, column=0, sticky="ew")

        self.variable_name_entry = SmallEntry(self.create_variable_frame,
                                              placeholder_text="eg., Positive descriptors")
        self.variable_name_entry.grid(row=1, column=0, sticky="nsew", pady=(0, SMALL_PAD))

        self.variable_choice_label = ctk.CTkLabel(
            self.create_variable_frame,
            fg_color="transparent",
            text="Variable choices",
            font=ctk.CTkFont(**SMALL_LABEL_FONT, slant="italic"),
            anchor="w"
        )
        self.variable_choice_label.grid(row=2, column=0, sticky="ew")

        self.variable_choice_entry = SmallEntry(self.create_variable_frame,
                                                placeholder_text="eg., choice1, choice2, ...")
        self.variable_choice_entry.grid(row=3, column=0, sticky="nsew")

        self.create_variable_frame.rowconfigure([0, 1], weight=0)
        self.create_variable_frame.columnconfigure(0, weight=1)

        self.rowconfigure(0, weight=0)
        self.columnconfigure(0, weight=2, uniform="columns")
        self.columnconfigure(1, weight=1, uniform="columns")
