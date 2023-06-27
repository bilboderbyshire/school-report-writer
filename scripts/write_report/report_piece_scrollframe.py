import customtkinter as ctk
from ..settings import *
from ..components import AutohidingScrollableAndLoadingFrame
from ..containers import IndividualPiece
from .report_piece_list_card import ReportPieceListCard


class ReportPieceScrollframe(AutohidingScrollableAndLoadingFrame):
    def __init__(self,
                 master):
        super().__init__(master,
                         fg_color=LABEL_CARD_COLOR)

        self.all_cards: dict[str, ReportPieceListCard] = {}
        self.current_max_row = -1

    def build_pieces_frame(self, dict_of_pieces: dict[str, IndividualPiece]):
        for i in self.winfo_children():
            i.destroy()

        self.all_cards = {}
        self.current_max_row = -1

        for index, piece in enumerate(dict_of_pieces.values()):
            new_card = ReportPieceListCard(self, piece)
            new_card.grid(row=index, column=0, sticky="nsew", padx=(0, SMALL_PAD), pady=(0, DEFAULT_PAD))

            self.current_max_row += 1
            self.all_cards[piece.id] = new_card

        self.rowconfigure("all", weight=0)
        self.columnconfigure(0, weight=1)
