import customtkinter as ctk
from tkinter import Menu, Event
from ..settings import *


class ListCard(ctk.CTkFrame):
    def __init__(self, master,
                 fg_color=LABEL_CARD_COLOR,
                 hover_color=LABEL_CARD_HOVER_COLOR,
                 selected_color=LABEL_CARD_SELECTED_COLOR,
                 height=98,
                 click_command=None,
                 **kwargs):
        super().__init__(master,
                         height=height,
                         fg_color=fg_color,
                         **kwargs)

        self.card_data = None

        # When griding widgets into the list card, the card will not propagate and stay the same fixed size
        self.grid_propagate(False)
        self.command = click_command
        self.hover_color = hover_color
        self.main_color = fg_color
        self.selected_color = selected_color

        self.selected: bool = False

        self.right_click_menu = Menu(self, tearoff=False)

        self.bind("<Enter>", lambda event: self.on_hover())
        self.bind("<Leave>", lambda event: self.on_mouse_leave())
        self.bind("<Button-1>", lambda event: self.command(self.card_data))
        self.bind("<Button-3>", self.right_clicked)

    def right_clicked(self, event: Event):
        self.right_click_menu.tk_popup(event.x_root, event.y_root)

    def on_hover(self):
        if not self.selected:
            self.configure(fg_color=self.hover_color)

    def on_mouse_leave(self):
        if not self.selected:
            self.configure(fg_color=self.main_color)

    def bind_frame(self):
        for child in self.winfo_children():
            child.bind("<Enter>", lambda event: self.on_hover())
            child.bind("<Leave>", lambda event: self.on_mouse_leave())
            child.bind("<Button-3>", self.right_clicked)

            if self.command is not None:
                child.bind("<Button-1>", lambda event: self.command(self.card_data))

    def card_selected(self):
        self.selected = True
        self.configure(fg_color=LABEL_CARD_SELECTED_COLOR)

    def card_deselected(self):
        self.selected = False
        self.configure(fg_color=self.main_color)
