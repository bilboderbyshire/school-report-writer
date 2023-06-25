import customtkinter as ctk
from ..components import AutohidingScrollableAndLoadingFrame
from ..settings import *


class SelectionColumnScrollframe(AutohidingScrollableAndLoadingFrame):
    def __init__(self, master,
                 label_text: str):
        super().__init__(master,
                         label_font=ctk.CTkFont(**NORMAL_LABEL_FONT),
                         label_anchor="w",
                         label_fg_color="transparent",
                         label_text=label_text,
                         fg_color=LABEL_CARD_COLOR)

