import customtkinter as ctk
from ..settings import *
from ..containers import IndividualPiece
from ..components import AutohidingScrollableAndLoadingFrame, ListCard


class PiecesScrollableFrame(AutohidingScrollableAndLoadingFrame):
    def __init__(self, master):
        super().__init__(master,
                         label_font=ctk.CTkFont(**NORMAL_LABEL_FONT),
                         label_anchor="w",
                         label_fg_color="transparent",
                         label_text="Pieces")

        self.given_pieces_list: list[IndividualPiece] = []
        self.added_pieces: list[IndividualPiece] = []

    def build_pieces_frame(self, all_pieces_of_section: list[IndividualPiece]):
        pass

    def make_add_piece_button(self) -> ListCard:
        add_piece_button = ListCard(
            self,
            fg_color="transparent",
            hover_color=BUTTON_HOVER_COLOR,
            height=30,
            command=self.add_section)

        add_button_text = ctk.CTkLabel(
            add_piece_button,
            text=f"+ Add new section...",
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

    def add_section(self):
        self.added_pieces += 1
        self.build_pieces_frame(self.given_pieces_list)
        self.check_scrollbar_needed()