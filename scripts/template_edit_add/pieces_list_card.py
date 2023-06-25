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
                 card_duplicate: tuple[str, Callable]
                 ):
        super().__init__(master, height=30, click_command=select_piece_command)

        self.card_data = piece
        self.grid_propagate(True)

        self.display_text_sv = ctk.StringVar(value=self.card_data.piece_text)

        self.right_click_menu.add_command(label=card_add[0], command=lambda: card_add[1](self.card_data))
        self.right_click_menu.add_command(label=card_duplicate[0], command=lambda: card_duplicate[1](self.card_data))
        self.right_click_menu.add_command(label=card_delete[0], command=lambda: card_delete[1](self.card_data))

        self.subtitle_label = ctk.CTkLabel(
            self,
            textvariable=self.display_text_sv,
            font=ctk.CTkFont(**SMALL_LABEL_FONT),
            fg_color="transparent",
            justify="left",
            anchor="w",
            pady=0,
            padx=0
        )

        self.subtitle_label.grid(row=0, column=0, sticky="nsew", padx=(DEFAULT_PAD, SMALL_PAD), pady=DEFAULT_PAD)
        self.bind_frame()

        delete_image = ctk.CTkImage(
            light_image=Image.open(os.path.join(os.getcwd(), "images/light-close.png")),
            dark_image=Image.open(os.path.join(os.getcwd(), "images/dark-close.png")),
            size=(15, 15)
        )
        delete_button = ctk.CTkButton(
            self,
            fg_color="transparent",
            image=delete_image,
            command=lambda: card_delete[1](self.card_data),
            text="",
            width=30,
            height=30,
            hover_color=BUTTON_HOVER_COLOR,
            corner_radius=5
        )

        delete_button.grid(row=0, column=1, sticky="ne", padx=(0, DEFAULT_PAD), pady=(DEFAULT_PAD, 0))

        self.bind("<Configure>", lambda event: self.configure_label_width())

        self.rowconfigure(0, weight=0)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=0)

    def update_display_text(self):
        self.display_text_sv.set(self.card_data.piece_text)
        self.update()
        self.subtitle_label.update()

    def configure_label_width(self):
        self.update_idletasks()
        self.subtitle_label.configure(wraplength=self.subtitle_label._current_width)
        print("Card width: ", self.winfo_width())

