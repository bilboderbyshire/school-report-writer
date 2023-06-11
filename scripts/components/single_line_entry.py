import customtkinter as ctk
from ..settings import *


class SingleLineEntry(ctk.CTkEntry):
    def __init__(self, master, **kwargs):
        super().__init__(master,
                         height=40,
                         font=ctk.CTkFont(**ENTRY_FONT),
                         **kwargs)