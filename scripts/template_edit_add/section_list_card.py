import customtkinter as ctk
from ..settings import *
from ..components import ListCard


class SectionCard(ListCard):
    def __init__(self, master, section_number: int, piece_count: int, select_section_command):
        super().__init__(master,
                         fg_color="transparent",
                         hover_color=BUTTON_HOVER_COLOR,
                         height=57,
                         click_command=select_section_command)

        self.card_data = section_number

        self.text_label = ctk.CTkLabel(
            self,
            text=f"Section {section_number}",
            font=ctk.CTkFont(**NORMAL_LABEL_FONT),
            fg_color="transparent",
            anchor="nw",
            pady=0,
            padx=0
        )

        self.text_label.grid(row=0, column=0, sticky="new", padx=DEFAULT_PAD)

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
        self.bind_frame()
