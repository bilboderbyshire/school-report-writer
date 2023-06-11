import customtkinter as ctk
from ..components import TitleLabel, SingleLineEntry, NormalLabel, SmallLabelButton, SmallLabel
from ..settings import *
from ..database import RUNNING_DB


class RegisterFrame(ctk.CTkFrame):
    """This frame allows the user to create a new account, by inputting their details and making a create request to the
    database. Basic local validation is performed to ensure all the information is good. If successful, the user is
    logged in, and the main menu is displayed. If not successful, an error label is updated with an appropriate
    message, and the user is given another chance"""
    def __init__(self, master, user_accepted: ctk.BooleanVar):
        super().__init__(master,
                         fg_color="transparent")

        # User accepted bool is tracked by root app, decides if root should destroy itself (registration cancelled) or
        #  deiconify (registration successful)
        self.user_accepted = user_accepted

        self.__build_app()

    def __build_app(self):

        # Title of the frame
        self.title_bar = TitleLabel(self,
                                    "Register")
        self.title_bar.grid(row=0, column=0, columnspan=3, sticky="w", pady=(DEFAULT_PAD, 0), padx=DEFAULT_PAD)

        self.back_button = SmallLabelButton(self,
                                            text="Back",
                                            height=35-(DEFAULT_PAD-5),
                                            anchor="nw",
                                            command=self.back_button_pressed)
        self.back_button.grid(row=1, column=0, sticky="w", pady=(5, 0), padx=DEFAULT_PAD-5)

        # Name entry
        # ==========

        self.name_frame = ctk.CTkFrame(self,
                                       fg_color="transparent")
        self.name_frame.grid(row=2, column=0, columnspan=3, sticky="nsew", pady=(0, DEFAULT_PAD + 20), padx=DEFAULT_PAD)

        # Forename entry
        self.forename_label = NormalLabel(self.name_frame,
                                          text="Forename",
                                          anchor="sw")
        self.forename_label.grid(row=0, column=0, sticky="nsew", pady=(0, DEFAULT_PAD))

        self.forename_entry = SingleLineEntry(self.name_frame,
                                              placeholder_text="Type your forename")
        self.forename_entry.grid(row=1, column=0, sticky="new", padx=(0, DEFAULT_PAD//2))

        # Surname entry
        self.surname_label = NormalLabel(self.name_frame,
                                         text="Surname",
                                         anchor="sw")
        self.surname_label.grid(row=0, column=1, sticky="nsew", pady=(0, DEFAULT_PAD), padx=DEFAULT_PAD)

        self.surname_entry = SingleLineEntry(self.name_frame,
                                             placeholder_text="Type your surname")
        self.surname_entry.grid(row=1, column=1, sticky="new", padx=(DEFAULT_PAD//2, 0))

        self.name_frame.rowconfigure([0, 1], weight=0)
        self.name_frame.columnconfigure([0, 1], weight=1, uniform="columns")

        # Email entry
        self.email_label = NormalLabel(self,
                                       text="Email",
                                       anchor="sw")
        self.email_label.grid(row=3, column=0, columnspan=3, sticky="nsew", pady=(0, DEFAULT_PAD), padx=DEFAULT_PAD)

        self.email_entry = SingleLineEntry(self,
                                           placeholder_text="Type your email here...")
        self.email_entry.grid(row=4, column=0, columnspan=3, sticky="new", pady=(0, DEFAULT_PAD + 20),
                              padx=DEFAULT_PAD)

        # Password entry
        # ==========

        self.password_frame = ctk.CTkFrame(self,
                                           fg_color="transparent")
        self.password_frame.grid(row=5, column=0, columnspan=3, sticky="nsew", pady=(0, DEFAULT_PAD), padx=DEFAULT_PAD)

        # Password entry
        self.password_label = NormalLabel(self.password_frame,
                                          text="Password",
                                          anchor="sw")
        self.password_label.grid(row=0, column=0, sticky="nsew", pady=(0, DEFAULT_PAD))

        self.password_entry = SingleLineEntry(self.password_frame,
                                              placeholder_text="Password",
                                              show="•")
        self.password_entry.grid(row=1, column=0, sticky="new", padx=(0, DEFAULT_PAD // 2))

        # Password confirm entry
        self.password_confirm_label = NormalLabel(self.password_frame,
                                                  text="Confirm Password",
                                                  anchor="sw")
        self.password_confirm_label.grid(row=0, column=1, sticky="nsew", pady=(0, DEFAULT_PAD), padx=DEFAULT_PAD)

        self.password_confirm_entry = SingleLineEntry(self.password_frame,
                                                      placeholder_text="Type your surname",
                                                      show="•")
        self.password_confirm_entry.grid(row=1, column=1, sticky="new", padx=(DEFAULT_PAD // 2, 0))

        self.password_frame.rowconfigure([0, 1], weight=0)
        self.password_frame.columnconfigure([0, 1], weight=1, uniform="columns")

        # Error display label
        self.error_label_sv = ctk.StringVar()
        self.error_label = SmallLabel(self,
                                      textvariable=self.error_label_sv,
                                      text_color=ERROR_TEXT_COLOR,
                                      wraplength=LOGIN_WIDTH - (DEFAULT_PAD * 2),
                                      anchor="nw",
                                      justify="left")
        self.error_label.grid(row=6, column=0, columnspan=3, sticky="nsew", pady=(0, DEFAULT_PAD), padx=DEFAULT_PAD)

        # Register button
        self.register_button = ctk.CTkButton(self,
                                             text="Register",
                                             font=ctk.CTkFont(**NORMAL_LABEL_FONT),
                                             border_spacing=5,
                                             )
        self.register_button.grid(row=7, column=1, sticky="ew", pady=(0, DEFAULT_PAD), padx=(0, DEFAULT_PAD))

        # Cancel button
        self.cancel_button = ctk.CTkButton(self,
                                           text="Cancel",
                                           font=ctk.CTkFont(**NORMAL_LABEL_FONT),
                                           border_spacing=5,
                                           command=self.back_button_pressed)
        self.cancel_button.grid(row=7, column=2, sticky="ew", pady=(0, DEFAULT_PAD), padx=(0, DEFAULT_PAD))

        self.rowconfigure([0, 1, 2, 3, 4, 5, 7], weight=0)
        self.rowconfigure(6, weight=1)
        self.columnconfigure([0, 1, 2], weight=1, uniform="columns")

    def back_button_pressed(self):
        self.master.show_frame("login")
