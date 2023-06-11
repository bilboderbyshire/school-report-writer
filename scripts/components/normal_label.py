import customtkinter as ctk
from ..settings import *


class NormalLabel(ctk.CTkLabel):
    def __init__(self, master, **kwargs):
        super().__init__(master,
                         font=ctk.CTkFont(**NORMAL_LABEL_FONT),
                         **kwargs)

