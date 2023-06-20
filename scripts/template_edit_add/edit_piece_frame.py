import customtkinter as ctk
from ..settings import *
from ..containers import IndividualPiece
from typing import Callable


class EditPieceFrame(ctk.CTkFrame):
    def __init__(self,
                 master,
                 edit_command: Callable):
        super().__init__(master)

        self.current_piece: IndividualPiece | None = None

        title_label = ctk.CTkLabel(
            self,
            font=ctk.CTkFont(**NORMAL_LABEL_FONT),
            anchor="w",
            fg_color="transparent",
            text="Edit piece")

        title_label.grid(row=0, column=0, sticky="nw", padx=13, pady=(5, 6))

        self.piece_textbox = ctk.CTkTextbox(
            self,
            font=ctk.CTkFont(**SMALL_LABEL_FONT),
            fg_color="transparent",
            border_width=2,
            wrap="word",
            undo=True,
        )
        self.piece_textbox.grid(row=1, column=0, sticky="nsew", padx=13, pady=DEFAULT_PAD)

        self.piece_textbox.bind("<KeyRelease>", lambda event: edit_command(self.current_piece,
                                                                           self.piece_textbox.get("1.0", "end")))

        self.rowconfigure(0, weight=0)
        self.rowconfigure([1, 2], weight=1, uniform="rows")
        self.columnconfigure(0, weight=1)

    def display_piece(self, piece: IndividualPiece | None):
        if piece is not None:
            self.current_piece = piece
            self.piece_textbox.delete("1.0", "end")
            self.piece_textbox.insert("1.0", self.current_piece.piece_text)
            self.piece_textbox.focus_set()
        else:
            self.piece_textbox.delete("1.0", "end")
