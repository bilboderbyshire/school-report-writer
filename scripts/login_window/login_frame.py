import customtkinter as ctk
from ..components import TitleLabel, SingleLineEntry, NormalLabel, SmallLabelButton
from ..settings import *


class LoginFrame(ctk.CTkFrame):
    def __init__(self, master, user_accepted: ctk.BooleanVar):
        super().__init__(master,
                         fg_color="transparent")

        self.title_bar = TitleLabel(self,
                                    "Login")
        self.title_bar.grid(row=0, column=0, columnspan=3, sticky="w", **DEFAULT_PAD_COMPLETE)

        self.username_label = NormalLabel(self,
                                          text="Username",
                                          anchor="w")
        self.username_label.grid(row=1, column=0, columnspan=3, sticky="nsew", pady=(30, DEFAULT_PAD), padx=DEFAULT_PAD)

        self.username_entry = SingleLineEntry(self,
                                              placeholder_text="Type username here...")
        self.username_entry.grid(row=2, column=0, columnspan=3, sticky="nsew", pady=(0, DEFAULT_PAD), padx=DEFAULT_PAD)

        self.password_label = NormalLabel(self,
                                          text="Password",
                                          anchor="w")
        self.password_label.grid(row=3, column=0, columnspan=3, sticky="nsew", pady=(30, DEFAULT_PAD), padx=DEFAULT_PAD)

        self.password_entry = SingleLineEntry(self,
                                              placeholder_text="Type password here...",
                                              show="•")
        self.password_entry.grid(row=4, column=0, columnspan=3, sticky="nsew", pady=(0, DEFAULT_PAD), padx=DEFAULT_PAD)

        self.register_button = SmallLabelButton(self,
                                                text="Register account",
                                                width=5)
        self.register_button.grid(row=5, column=2, sticky="e", pady=(0, DEFAULT_PAD), padx=DEFAULT_PAD)

        self.rowconfigure([0, 1, 2, 3, 4, 5], weight=0)
        self.columnconfigure([0, 1, 2], weight=1)

