from typing import Literal

import customtkinter as ctk
from ..settings import *


class Separator(ctk.CTkFrame):
    def __init__(self, master,
                 orientation: Literal["hor", "ver"],
                 thickness: int = 2,
                 fg_color=SEPERATOR_COLOR,):
        super().__init__(master,
                         fg_color=fg_color,
                         border_width=0)

        if orientation == "hor":
            self.configure(height=thickness)
        else:
            self.configure(width=thickness)
