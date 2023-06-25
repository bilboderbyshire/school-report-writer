import customtkinter as ctk
from ..settings import *
import os
from ..title_bar import TitleLabel
from ..app_engine import AppEngine
from .selection_column_scrollframe import SelectionColumnScrollframe
from ..components import Separator, SecondaryButton


class CopyTemplateFromToplevel(ctk.CTkToplevel):
    def __init__(self, master, app_engine: AppEngine):
        super().__init__(master,
                         fg_color=ROOT_BG)

        self.update_idletasks()
        ws = self.winfo_screenwidth()
        hs = self.winfo_screenheight()

        x = int((ws / 2) - (COPY_FROM_TOPLEVEL_WIDTH / 2))
        y = int((hs / 2) - (COPY_FROM_TOPLEVEL_HEIGHT / 2)) - 100

        self.geometry(f"{COPY_FROM_TOPLEVEL_GEOMETRY}+{x}+{y}")

        self.title("Copy from...")

        # CTk.Toplevel source code applies default iconbitmap after 200ms (for some reason), this overrides any icon
        #  change made during initialisation of login window. This code overrides their override by rendering my icon
        #  50ms after theirs.
        self.after(250, lambda: self.iconbitmap(os.path.join(os.getcwd(), "images/app-logo.ico")))

        self.app_engine = app_engine

        title_bar = TitleLabel(self,
                               "Copy from...")
        title_bar.grid(row=0, column=0, sticky="w", pady=(DEFAULT_PAD, 35), padx=DEFAULT_PAD)

        mainframe = ctk.CTkFrame(self, fg_color=LABEL_CARD_COLOR)
        mainframe.grid(row=1, column=0, sticky="nsew", padx=DEFAULT_PAD, pady=(0, SMALL_PAD))
        mainframe.rowconfigure(0, weight=1)
        mainframe.columnconfigure([0, 2, 4], weight=1, uniform="columns")
        mainframe.columnconfigure([1, 3], weight=0)

        self.template_scrollframe = SelectionColumnScrollframe(
            mainframe,
            label_text="Templates"
        )
        self.template_scrollframe.grid(row=0, column=0, sticky="nsew", padx=(SMALL_PAD, 0), pady=(0, SMALL_PAD))

        sep1 = Separator(mainframe, "ver", fg_color=LIGHT_SEPERATOR_COLOR)
        sep1.grid(row=0, column=1, sticky="ns", pady=(40, DEFAULT_PAD))

        self.section_scrollframe = SelectionColumnScrollframe(
            mainframe,
            label_text="Sections"
        )
        self.section_scrollframe.grid(row=0, column=2, sticky="nsew", pady=(0, SMALL_PAD))

        sep2 = Separator(mainframe, "ver", fg_color=LIGHT_SEPERATOR_COLOR)
        sep2.grid(row=0, column=3, sticky="ns", pady=(40, DEFAULT_PAD))

        self.pieces_scrollframe = SelectionColumnScrollframe(
            mainframe,
            label_text="Pieces"
        )
        self.pieces_scrollframe.grid(row=0, column=4, sticky="nsew", padx=(0, SMALL_PAD), pady=(0, SMALL_PAD))

        self.button_frame = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )
        self.button_frame.grid(row=2, column=0, sticky="nsew", padx=DEFAULT_PAD, pady=(0, DEFAULT_PAD))
        self.button_frame.columnconfigure([0, 1, 2, 3, 4], weight=1, uniform="columns")
        self.button_frame.rowconfigure(0, weight=0)

        copy_section_button = ctk.CTkButton(
            self.button_frame,
            text="Copy section",
            font=ctk.CTkFont(**NORMAL_LABEL_FONT),
            state="disabled"
        )
        copy_section_button.grid(row=0, column=2, sticky="ew", padx=(0, SMALL_PAD))

        copy_pieces_button = ctk.CTkButton(
            self.button_frame,
            text="Copy piece",
            font=ctk.CTkFont(**NORMAL_LABEL_FONT),
            state="disabled"
        )
        copy_pieces_button.grid(row=0, column=3, sticky="ew", padx=(0, SMALL_PAD))

        cancel_button = SecondaryButton(
            self.button_frame,
            text="Cancel",
            font=ctk.CTkFont(**NORMAL_LABEL_FONT)
        )
        cancel_button.grid(row=0, column=4, sticky="ew")

        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=0)
        self.columnconfigure(0, weight=1)

        self.after(1, self.check_all_scrollbars)

        self.grab_set()
        self.wait_window()

    def check_all_scrollbars(self):
        self.template_scrollframe.check_scrollbar_needed()
        self.section_scrollframe.check_scrollbar_needed()
        self.pieces_scrollframe.check_scrollbar_needed()
