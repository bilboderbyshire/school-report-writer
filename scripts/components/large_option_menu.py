import customtkinter as ctk
from ..settings import *


class LargeOptionMenu(ctk.CTkOptionMenu):
    def __init__(self, master,
                 fg_color=LABEL_CARD_COLOR,
                 hover_color=LABEL_CARD_HOVER_COLOR,
                 **kwargs):
        super().__init__(master,
                         fg_color=fg_color,
                         button_color=fg_color,
                         button_hover_color=hover_color,
                         font=ctk.CTkFont(**NORMAL_LABEL_FONT),
                         dropdown_font=ctk.CTkFont(**SMALL_LABEL_FONT),
                         **kwargs)

        self.hover_color = hover_color
        self.main_color = fg_color
        self.bind("<Enter>", lambda event: self.on_hover())
        self.bind("<Leave>", lambda event: self.on_leave())

    def on_hover(self):
        self.configure(fg_color=self.hover_color, button_color=self.hover_color)

    def on_leave(self):
        self.configure(fg_color=self.main_color, button_color=self.main_color)
