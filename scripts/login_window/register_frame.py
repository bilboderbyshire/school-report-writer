import customtkinter as ctk
from ..components import TitleLabel, SingleLineEntry, NormalLabel, SmallLabelButton, SmallLabel, SecondaryButton
from ..settings import *
from ..database import RUNNING_DB


class RegisterFrame(ctk.CTkFrame):
    """This frame allows the user to create a new account, by inputting their details and making a create request to the
    database. Basic local validation is performed to ensure all the information is good. If successful, the user is
    logged in, and the main menu is displayed. If not successful, an error label is updated with an appropriate
    message, and the user is given another chance"""
    def __init__(self, master, user_accepted: ctk.BooleanVar) -> None:
        super().__init__(master,
                         fg_color="transparent")

        # User accepted bool is tracked by root app, decides if root should destroy itself (registration cancelled) or
        #  deiconify (registration successful)
        self.user_accepted = user_accepted

        self.__build_frame()

    def __build_frame(self) -> None:
        """Private function keeps all build code in the same place"""

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

        # Name entry frame
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

        # Password entry frame
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
                                             command=self.register_account)
        self.register_button.grid(row=7, column=1, sticky="ew", pady=(0, DEFAULT_PAD), padx=(0, DEFAULT_PAD))

        # Back button
        self.back_button = SecondaryButton(self,
                                           text="Back",
                                           font=ctk.CTkFont(**NORMAL_LABEL_FONT),
                                           border_spacing=5,
                                           command=self.back_button_pressed)
        self.back_button.grid(row=7, column=2, sticky="ew", pady=(0, DEFAULT_PAD), padx=(0, DEFAULT_PAD))

        self.rowconfigure([0, 1, 2, 3, 4, 5, 7], weight=0)
        self.rowconfigure(6, weight=1)
        self.columnconfigure([0, 1, 2], weight=1, uniform="columns")

        all_entries = [self.forename_entry, self.surname_entry, self.email_entry,
                       self.password_entry, self.password_confirm_entry]

        for i in all_entries:
            i.bind("<Return>", lambda event: self.register_account())

    def back_button_pressed(self) -> None:
        """
        When either back button is pressed, the login frame is displayed
        :return: None
        """
        self.master.show_frame("login")

    def register_account(self) -> None:
        """
        A record is created based off of all the data inputs, a basic input validation is performed on the relevant
        pieces of data. If a validation fails, an appropriate error message is displayed and the user continues to edit.
        If the validations pass, a create request is made to the database. If the request is successful, the login top
        level self-destructs, and the main menu is displayed. If the request fails, a relevant error message is provided
        :return: None
        """
        data = {
            "forename": self.forename_entry.get().capitalize(),
            "surname": self.surname_entry.get().capitalize(),
            "email": self.email_entry.get().lower(),
            "emailVisibility": True,
            "password": self.password_entry.get(),
            "passwordConfirm": self.password_confirm_entry.get()
        }

        # Presence check for all inputs
        for key, value in data.items():
            if key != "emailVisibility" and len(value) == 0:
                if key != "passwordConfirm":
                    self.error_label_sv.set(f"{key.capitalize()} cannot be empty")
                else:
                    self.error_label_sv.set("Password confirm cannot be empty")
                return

        # Type check for names
        acceptable_name_chars = "abcdefghijklmnopqrstuvwxyz -'"
        for i in ["forename", "surname"]:
            for j in data[i].lower():
                if j not in acceptable_name_chars:
                    self.error_label_sv.set(f"{i.capitalize()} cannot contain illegal characters: {j}")
                    return

        # Format check for email
        if "@" not in data["email"] or "." not in data["email"]:
            self.error_label_sv.set("Invalid email")
            return

        # Length check for password, based off of what is required by the database
        if len(data["password"]) < 8 or len(data["password"]) > 72:
            self.error_label_sv.set("Password must be between 8 and 72 characters")
            return

        # Match check for passwords
        if data["password"] != data["passwordConfirm"]:
            self.error_label_sv.set("Passwords don't match")
            return

        # Cursor set to watch to make clear work is happening in the background
        self.configure(cursor="watch")

        # A request is sent to the database. An after is used to allow cursor to change while waiting
        self.after(500, lambda: self.make_db_request(data))

    def make_db_request(self, data) -> None:
        response = RUNNING_DB.register_account(data)

        # After response is received, reset cursor
        self.configure(cursor="arrow")

        # If the database response is successful, the login top level self-destructs. Otherwise, the response error
        #  message is given to the user, and they are given another chance
        if response["response"]:
            self.user_accepted.set(True)
            self.master.destroy()
        else:
            self.user_accepted.set(False)
            self.error_label_sv.set(response["message"])
