import customtkinter as ctk
from ..settings import *
from ..components import AutohidingScrollableAndLoadingFrame
from .option_list_card import OptionListCard


class VariableOptionsScrollframe(AutohidingScrollableAndLoadingFrame):
    def __init__(self, master, options_list: list[str]):
        super().__init__(master,
                         label_font=ctk.CTkFont(**NORMAL_LABEL_FONT),
                         label_anchor="w",
                         label_fg_color="transparent",
                         label_text="Options:")

        self.options_list = options_list
        self.all_cards: dict[int, OptionListCard] = {}

        self.frame_disabled: bool = False

        for index, value in enumerate(options_list):
            new_card = OptionListCard(
                self,
                card_id=index,
                card_text=value,
                add_option_command=self.add_option_command,
                delete_option_command=self.delete_option_command
            )
            new_card.grid(row=index, column=0, sticky="nsew", padx=SMALL_PAD, pady=(0, SMALL_PAD))
            self.all_cards[index] = new_card

        self.add_option_button = self.make_add_card_button(self.add_option_command, "+ Add new...")
        self.add_option_button.grid(row=len(self.all_cards.keys()), column=0, sticky="nsew", padx=SMALL_PAD,
                                    pady=(0, SMALL_PAD))

        self.columnconfigure(0, weight=1)

        self.update()
        self.after(150, self.check_scrollbar_needed)

    def add_option_command(self, _):
        new_id = max(list(self.all_cards.keys()), default=-1) + 1
        new_card = OptionListCard(
            self,
            card_id=new_id,
            add_option_command=self.add_option_command,
            delete_option_command=self.delete_option_command
        )
        self.all_cards[new_id] = new_card

        self.add_option_button.grid(row=new_id+1, column=0, sticky="nsew", padx=SMALL_PAD, pady=(0, SMALL_PAD))
        new_card.grid(row=new_id, column=0, sticky="nsew", padx=SMALL_PAD, pady=(0, SMALL_PAD))
        self.check_scrollbar_needed()

        new_card.edit_text()

    def delete_option_command(self, card_id: int):
        card_to_delete = self.all_cards.pop(card_id)
        card_to_delete.destroy()

    def disabled(self):
        if not self.frame_disabled:
            self.add_option_button.grid_remove()
            self.check_scrollbar_needed()

            for card in self.all_cards.values():
                card.card_disabled()

            self.configure(label_text_color=DISABLED_TEXT_COLOR)
            self.frame_disabled = True

    def enabled(self):
        if self.frame_disabled:
            self.add_option_button.grid()

            self.check_scrollbar_needed()

            for card in self.all_cards.values():
                card.card_enabled()

            self.configure(label_text_color=STANDARD_TEXT_COLOR)
            self.frame_disabled = False
