import customtkinter as ctk
from ..settings import *


class WarningButton(ctk.CTkButton):
    def __init__(self, master,
                 fg_color=BAD_COLOR,
                 hover_color=BAD_COLOR_HOVERED,
                 **kwargs):
        super().__init__(master,
                         fg_color=fg_color,
                         hover_color=hover_color,
                         text_color_disabled=DISABLED_TEXT_COLOR,
                         **kwargs)
