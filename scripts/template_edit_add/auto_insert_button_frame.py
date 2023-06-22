import customtkinter as ctk
from ..settings import *
from typing import Callable


class AutoInsertButtons(ctk.CTkFrame):
    def __init__(self,
                 master,
                 insert_pronoun_command: Callable,
                 insert_pronoun_dependant_command: Callable,
                 insert_name_command: Callable):
        super().__init__(master,
                         fg_color="transparent")

        title_label = ctk.CTkLabel(
            self,
            font=ctk.CTkFont(**NORMAL_LABEL_FONT),
            anchor="w",
            fg_color="transparent",
            text="Auto inputs")

        title_label.grid(row=0, column=0, columnspan=3, sticky="nw", pady=(5, 6))

        self.insert_pronoun_dependant_command = insert_pronoun_dependant_command
        self.insert_pronoun_command = insert_pronoun_command

        self.pronoun_dropdown = ctk.CTkOptionMenu(
            self,
            font=ctk.CTkFont(**SMALL_LABEL_FONT, weight="bold"),
            dropdown_font=ctk.CTkFont(**SMALL_LABEL_FONT),
            values=[
                "Subjective: She laughed",
                "Objective: Told him",
                "Possessive: Her things",
                "Possessive adj: That's hers",
                "Reflexive: To themself"
            ],
            command=self.pronoun_dropdown_callback
        )
        self.pronoun_dropdown.set("Pronoun")
        self.pronoun_dropdown.grid(row=1, column=0, sticky="ew", padx=(0, SMALL_PAD))

        self.pronoun_dependants_dropdown = ctk.CTkOptionMenu(
            self,
            font=ctk.CTkFont(**SMALL_LABEL_FONT, weight="bold"),
            dropdown_font=ctk.CTkFont(**SMALL_LABEL_FONT),
            values=[
                "is/are",
                "has/have",
            ],
            command=self.pronoun_dependants_dropdown_callback
        )
        self.pronoun_dependants_dropdown.set("Dependant")
        self.pronoun_dependants_dropdown.grid(row=1, column=1, sticky="ew", padx=(0, SMALL_PAD))

        self.insert_name = ctk.CTkButton(
            self,
            font=ctk.CTkFont(**SMALL_LABEL_FONT, weight="bold"),
            text="Name",
            command=insert_name_command
        )
        self.insert_name.grid(row=1, column=2, sticky="ew")

        self.rowconfigure([0, 1], weight=0)
        self.columnconfigure([0, 1, 2], weight=1, uniform="columns")

    def pronoun_dropdown_callback(self, dropdown_value):
        self.pronoun_dropdown.set("Pronoun")
        self.insert_pronoun_command(dropdown_value)

    def pronoun_dependants_dropdown_callback(self, dropdown_value):
        self.pronoun_dependants_dropdown.set("Dependant")
        self.insert_pronoun_dependant_command(dropdown_value)

    def disable_all(self):
        self.pronoun_dropdown.configure(state="disabled")
        self.pronoun_dependants_dropdown.configure(state="disabled")
        self.insert_name.configure(state="disabled")

    def enable_all(self):
        self.pronoun_dropdown.configure(state="normal")
        self.pronoun_dependants_dropdown.configure(state="normal")
        self.insert_name.configure(state="normal")
