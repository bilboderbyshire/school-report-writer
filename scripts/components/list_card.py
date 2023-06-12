import customtkinter as ctk
from ..settings import *
from ..containers import SingleReportSet


class ListCard(ctk.CTkFrame):
    def __init__(self, master,
                 fg_color=LABEL_CARD_COLOR, text_color=STANDARD_TEXT_COLOR,
                 hover_color=LABEL_CARD_HOVER_COLOR,
                 command=None):
        super().__init__(master,
                         height=80,
                         fg_color=fg_color)

        self.command = command
        self.hover_color = hover_color
        self.main_color = fg_color

        self.bind("<Enter>", lambda event: self.on_hover())
        self.bind("<Leave>", lambda event: self.on_mouse_leave())

        if self.command is not None:
            self.bind("<Button-1>", lambda event: self.command())

    def on_hover(self):
        self.configure(fg_color=self.hover_color)

    def on_mouse_leave(self):
        self.configure(fg_color=self.main_color)