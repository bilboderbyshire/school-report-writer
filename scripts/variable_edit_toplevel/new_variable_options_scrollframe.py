import customtkinter as ctk
from ..settings import *
from ..components import AutohidingScrollableAndLoadingFrame, ListCard
from .option_list_card import OptionListCard


class VariableOptionsScrollframe(AutohidingScrollableAndLoadingFrame):
    def __init__(self, master, options_list: list[str]):
        super().__init__(master)

        self.options_list = options_list
        self.all_cards: dict[int, ListCard] = {}

        for index, value in enumerate(options_list):
            new_card = OptionListCard(
                self,
                card_id=index,
                card_text=value,
                add_option_command=self.add_option_command,
                delete_option_command=self.delete_option_command
            )
            new_card.grid(row=index, column=0, sticky="nsew", padx=SMALL_PAD, pady=(SMALL_PAD, 0))
            self.all_cards[index] = new_card

        self.add_option_button = self.make_add_option_button()
        self.add_option_button.grid(row=len(self.all_cards.keys()), column=0, sticky="nsew", **SMALL_PAD_COMPLETE)

        self.columnconfigure(0, weight=1)

        self.update()
        self.after(150, self.check_scrollbar_needed)

        self._parent_canvas.bind("<Button-1>", lambda event: self.focus_set())
        self._parent_frame.bind("<Button-1>", lambda event: self.focus_set())

    def make_add_option_button(self) -> ListCard:
        add_option_button = ListCard(
            self,
            fg_color="transparent",
            height=30,
            click_command=self.add_option_command)

        add_button_text = ctk.CTkLabel(
            add_option_button,
            text=f"+ Add new option...",
            font=ctk.CTkFont(**SMALL_LABEL_FONT, slant="italic"),
            fg_color="transparent",
            anchor="w",
            pady=0,
            padx=0
        )

        add_button_text.grid(row=0, column=0, sticky="ew", padx=DEFAULT_PAD)
        add_option_button.rowconfigure(0, weight=1)
        add_option_button.columnconfigure(0, weight=1)
        add_option_button.bind_frame()

        return add_option_button

    def add_option_command(self, _):
        new_id = max(list(self.all_cards.keys()), default=-1) + 1
        new_card = OptionListCard(
            self,
            card_id=new_id,
            add_option_command=self.add_option_command,
            delete_option_command=self.delete_option_command
        )
        self.all_cards[new_id] = new_card

        self.add_option_button.grid(row=new_id+1, column=0, sticky="nsew", **SMALL_PAD_COMPLETE)
        new_card.grid(row=new_id, column=0, sticky="nsew", padx=SMALL_PAD, pady=(SMALL_PAD, 0))
        self.check_scrollbar_needed()

        new_card.edit_text()

    def delete_option_command(self, card_id: int):
        card_to_delete = self.all_cards.pop(card_id)
        card_to_delete.destroy()


