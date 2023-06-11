import customtkinter as ctk
from ..settings import *


class SmallLabel(ctk.CTkLabel):
    def __init__(self, master, **kwargs):
        super().__init__(master,
                         fg_color="transparent",
                         font=ctk.CTkFont(**SMALL_LABEL_FONT),
                         **kwargs)
