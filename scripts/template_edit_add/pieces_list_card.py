import customtkinter as ctk
from ..settings import *
from ..components import ListCard
from ..containers import IndividualPiece
from typing import Callable
from PIL import Image
import os


class PieceListCard(ListCard):
    def __init__(self, master,
                 piece: IndividualPiece,
                 select_piece_command: Callable,
                 card_add: tuple[str, Callable],
                 card_delete: tuple[str, Callable],
                 card_copy: tuple[str, Callable]
                 ):
        super().__init__(master, height=30, click_command=select_piece_command)

        self.card_data = piece

        self.piece_text = piece.piece_text
        self.card_font = ctk.CTkFont(**SMALL_LABEL_FONT)
        self.display_text_sv = ctk.StringVar()

        self.right_click_menu.add_command(label=card_add[0], command=lambda: card_add[1](self.card_data))
        self.right_click_menu.add_command(label=card_copy[0], command=lambda: card_copy[1](self.card_data))
        self.right_click_menu.add_command(label=card_delete[0], command=lambda: card_delete[1](self.card_data))

        self.subtitle_label = ctk.CTkLabel(
            self,
            textvariable=self.display_text_sv,
            font=self.card_font,
            fg_color="transparent",
            anchor="w",
            pady=0,
            padx=0
        )

        self.subtitle_label.grid(row=0, column=0, sticky="w", padx=(DEFAULT_PAD, 0))

        self.rowconfigure(0, weight=0)
        self.columnconfigure(0, weight=1)
        self.columnconfigure([1, 2], weight=0)
        self.bind_frame()

        copy_image = ctk.CTkImage(
            light_image=Image.open(os.path.join(os.getcwd(), "images/light-copy.png")),
            dark_image=Image.open(os.path.join(os.getcwd(), "images/dark-copy.png")),
            size=(15, 15)
        )
        copy_button = ctk.CTkButton(
            self,
            fg_color="transparent",
            image=copy_image,
            command=lambda: card_copy[1](self.card_data),
            text="",
            width=0,
            height=0,
            hover_color=BUTTON_HOVER_COLOR,
            corner_radius=5
        )

        copy_button.grid(row=0, column=1, sticky="e", padx=(0, SMALL_PAD))

        delete_image = ctk.CTkImage(
            light_image=Image.open(os.path.join(os.getcwd(), "images/bin.png")),
            dark_image=Image.open(os.path.join(os.getcwd(), "images/bin.png")),
            size=(15, 15)
        )
        delete_button = ctk.CTkButton(
            self,
            fg_color="transparent",
            image=delete_image,
            command=lambda: card_delete[1](self.card_data),
            text="",
            width=0,
            height=0,
            hover_color=BUTTON_HOVER_COLOR,
            corner_radius=5
        )

        delete_button.grid(row=0, column=2, sticky="e", padx=(0, SMALL_PAD))
        self.update_display_text()

    def update_display_text(self):
        self.update_idletasks()
        if len(self.piece_text) > 30:
            self.display_text_sv.set(self.piece_text[0:28] + "...")
        else:
            self.display_text_sv.set(self.piece_text)
