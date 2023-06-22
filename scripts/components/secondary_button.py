import customtkinter as ctk
from ..settings import *


class SecondaryButton(ctk.CTkButton):
    def __init__(self, master,
                 fg_color=SECONDARY_BUTTON_FG_COLOR,
                 hover_color=SECONDARY_BUTTON_HOVER_COLOR,
                 text_color=SECONDARY_BUTTON_TEXT_COLOR,
                 **kwargs):
        super().__init__(master,
                         fg_color=fg_color,
                         hover_color=hover_color,
                         text_color=text_color,
                         text_color_disabled="#737A82",
                         **kwargs)
