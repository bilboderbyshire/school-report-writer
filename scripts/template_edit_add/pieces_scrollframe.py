import customtkinter as ctk
from ..settings import *
from ..components import AutohidingScrollableAndLoadingFrame, ListCard
from ..containers import IndividualPiece
from .pieces_list_card import PieceListCard
from typing import Callable


class PiecesScrollableFrame(AutohidingScrollableAndLoadingFrame):
    def __init__(self, master,
                 structured_pieces: dict[int, dict[str, IndividualPiece]],
                 select_piece_command: Callable,
                 card_add_command: tuple[str, Callable],
                 card_delete_command: tuple[str, Callable],
                 card_copy_command: tuple[str, Callable]):
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
        self.card_copy = card_copy_command

        self.all_cards: dict[str, PieceListCard] = {}

    def build_pieces_frame(self, section: int | None = None):
        for i in self.winfo_children():
            i.destroy()

        self.update_idletasks()

        if section is None:
            self.all_cards = {}
            return

        for index, piece in enumerate(self.structured_pieces[section].values()):
            new_piece_card = PieceListCard(self,
                                           piece,
                                           select_piece_command=self.select_piece_command,
                                           card_add=self.card_add,
                                           card_delete=self.card_delete,
                                           card_copy=self.card_copy)
            self.all_cards[piece.id] = new_piece_card
            new_piece_card.grid(row=index, column=0, sticky="ew", padx=DEFAULT_PAD-7)

        add_piece = self.make_add_piece_button()
        add_piece.grid(row=len(self.structured_pieces[section].values()) + 1, column=0, sticky="ew", padx=DEFAULT_PAD-7,
                       pady=(0, DEFAULT_PAD))

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=0)

    def make_add_piece_button(self) -> ListCard:
        add_piece_button = ListCard(
            self,
            fg_color="transparent",
            height=30,
            click_command=self.card_add[1])

        add_button_text = ctk.CTkLabel(
            add_piece_button,
            text=f"+ Add new piece...",
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
