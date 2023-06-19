import customtkinter as ctk
from ..settings import *
from ..components import AutohidingScrollableAndLoadingFrame, ListCard
from ..containers import IndividualPiece
from .section_list_card import SectionCard
from typing import Callable


class SectionScrollableFrame(AutohidingScrollableAndLoadingFrame):
    def __init__(self, master,
                 structured_pieces: dict[int, dict[str, IndividualPiece]],
                 select_section_command: Callable,
                 card_add_command: tuple[str, Callable],
                 card_delete_command: tuple[str, Callable]):
        super().__init__(master,
                         fg_color=ROOT_BG,
                         label_font=ctk.CTkFont(**NORMAL_LABEL_FONT),
                         label_anchor="w",
                         label_fg_color="transparent",
                         label_text="Sections")

        self.structured_pieces = structured_pieces
        self.select_section_command = select_section_command
        self.card_add = card_add_command
        self.card_delete = card_delete_command
        self.all_cards: dict[int, SectionCard] = {}

    def build_section_frame(self):
        for i in self.winfo_children():
            i.destroy()

        self.update_idletasks()

        for index, section in enumerate(self.structured_pieces.keys()):
            new_section_card = SectionCard(
                self,
                section,
                len(self.structured_pieces[section]),
                select_section_command=self.select_section_command,
                add_command=self.card_add,
                delete_command=self.card_delete
            )
            self.all_cards[section] = new_section_card
            new_section_card.grid(row=index, column=0, sticky="ew", padx=DEFAULT_PAD-7)

        add_section = self.make_add_section_button()
        add_section.grid(row=len(self.structured_pieces.keys()) + 1, column=0, sticky="ew", padx=DEFAULT_PAD-7,
                         pady=(0, DEFAULT_PAD))

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=0)

    def make_add_section_button(self) -> ListCard:
        add_section_button = ListCard(
            self,
            fg_color="transparent",
            hover_color=BUTTON_HOVER_COLOR,
            height=30,
            click_command=self.card_add[1])

        add_button_text = ctk.CTkLabel(
            add_section_button,
            text=f"+ Add new section...",
            font=ctk.CTkFont(**SMALL_LABEL_FONT, slant="italic"),
            fg_color="transparent",
            anchor="w",
            pady=0,
            padx=0
        )

        add_button_text.grid(row=0, column=0, sticky="ew", padx=DEFAULT_PAD)
        add_section_button.rowconfigure(0, weight=1)
        add_section_button.columnconfigure(0, weight=1)
        add_section_button.bind_frame()

        return add_section_button
