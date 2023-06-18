import customtkinter as ctk
from ..settings import *
from PIL import Image
import os


class InvisibleEntry(ctk.CTkFrame):
    def __init__(self, master,
                 fg_color="transparent",
                 text_color=STANDARD_TEXT_COLOR,
                 placeholder_text="Invisible entry",
                 **kwargs):
        super().__init__(master,
                         fg_color=fg_color)

        self.text_entry = ctk.CTkEntry(
            self,
            font=ctk.CTkFont(**SECONDARY_TITLE_FONT),
            fg_color=fg_color,
            text_color=text_color,
            border_width=0,
            **kwargs)
        self.text_entry.insert(0, placeholder_text)
        self.edit_image = ctk.CTkImage(
                light_image=Image.open(os.path.join(os.getcwd(), "images/light-pencil.png")),
                dark_image=Image.open(os.path.join(os.getcwd(), "images/dark-pencil.png")),
                size=(15, 15)
            )

        self.image_label = ctk.CTkLabel(
            self,
            text="",
            fg_color=fg_color,
            image=self.edit_image,
            anchor="center",
        )

        self.image_label.grid(row=0, column=0, sticky="nsew", padx=(0, DEFAULT_PAD))
        self.text_entry.grid(row=0, column=1, sticky="nsew")

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=1)

        self.text_entry.bind("<Return>", lambda e: self.focus())
