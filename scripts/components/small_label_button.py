import customtkinter as ctk
from ..settings import *


class SmallLabelButton(ctk.CTkButton):
    def __init__(self,
                 master,
                 fg_color="transparent",
                 border_spacing=3,
                 **kwargs):
        super().__init__(master,
                         fg_color=fg_color,
                         hover=False,
                         border_width=0,
                         text_color=LABEL_BUTTON_TEXT_COLOR,
                         border_spacing=border_spacing,
                         **kwargs)

        self.button_font = ctk.CTkFont(**SMALL_LABEL_FONT)
        self.configure(font=self.button_font)

        self.bind("<Enter>", lambda event: self.set_hover())
        self.bind("<Leave>", lambda event: self.unset_hover())

    def set_hover(self):
        self.button_font.configure(underline=True)
        self.configure(cursor="hand2")

    def unset_hover(self):
        self.button_font.configure(underline=False)
