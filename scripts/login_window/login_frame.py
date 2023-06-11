import customtkinter as ctk
from ..components import TitleLabel, SingleLineEntry, NormalLabel, SmallLabelButton, SmallLabel, SecondaryButton
from ..settings import *
from ..database import RUNNING_DB


class LoginFrame(ctk.CTkFrame):
    """
    This class runs the login frame of the login window. Allows the user to enter their email and password, and requests
    authorisation when the login button is clicked. Will display appropriate error messages on unsuccessful requests,
    or when local validation is run. The frame also allows users to select the option to create an account.
    """
    def __init__(self, master, user_accepted: ctk.BooleanVar) -> None:
        super().__init__(master,
                         fg_color="transparent")

        # User accepted bool is tracked by root app, decides if root should destroy itself (login cancelled) or
        #  deiconify (login successful)
        self.user_accepted = user_accepted

        # Title of the frame
        self.title_bar = TitleLabel(self,
                                    "Login")
        self.title_bar.grid(row=0, column=0, columnspan=3, sticky="w", pady=(DEFAULT_PAD, 35), padx=DEFAULT_PAD)

        # Email entry
        self.email_label = NormalLabel(self,
                                       text="Email address",
                                       anchor="sw")
        self.email_label.grid(row=1, column=0, columnspan=3, sticky="nsew", pady=(0, DEFAULT_PAD), padx=DEFAULT_PAD)

        self.email_entry = SingleLineEntry(self,
                                           placeholder_text="Type email here...")
        self.email_entry.grid(row=2, column=0, columnspan=3, sticky="new", pady=(0, DEFAULT_PAD+20), padx=DEFAULT_PAD)

        # Password entry
        self.password_label = NormalLabel(self,
                                          text="Password",
                                          anchor="sw")
        self.password_label.grid(row=3, column=0, columnspan=3, sticky="nsew", pady=(0, DEFAULT_PAD), padx=DEFAULT_PAD)

        self.password_entry = SingleLineEntry(self,
                                              placeholder_text="Type password here...",
                                              show="•")
        self.password_entry.grid(row=4, column=0, columnspan=3, sticky="new", pady=(0, DEFAULT_PAD), padx=DEFAULT_PAD)

        # Register button
        self.register_button = SmallLabelButton(self,
                                                text="Register account",
                                                width=5,
                                                command=self.register_account)
        self.register_button.grid(row=5, column=1, columnspan=2, sticky="ne", pady=(0, DEFAULT_PAD), padx=DEFAULT_PAD)

        # Error display label
        self.error_label_sv = ctk.StringVar()
        self.error_label = SmallLabel(self,
                                      textvariable=self.error_label_sv,
                                      text_color=ERROR_TEXT_COLOR,
                                      wraplength=LOGIN_WIDTH-(DEFAULT_PAD*2),
                                      anchor="nw",
                                      justify="left")
        self.error_label.grid(row=6, column=0, columnspan=3, sticky="nsew", pady=(0, DEFAULT_PAD), padx=DEFAULT_PAD)

        # Login button
        self.login_button = ctk.CTkButton(self,
                                          text="Login",
                                          font=ctk.CTkFont(**NORMAL_LABEL_FONT),
                                          border_spacing=5,
                                          command=self.login_request)
        self.login_button.grid(row=7, column=1, sticky="ew", pady=(0, DEFAULT_PAD), padx=(0, DEFAULT_PAD))

        # Cancel button
        self.cancel_button = SecondaryButton(self,
                                             text="Cancel",
                                             font=ctk.CTkFont(**NORMAL_LABEL_FONT),
                                             border_spacing=5,
                                             command=self.cancel_login)
        self.cancel_button.grid(row=7, column=2, sticky="ew", pady=(0, DEFAULT_PAD), padx=(0, DEFAULT_PAD))

        self.rowconfigure([0, 1, 2, 3, 4, 5, 7], weight=0)
        self.rowconfigure([6], weight=1, uniform="rows")
        self.columnconfigure([0, 1, 2], weight=1, uniform="columns")

        self.email_entry.bind("<Return>", lambda event: self.login_request())
        self.password_entry.bind("<Return>", lambda event: self.login_request())

    def login_request(self) -> None:
        """
        Collects the input email and password, performs basic validation, and requests authorisation from the database.
        Will set the user_accepted attribute to true if authorisation is granted, and destroy the login window. Sets
        the error label to an appropriate message if authorisation is not granted.
        :return: None
        """

        # Collect email and passwords from entry widgets
        current_email = self.email_entry.get()
        current_password = self.password_entry.get()

        # Basic input validation for password and email is performed. If it fails the checks, the error label is updated
        #  and the function is stopped
        if "@" not in current_email or "." not in current_email:
            self.error_label_sv.set("Not a valid email address")
            return
        else:
            self.error_label_sv.set("")

        if len(current_password) < 0 or len(current_password) > 72:
            self.error_label_sv.set("Your password should be between 8 and 72 characters long")

        # While waiting for database, set cursor to watch to make clear work is happening behind the scenes
        self.configure(cursor="watch")

        # Run request function in after() to allow cursor change to render
        self.after(500, lambda: self.make_db_request(current_email, current_password))

    def cancel_login(self) -> None:
        """
        If the cancel button is clicked, the login window self-destructs
        :return: None
        """
        self.user_accepted.set(False)
        self.master.destroy()

    def register_account(self) -> None:
        self.master.show_frame("register")

    def make_db_request(self, email, password) -> None:
        # A request is made to the database
        response = RUNNING_DB.login(email, password)

        # After response is received, reset cursor
        self.configure(cursor="arrow")

        # Depending on the type of response, the login window self-destructs (successful login), or updates the error
        #  label and allows the user to try again
        if response["response"]:
            self.user_accepted.set(True)
            self.master.destroy()
        else:
            self.user_accepted.set(False)
            self.error_label_sv.set(response["message"])
