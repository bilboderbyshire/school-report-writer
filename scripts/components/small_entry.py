import customtkinter as ctk
from ..settings import *


class SmallEntry(ctk.CTkEntry):
    def __init__(self, master,
                 fg_color="transparent",
                 text_color=STANDARD_TEXT_COLOR,
                 border_width=1,
                 font=None,
                 **kwargs):

        if font is None:
            font = ctk.CTkFont(**SMALL_LABEL_FONT)

        super().__init__(master,
                         fg_color=fg_color,
                         text_color=text_color,
                         border_width=border_width,
                         font=font,
                         **kwargs)
