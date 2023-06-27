import customtkinter as ctk
from ..components import ListCard
from ..settings import *
from ..containers import IndividualPiece
from PIL import Image
import os


class ReportPieceListCard(ListCard):
    def __init__(self,
                 master,
                 piece: IndividualPiece):
        super().__init__(master, fg_color=SECONDARY_LABEL_CARD_COLOR)

        self.card_data = piece

        self.grid_propagate(True)

        self.piece_text_label = ctk.CTkLabel(
            self,
            text=self.card_data.piece_text,
            font=ctk.CTkFont(**SMALL_LABEL_FONT),
            fg_color="transparent",
            justify="left",
            anchor="w",
            pady=0,
            padx=0
        )
        self.piece_text_label.grid(row=0, column=0, sticky="nsew", padx=(DEFAULT_PAD, SMALL_PAD), pady=DEFAULT_PAD)

        self.bind_frame()

        add_piece_image = ctk.CTkImage(
            light_image=Image.open(os.path.join(os.getcwd(), "images/light-chevron.png")),
            dark_image=Image.open(os.path.join(os.getcwd(), "images/dark-chevron.png")),
            size=(15, 15)
        )
        add_piece_button = ctk.CTkButton(
            self,
            fg_color="transparent",
            image=add_piece_image,
            command=lambda: print("Added"),
            text="",
            width=30,
            height=30,
            hover_color=BUTTON_HOVER_COLOR,
            corner_radius=5
        )

        add_piece_button.grid(row=0, column=1, sticky="e", padx=(0, DEFAULT_PAD), pady=DEFAULT_PAD)

        self.bind("<Configure>", lambda event: self.configure_label_width())

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=0)

    def configure_label_width(self):
        self.update_idletasks()
        self.piece_text_label.configure(wraplength=self.piece_text_label._current_width)
