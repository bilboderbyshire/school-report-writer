import customtkinter as ctk
from ..components import AutohidingScrollableAndLoadingFrame
from ..settings import *
from .copy_template_from_toplevel_listcard import CTFTLListCard
from typing import Callable


class SelectionColumnScrollframe(AutohidingScrollableAndLoadingFrame):
    def __init__(self, master,
                 label_text: str,
                 card_selected_command: Callable):
        super().__init__(master,
                         label_font=ctk.CTkFont(**NORMAL_LABEL_FONT),
                         label_anchor="w",
                         label_fg_color="transparent",
                         label_text=label_text,
                         fg_color=LABEL_CARD_COLOR)

        self.all_cards: dict[str, CTFTLListCard] = {}
        self.card_selected_command = card_selected_command
        self.currently_selected: str | None = None
        self.total_selected: int = 0

    def populate_cards(self, card_items: dict[str, str] | None):
        for i in self.winfo_children():
            i.destroy()

        self.all_cards = {}
        self.currently_selected: str | None = None
        self.total_selected: int = 0

        if card_items is None or len(card_items.keys()) == 0:
            return

        current_row = 0
        for card_id, card_text in card_items.items():
            new_card = CTFTLListCard(
                self,
                card_selected=self.card_selected_command,
                card_id=card_id,
                card_text=card_text,

            )
            new_card.grid(row=current_row, column=0, sticky="nsew", padx=SMALL_PAD)
            self.all_cards[card_id] = new_card

            current_row += 1

        self.rowconfigure("all", weight=0)
        self.columnconfigure(0, weight=1)

    def card_selected(self, card_id: str):
        if self.currently_selected is not None:
            self.all_cards[self.currently_selected].card_deselected()

        self.currently_selected = card_id

        self.all_cards[self.currently_selected].card_selected()

    def compound_card_selected(self, card_id: str):
        if self.all_cards[card_id].selected:
            self.all_cards[card_id].card_deselected()
            self.total_selected -= 1
        else:
            self.all_cards[card_id].card_selected()
            self.total_selected += 1
