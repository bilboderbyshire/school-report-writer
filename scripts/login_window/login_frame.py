import customtkinter as ctk
from ..components import TitleLabel, SingleLineEntry, NormalLabel, SmallLabelButton, SmallLabel
from ..settings import *
from ..database import RUNNING_DB


class LoginFrame(ctk.CTkFrame):
    def __init__(self, master, user_accepted: ctk.BooleanVar):
        super().__init__(master,
                         fg_color="transparent")

        self.user_accepted = user_accepted

        self.title_bar = TitleLabel(self,
                                    "Login")
        self.title_bar.grid(row=0, column=0, columnspan=3, sticky="w", pady=(DEFAULT_PAD, 30), padx=DEFAULT_PAD)

        self.email_label = NormalLabel(self,
                                       text="Email address",
                                       anchor="sw")
        self.email_label.grid(row=1, column=0, columnspan=3, sticky="nsew", pady=(0, DEFAULT_PAD), padx=DEFAULT_PAD)

        self.email_entry = SingleLineEntry(self,
                                           placeholder_text="Type email here...")
        self.email_entry.grid(row=2, column=0, columnspan=3, sticky="new", pady=(0, DEFAULT_PAD+20), padx=DEFAULT_PAD)

        self.password_label = NormalLabel(self,
                                          text="Password",
                                          anchor="sw")
        self.password_label.grid(row=3, column=0, columnspan=3, sticky="nsew", pady=(0, DEFAULT_PAD), padx=DEFAULT_PAD)

        self.password_entry = SingleLineEntry(self,
                                              placeholder_text="Type password here...",
                                              show="•")
        self.password_entry.grid(row=4, column=0, columnspan=3, sticky="new", pady=(0, DEFAULT_PAD), padx=DEFAULT_PAD)

        self.register_button = SmallLabelButton(self,
                                                text="Register account",
                                                width=5)
        self.register_button.grid(row=5, column=1, columnspan=2, sticky="ne", pady=(0, DEFAULT_PAD), padx=DEFAULT_PAD)

        self.error_label_sv = ctk.StringVar()
        self.error_label = SmallLabel(self,
                                      textvariable=self.error_label_sv,
                                      text_color=ERROR_TEXT_COLOR,
                                      wraplength=LOGIN_WIDTH-(DEFAULT_PAD*2),
                                      anchor="nw",
                                      justify="left")
        self.error_label.grid(row=6, column=0, columnspan=3, sticky="nsew", pady=(0, DEFAULT_PAD), padx=DEFAULT_PAD)

        self.login_button = ctk.CTkButton(self,
                                          text="Login",
                                          font=ctk.CTkFont(**NORMAL_LABEL_FONT),
                                          border_spacing=5,
                                          command=self.login_request)
        self.login_button.grid(row=7, column=1, sticky="ew", pady=(0, DEFAULT_PAD), padx=(0, DEFAULT_PAD))

        self.cancel_button = ctk.CTkButton(self,
                                           text="Cancel",
                                           font=ctk.CTkFont(**NORMAL_LABEL_FONT),
                                           border_spacing=5,
                                           command=self.cancel_login)
        self.cancel_button.grid(row=7, column=2, sticky="ew", pady=(0, DEFAULT_PAD), padx=(0, DEFAULT_PAD))

        self.rowconfigure([0, 1, 2, 3, 4, 5, 7], weight=0)
        self.rowconfigure([6], weight=1, uniform="rows")
        self.columnconfigure([0, 1, 2], weight=1, uniform="columns")

    def login_request(self):
        current_email = self.email_entry.get()
        current_password = self.password_entry.get()

        if "@" not in current_email or "." not in current_email:
            self.error_label_sv.set("Not a valid email address")
            return
        else:
            self.error_label_sv.set("")

        response = RUNNING_DB.login(current_email, current_password)

        if response["response"]:
            self.user_accepted.set(True)
            self.master.destroy()
        else:
            self.user_accepted.set(False)
            self.error_label_sv.set(response["message"])
            return

    def cancel_login(self):
        self.user_accepted.set(False)
        self.master.destroy()