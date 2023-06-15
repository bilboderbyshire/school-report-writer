import customtkinter as ctk
from ..settings import *
from ..components import ListCard
from ..containers import IndividualPiece


class PieceListCard(ListCard):
    def __init__(self, master, piece: IndividualPiece):
        super().__init__(master, height=30)

        self.card_data = piece

        self.piece_text = piece.piece_text
        self.card_font = ctk.CTkFont(**SMALL_LABEL_FONT)
        self.display_text_sv = ctk.StringVar()

        self.subtitle_label = ctk.CTkLabel(
            self,
            textvariable=self.display_text_sv,
            font=self.card_font,
            fg_color="transparent",
            anchor="w",
            pady=0,
            padx=0
        )

        self.subtitle_label.grid(row=1, column=0, sticky="w", padx=DEFAULT_PAD)

        self.rowconfigure([0, 1], weight=0)
        self.columnconfigure(0, weight=1)
        self.bind_frame()
        self.update_display_text()

    def update_display_text(self):
        self.update_idletasks()
        print(self.winfo_width(), "width of piece card")
        if len(self.piece_text) > 30:
            self.display_text_sv.set(self.piece_text[0:28] + "...")
        else:
            self.display_text_sv.set(self.piece_text)
