import customtkinter as ctk
from ..settings import *
from PIL import Image
import os


class InvisibleEntry(ctk.CTkFrame):
    def __init__(self, master,
                 fg_color="transparent",
                 text_color=STANDARD_TEXT_COLOR,
                 placeholder_text="Invisible entry",
                 font: ctk.CTkFont | None = None,
                 image_size: int = 15,
                 show_image: bool = True,
                 **kwargs):
        super().__init__(master,
                         fg_color=fg_color)

        if font is None:
            self.entry_font = ctk.CTkFont(**SECONDARY_TITLE_FONT)
        else:
            self.entry_font = font

        self.text_entry = ctk.CTkEntry(
            self,
            font=self.entry_font,
            fg_color=fg_color,
            text_color=text_color,
            corner_radius=10,
            border_width=0,
            **kwargs)
        self.text_entry.insert(0, placeholder_text)

        self.text_entry.winfo_children()[1].grid_configure(padx=0, pady=0)

        if show_image:
            self.edit_image = ctk.CTkImage(
                    light_image=Image.open(os.path.join(os.getcwd(), "images/light-pencil.png")),
                    dark_image=Image.open(os.path.join(os.getcwd(), "images/dark-pencil.png")),
                    size=(image_size, image_size)
                )

            self.image_label = ctk.CTkLabel(
                self,
                text="",
                fg_color=fg_color,
                image=self.edit_image,
                anchor="center",
            )

            self.image_label.grid(row=0, column=0, sticky="w")
            self.text_entry.grid(row=0, column=1, sticky="new", padx=(DEFAULT_PAD, 0))
            self.columnconfigure(0, weight=0)
            self.columnconfigure(1, weight=1)
        else:
            self.text_entry.grid(row=0, column=0, sticky="nsew")
            self.columnconfigure(0, weight=1)

        self.rowconfigure(0, weight=1)

        self.text_entry.bind("<Return>", lambda e: self.focus())

    def configure(self, require_redraw=False, **kwargs):
        self.text_entry.configure(require_redraw, **kwargs)
