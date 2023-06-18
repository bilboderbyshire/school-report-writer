import customtkinter as ctk
from ..settings import *


class TitleLabel(ctk.CTkLabel):
    def __init__(self, master, title_text: str, anchor="w"):
        super().__init__(master,
                         text=title_text,
                         font=ctk.CTkFont(**TITLE_FONT),
                         anchor=anchor)