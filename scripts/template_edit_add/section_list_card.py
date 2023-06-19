import customtkinter as ctk
from ..settings import *
from ..components import ListCard, InvisibleEntry
from ..containers import TemplateSection
from typing import Callable
from PIL import Image
import os


class SectionCard(ListCard):
    def __init__(self, master,
                 section: TemplateSection,
                 piece_count: int,
                 select_section_command: Callable,
                 add_command: tuple[str, Callable],
                 delete_command: tuple[str, Callable]):
        super().__init__(master,
                         fg_color="transparent",
                         hover_color=BUTTON_HOVER_COLOR,
                         height=57,
                         click_command=select_section_command)

        self.card_data = section

        entry_text = f"{self.card_data.section_title}"
        if "@" in self.card_data.id:
            entry_text = "*" + entry_text

        self.section_name = InvisibleEntry(
            self,
            placeholder_text=entry_text,
            font=ctk.CTkFont(**NORMAL_LABEL_FONT),
            show_image=False,
            validate="key",
            validatecommand=(self.register(self.validate_command), "%P")
        )

        self.section_name.grid(row=0, column=0, columnspan=2, sticky="new", padx=DEFAULT_PAD)

        if piece_count == 0:
            sub_text = "No pieces"
        elif piece_count == 1:
            sub_text = "1 piece"
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

        self.right_click_menu.add_command(label="Select section",
                                          command=lambda: select_section_command(self.card_data))
        self.right_click_menu.add_command(label=add_command[0], command=lambda: add_command[1](self.card_data))
        self.right_click_menu.add_command(label=delete_command[0], command=lambda: delete_command[1](self.card_data))
        self.right_click_menu.add_command(label="Edit section title", command=self.section_name.text_entry.focus_set)

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

        delete_button.grid(row=1, column=1, sticky="e", padx=(0, DEFAULT_PAD))

    def validate_command(self, p: str):
        if "@" in self.card_data.id:
            self.card_data.section_title = p[1::]
        else:
            self.card_data.section_title = p
        return True

    def update_piece_count(self, new_count: int):
        if new_count == 0:
            sub_text = "No pieces"
        elif new_count == 1:
            sub_text = "1 piece"
        else:
            sub_text = f"{new_count} pieces"

        self.subtitle_label.configure(text=sub_text)

    def bind_frame(self):
        for child in self.winfo_children():
            child.bind("<Enter>", lambda event: self.on_hover())
            child.bind("<Leave>", lambda event: self.on_mouse_leave())
            child.bind("<Button-3>", self.right_clicked)

            if self.command is not None:
                child.bind("<Button-1>", lambda event: self.command(self.card_data))

        self.section_name.text_entry.bind("<Enter>", lambda event: self.on_hover())
        self.section_name.text_entry.bind("<Leave>", lambda event: self.on_mouse_leave())
