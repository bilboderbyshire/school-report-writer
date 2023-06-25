import customtkinter as ctk
from ..settings import *
from ..components import AutohidingScrollableAndLoadingFrame
from ..containers import IndividualPiece
from .pieces_list_card import PieceListCard
from typing import Callable


class PiecesScrollableFrame(AutohidingScrollableAndLoadingFrame):
    def __init__(self, master,
                 structured_pieces: dict[str, dict[str, IndividualPiece]],
                 select_piece_command: Callable,
                 card_add_command: tuple[str, Callable],
                 card_delete_command: tuple[str, Callable],
                 card_duplicate_command: tuple[str, Callable]):
        super().__init__(master,
                         label_font=ctk.CTkFont(**NORMAL_LABEL_FONT),
                         label_anchor="w",
                         label_fg_color="transparent",
                         label_text="Pieces")

        self.configure(border_color=self.cget("fg_color"))

        self.structured_pieces = structured_pieces
        self.select_piece_command = select_piece_command
        self.card_add = card_add_command
        self.card_delete = card_delete_command
        self.card_duplicate = card_duplicate_command

        self.current_max_row = -1

        self.all_cards: dict[str, PieceListCard] = {}

        self.add_piece_button = None

    def build_pieces_frame(self, section: str | None = None):
        self.all_cards = {}
        self.current_max_row = -1
        for i in self.winfo_children():
            i.destroy()

        self.update_idletasks()

        if section is None:
            return

        self.add_piece_button = self.make_add_card_button(
            add_command=self.card_add[1],
            text="+ Add new..."
        )

        for index, piece in enumerate(self.structured_pieces[section].values()):
            new_piece_card = PieceListCard(self,
                                           piece,
                                           select_piece_command=self.select_piece_command,
                                           card_add=self.card_add,
                                           card_delete=self.card_delete,
                                           card_duplicate=self.card_duplicate)
            self.all_cards[piece.id] = new_piece_card
            new_piece_card.grid(row=index, column=0, sticky="ew", padx=DEFAULT_PAD-7)
            self.current_max_row += 1

        self.add_piece_button.grid(
            row=self.current_max_row + 1,
            column=0,
            sticky="ew",
            padx=DEFAULT_PAD-7,
            pady=(0, DEFAULT_PAD))

        self.columnconfigure(0, weight=1)
        self.rowconfigure("all", weight=0)

        self.update_all_text_displays()

    def update_all_text_displays(self):
        for card in self.all_cards.values():
            card.update_display_text()

    def add_card(self, piece_to_add: IndividualPiece):
        new_piece_card = PieceListCard(self,
                                       piece=piece_to_add,
                                       select_piece_command=self.select_piece_command,
                                       card_add=self.card_add,
                                       card_delete=self.card_delete,
                                       card_duplicate=self.card_duplicate)

        self.all_cards[piece_to_add.id] = new_piece_card

        self.current_max_row += 1
        self.add_piece_button.grid(
            row=self.current_max_row + 1,
            column=0,
            sticky="ew",
            padx=DEFAULT_PAD - 7,
            pady=(0, DEFAULT_PAD))

        new_piece_card.grid(
            row=self.current_max_row,
            column=0,
            sticky="ew",
            padx=DEFAULT_PAD - 7)

        new_piece_card.update_display_text()

    def delete_card(self, card_to_delete: IndividualPiece):
        deleted_card = self.all_cards[card_to_delete.id]
        deleted_card.destroy()
