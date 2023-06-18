import customtkinter as ctk
from ..settings import *
from ..components import ListCard
from typing import Callable
from PIL import Image
import os


class SectionCard(ListCard):
    def __init__(self, master,
                 section_number: int,
                 piece_count: int,
                 select_section_command: Callable,
                 add_command: tuple[str, Callable],
                 delete_command: tuple[str, Callable]):
        super().__init__(master,
                         fg_color="transparent",
                         hover_color=BUTTON_HOVER_COLOR,
                         height=57,
                         click_command=select_section_command)

        self.card_data = section_number

        self.right_click_menu.add_command(label="Select section",
                                          command=lambda: select_section_command(self.card_data))
        self.right_click_menu.add_command(label=add_command[0], command=add_command[1])
        self.right_click_menu.add_command(label=delete_command[0], command=lambda: delete_command[1](self.card_data))

        self.text_label = ctk.CTkLabel(
            self,
            text=f"Section {section_number}",
            font=ctk.CTkFont(**NORMAL_LABEL_FONT),
            fg_color="transparent",
            anchor="nw",
            pady=0,
            padx=0
        )

        self.text_label.grid(row=0, column=0, sticky="new", padx=(DEFAULT_PAD, 0))

        if piece_count == 0:
            sub_text = "No pieces"
        elif piece_count == 1:
            sub_text = f"1 piece"
        else:
            sub_text = f"{piece_count} pieces"

        self.subtitle_label = ctk.CTkLabel(
            self,
            text=sub_text,
            font=ctk.CTkFont(**SMALL_LABEL_FONT, slant="italic"),
            fg_color="transparent",
            anchor="nw",
            pady=0,
            padx=0
        )

        self.subtitle_label.grid(row=1, column=0, sticky="ew", padx=DEFAULT_PAD)

        self.rowconfigure([0, 1], weight=0)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=0)
        self.bind_frame()

        delete_image = ctk.CTkImage(
            light_image=Image.open(os.path.join(os.getcwd(), "images/bin.png")),
            dark_image=Image.open(os.path.join(os.getcwd(), "images/bin.png")),
            size=(15, 15)
        )
        delete_button = ctk.CTkButton(
            self,
            fg_color="transparent",
            image=delete_image,
            command=lambda: delete_command[1](self.card_data),
            text="",
            width=0,
            height=0,
            hover_color=BUTTON_HOVER_COLOR,
            corner_radius=5
        )

        delete_button.grid(row=0, column=1, sticky="e", padx=(0, DEFAULT_PAD))
