import customtkinter as ctk
from ..settings import *


class SecondaryOptionmenu(ctk.CTkOptionMenu):
    def __init__(self, master, font=None, **kwargs):
        if font is None:
            font = ctk.CTkFont(**SMALL_LABEL_FONT)

        super().__init__(master,
                         fg_color=SECONDARY_OPTIONMENU_FG_COLOR,
                         text_color=SECONDARY_BUTTON_TEXT_COLOR,
                         button_color=SECONDARY_BUTTON_FG_COLOR,
                         button_hover_color=SECONDARY_BUTTON_HOVER_COLOR,
                         font=font,
                         **kwargs
                         )