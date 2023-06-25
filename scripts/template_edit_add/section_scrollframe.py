import customtkinter as ctk
from ..settings import *
from ..components import AutohidingScrollableAndLoadingFrame, ListCard
from ..containers import IndividualPiece, TemplateSection
from .section_list_card import SectionCard
from typing import Callable
from ..app_engine import AppEngine


class SectionScrollableFrame(AutohidingScrollableAndLoadingFrame):
    def __init__(self, master,
                 app_engine: AppEngine,
                 structured_pieces: dict[str, dict[str, IndividualPiece]],
                 select_section_command: Callable,
                 card_add_command: tuple[str, Callable],
                 card_delete_command: tuple[str, Callable]):
        super().__init__(master,
                         fg_color=ROOT_BG,
                         label_font=ctk.CTkFont(**NORMAL_LABEL_FONT),
                         label_anchor="w",
                         label_fg_color="transparent",
                         label_text="Sections")

        self.app_engine = app_engine
        self.structured_pieces = structured_pieces
        self.select_section_command = select_section_command
        self.card_add = card_add_command
        self.card_delete = card_delete_command
        self.all_cards: dict[str, SectionCard] = {}

        self.current_max_row = -1

        for index, section_id in enumerate(self.structured_pieces.keys()):
            new_section_card = SectionCard(
                self,
                section=self.app_engine.copy_of_section_collection[section_id],
                piece_count=len(self.structured_pieces[section_id]),
                select_section_command=self.select_section_command,
                add_command=self.card_add,
                delete_command=self.card_delete
            )
            self.all_cards[section_id] = new_section_card
            new_section_card.grid(row=index, column=0, sticky="ew", padx=DEFAULT_PAD-7)
            self.current_max_row += 1

        self.add_section_button = self.make_add_section_button()
        self.add_section_button.grid(
            row=self.current_max_row + 1,
            column=0,
            sticky="ew",
            padx=DEFAULT_PAD-7,
            pady=(0, DEFAULT_PAD)
        )

        self.columnconfigure(0, weight=1)
        self.rowconfigure("all", weight=0)

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

    def reload_card_subtitles(self):
        for section_id, card in self.all_cards.items():
            card.update_piece_count(len(self.structured_pieces[section_id]))

    def add_card(self, section_to_add: TemplateSection):
        new_section_card = SectionCard(
            self,
            section=section_to_add,
            piece_count=len(self.structured_pieces[section_to_add.id]),
            select_section_command=self.select_section_command,
            add_command=self.card_add,
            delete_command=self.card_delete
        )
        self.all_cards[section_to_add.id] = new_section_card
        self.current_max_row += 1
        self.add_section_button.grid(
            row=self.current_max_row+1,
            column=0,
            sticky="ew",
            padx=DEFAULT_PAD - 7,
            pady=(0, DEFAULT_PAD)
        )
        new_section_card.grid(row=self.current_max_row, column=0, sticky="ew", padx=DEFAULT_PAD - 7)

    def delete_card(self, section_to_delete: TemplateSection):
        deleted_card = self.all_cards.pop(section_to_delete.id)
        deleted_card.destroy()
