import customtkinter as ctk
from ..components import TitleLabel
from ..settings import *


class LoginFrame(ctk.CTkFrame):
    def __init__(self, master, user_accepted: ctk.BooleanVar):
        super().__init__(master,
                         fg_color="transparent")

        self.title_bar = TitleLabel(self,
                                    "Login")
        self.title_bar.grid(row=0, column=0, columnspan=3, stick="w", **DEFAULT_PAD_COMPLETE)
