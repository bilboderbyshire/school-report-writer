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

        self.entry_text = f"{self.card_data.section_title}"

        self.section_name = InvisibleEntry(
            self,
            placeholder_text=self.entry_text,
            font=ctk.CTkFont(**NORMAL_LABEL_FONT),
            show_image=False
        )

        if "@" in self.card_data.id:
            self.unsaved_label = ctk.CTkLabel(
                self,
                fg_color="transparent",
                text="*",
                font=ctk.CTkFont(**NORMAL_LABEL_FONT),
            )
            self.unsaved_label.grid(row=0, column=0, sticky="w", padx=(DEFAULT_PAD, 0))
            self.section_name.grid(row=0, column=1, columnspan=2, sticky="new", padx=(0, DEFAULT_PAD))
        else:
            self.section_name.grid(row=0, column=0, columnspan=3, sticky="new", padx=DEFAULT_PAD)

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

        self.subtitle_label.grid(row=1, column=0, columnspan=2, sticky="ew", padx=DEFAULT_PAD)

        self.right_click_menu.add_command(label="Select section",
                                          command=lambda: select_section_command(self.card_data))
        self.right_click_menu.add_command(label="Edit section title", command=self.entry_enabled)
        self.right_click_menu.add_command(label=add_command[0], command=lambda: add_command[1](self.card_data))
        self.right_click_menu.add_command(label=delete_command[0], command=lambda: delete_command[1](self.card_data))

        self.rowconfigure([0, 1], weight=0)
        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=0)
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

        delete_button.grid(row=1, column=2, sticky="e", padx=(0, DEFAULT_PAD))

        self.section_name.text_entry.bind("<Button-1>", lambda event: self.entry_clicked())
        self.section_name.text_entry.bind("<Enter>", lambda event: self.on_hover())
        self.section_name.text_entry.bind("<Leave>", lambda event: self.on_mouse_leave())
        self.section_name.text_entry.bind("<Double-Button-1>", lambda event: self.entry_enabled())
        self.section_name.text_entry.bind("<FocusOut>", lambda event: self.entry_disabled())

        self.entry_disabled()

    def update_piece_count(self, new_count: int):
        if new_count == 0:
            sub_text = "No pieces"
        elif new_count == 1:
            sub_text = "1 piece"
        else:
            sub_text = f"{new_count} pieces"

        self.subtitle_label.configure(text=sub_text)

    def entry_enabled(self):
        self.section_name.text_entry.configure(state="normal")
        self.section_name.text_entry.select_range(0, "end")
        self.section_name.text_entry.focus_set()

    def entry_disabled(self):
        current_title = self.section_name.text_entry.get().strip()

        if current_title == "":
            self.section_name.text_entry.insert(0, self.entry_text)
            self.section_name.text_entry.delete(len(self.entry_text), "end")

        self.section_name.text_entry.configure(state="readonly")

    def entry_clicked(self):
        if self.section_name.text_entry.cget("state") == "readonly":
            self.card_clicked()
