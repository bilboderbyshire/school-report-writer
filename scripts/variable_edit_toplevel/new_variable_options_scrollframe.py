import customtkinter as ctk
from ..settings import *
from ..components import AutohidingScrollableAndLoadingFrame, ListCard
from .option_list_card import OptionListCard


class VariableOptionsScrollframe(AutohidingScrollableAndLoadingFrame):
    def __init__(self, master, options_list: list[str]):
        super().__init__(master)

        # self.card_add = card_add_command
        # self.card_delete = card_delete_command
        self.options_list = options_list
        self.all_cards: dict[str, ListCard] = {}

        new_card = OptionListCard(self)
        new_card.grid(row=0, column=0, sticky="nsew", **SMALL_PAD_COMPLETE)

        self.rowconfigure(0, weight=0)
        self.columnconfigure(0, weight=1)

        self.update()
        self.after(150, self.check_scrollbar_needed)
    def make_add_piece_button(self) -> ListCard:
        add_piece_button = ListCard(
            self,
            fg_color="transparent",
            height=30,
            click_command=self.card_add[1])

        add_button_text = ctk.CTkLabel(
            add_piece_button,
            text=f"+ Add new option...",
            font=ctk.CTkFont(**SMALL_LABEL_FONT, slant="italic"),
            fg_color="transparent",
            anchor="w",
            pady=0,
            padx=0
        )

        add_button_text.grid(row=0, column=0, sticky="ew", padx=DEFAULT_PAD)
        add_piece_button.rowconfigure(0, weight=1)
        add_piece_button.columnconfigure(0, weight=1)
        add_piece_button.bind_frame()

        return add_piece_button
