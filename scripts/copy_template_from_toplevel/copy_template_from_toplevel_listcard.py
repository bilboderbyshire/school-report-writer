from ..components import ListCard
import customtkinter as ctk
from ..settings import *
from typing import Callable


class CTFTLListCard(ListCard):
    def __init__(self, master,
                 card_selected: Callable,
                 card_id: str,
                 card_text: str):
        super().__init__(master,
                         height=30,
                         click_command=card_selected)

        self.card_data = card_id
        self.grid_propagate(True)

        self.label = ctk.CTkLabel(
            self,
            text=card_text,
            font=ctk.CTkFont(**SMALL_LABEL_FONT),
            fg_color="transparent",
            justify="left",
            anchor="w",
            pady=0,
            padx=0
        )
        self.label.grid(row=0, column=0, sticky="nsew", **SMALL_PAD_COMPLETE)
        self.rowconfigure(0, weight=0)
        self.columnconfigure(0, weight=1)

        self.bind_frame()
        self.bind("<Configure>", lambda event: self.configure_label_width())

    def configure_label_width(self):
        self.update_idletasks()
        self.label.configure(wraplength=self.label._current_width)
