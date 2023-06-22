import customtkinter as ctk
from ..settings import *
from ..components import ListCard, InvisibleEntry
from typing import Callable
from PIL import Image
import os


class OptionListCard(ListCard):
    def __init__(self, master):
        super().__init__(master)

        self.grid_propagate(True)

        self.option_text = ctk.StringVar(value="New option")

        self.entry_frame = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        self.entry_frame.grid(row=0, column=0, sticky="nsew", **SMALL_PAD_COMPLETE)
        self.entry_frame.rowconfigure(0, weight=1)
        self.entry_frame.columnconfigure(0, weight=1)

        self.option_entry = ctk.CTkEntry(
            self.entry_frame,
            textvariable=self.option_text,
            font=ctk.CTkFont(**VERY_SMALL_FONT),
        )
        self.option_entry.grid(row=0, column=0, sticky="nsew")

        self.label_frame = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        self.label_frame.grid(row=0, column=0, sticky="nsew", **SMALL_PAD_COMPLETE)
        self.label_frame.rowconfigure(0, weight=1)
        self.label_frame.columnconfigure(0, weight=1)

        self.option_label = ctk.CTkLabel(
            self.label_frame,
            font=ctk.CTkFont(**VERY_SMALL_FONT),
            fg_color="transparent",
            textvariable=self.option_text,
            justify="left",
            anchor="w"
        )
        self.option_label.grid(row=0, column=0, sticky="nsew")

        self.label_frame.tkraise(self.entry_frame)

        self.option_label.bind("<Double-Button-1>", lambda event: self.edit_text())
        self.label_frame.bind("<Double-Button-1>", lambda event: self.edit_text())
        self.option_label.bind("<Enter>", lambda event: self.on_hover())
        self.label_frame.bind("<Enter>", lambda event: self.on_hover())
        self.option_label.bind("<Leave>", lambda event: self.on_mouse_leave())
        self.label_frame.bind("<Leave>", lambda event: self.on_mouse_leave())
        self.option_label.bind("<Configure>", lambda event: self.resize_label())

        self.option_entry.bind("<Return>", lambda event: self.focus_set())
        self.option_entry.bind("<FocusOut>", lambda event: self.defocus_text())

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.resize_label()
        self.bind_frame()

    def resize_label(self):
        self.label_frame.update()
        self.option_label.configure(wraplength=self.label_frame.winfo_width())

    def edit_text(self):
        print("text editable")
        self.entry_frame.tkraise(self.label_frame)
        self.option_entry.focus_set()

    def defocus_text(self):
        self.label_frame.tkraise(self.entry_frame)
        self.resize_label()
