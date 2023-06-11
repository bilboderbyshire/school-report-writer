import customtkinter as ctk
from ..components import TitleLabel, SingleLineEntry, NormalLabel, SmallLabelButton, SmallLabel
from ..settings import *


class LoginFrame(ctk.CTkFrame):
    def __init__(self, master, user_accepted: ctk.BooleanVar):
        super().__init__(master,
                         fg_color="transparent")

        self.title_bar = TitleLabel(self,
                                    "Login")
        self.title_bar.grid(row=0, column=0, columnspan=3, sticky="w", pady=(DEFAULT_PAD, 20), padx=DEFAULT_PAD)

        self.username_label = NormalLabel(self,
                                          text="Username",
                                          anchor="sw")
        self.username_label.grid(row=1, column=0, columnspan=3, sticky="nsew", pady=(0, DEFAULT_PAD), padx=DEFAULT_PAD)

        self.username_entry = SingleLineEntry(self,
                                              placeholder_text="Type username here...")
        self.username_entry.grid(row=2, column=0, columnspan=3, sticky="ew", pady=(0, DEFAULT_PAD), padx=DEFAULT_PAD)

        self.password_label = NormalLabel(self,
                                          text="Password",
                                          anchor="sw")
        self.password_label.grid(row=3, column=0, columnspan=3, sticky="sew", pady=(0, DEFAULT_PAD), padx=DEFAULT_PAD)

        self.password_entry = SingleLineEntry(self,
                                              placeholder_text="Type password here...",
                                              show="•")
        self.password_entry.grid(row=4, column=0, columnspan=3, sticky="ew", pady=(0, DEFAULT_PAD), padx=DEFAULT_PAD)

        self.register_button = SmallLabelButton(self,
                                                text="Register account",
                                                width=5)
        self.register_button.grid(row=5, column=1, columnspan=2, sticky="e", pady=(0, DEFAULT_PAD), padx=DEFAULT_PAD)

        self.error_label_sv = ctk.StringVar()
        self.error_label = SmallLabel(self,
                                      textvariable=self.error_label_sv,
                                      text_color=ERROR_TEXT_COLOR,
                                      anchor="n")
        self.error_label.grid(row=6, column=0, columnspan=3, sticky="nsew", pady=(0, DEFAULT_PAD), padx=DEFAULT_PAD)

        self.login_button = ctk.CTkButton(self,
                                          text="Login",
                                          font=ctk.CTkFont(**NORMAL_LABEL_FONT),
                                          border_spacing=5)
        self.login_button.grid(row=7, column=1, sticky="ew", padx=(0, DEFAULT_PAD))

        self.cancel_button = ctk.CTkButton(self,
                                           text="Cancel",
                                           font=ctk.CTkFont(**NORMAL_LABEL_FONT),
                                           border_spacing=5)
        self.cancel_button.grid(row=7, column=2, sticky="ew", padx=(0, DEFAULT_PAD))

        self.rowconfigure(0, weight=0)
        self.rowconfigure([1, 2, 3, 4, 5, 6, 7], weight=1, uniform="rows")
        self.columnconfigure([0, 1, 2], weight=1, uniform="columns")

