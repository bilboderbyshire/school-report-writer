import customtkinter as ctk
from ..settings import *
import os
from ..title_bar import TitleLabel
from ..app_engine import AppEngine
from .selection_column_scrollframe import SelectionColumnScrollframe
from ..components import Separator, SecondaryButton


class CopyTemplateFromToplevel(ctk.CTkToplevel):
    def __init__(self, master, app_engine: AppEngine,
                 choice_tracker: ctk.StringVar):
        super().__init__(master,
                         fg_color=ROOT_BG)

        self.update_idletasks()
        self.results = {}
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
        self.choice_tracker = choice_tracker

        title_bar = TitleLabel(self,
                               "Copy from...")
        title_bar.grid(row=0, column=0, sticky="w", pady=(DEFAULT_PAD, 35), padx=DEFAULT_PAD)

        mainframe = ctk.CTkFrame(self, fg_color=LABEL_CARD_COLOR)
        mainframe.grid(row=1, column=0, sticky="nsew", padx=DEFAULT_PAD, pady=(0, SMALL_PAD))
        mainframe.rowconfigure(0, weight=1)
        mainframe.columnconfigure([0, 2], weight=2, uniform="columns")
        mainframe.columnconfigure(4, weight=3, uniform="columns")
        mainframe.columnconfigure([1, 3], weight=0)

        self.template_scrollframe = SelectionColumnScrollframe(
            mainframe,
            label_text="Templates",
            card_selected_command=self.template_selected
        )
        self.template_scrollframe.grid(row=0, column=0, sticky="nsew", padx=(SMALL_PAD, 0), pady=(0, SMALL_PAD))

        sep1 = Separator(mainframe, "ver", fg_color=LIGHT_SEPERATOR_COLOR)
        sep1.grid(row=0, column=1, sticky="ns", pady=(40, DEFAULT_PAD))

        self.section_scrollframe = SelectionColumnScrollframe(
            mainframe,
            label_text="Sections",
            card_selected_command=self.section_selected
        )
        self.section_scrollframe.grid(row=0, column=2, sticky="nsew", pady=(0, SMALL_PAD))

        sep2 = Separator(mainframe, "ver", fg_color=LIGHT_SEPERATOR_COLOR)
        sep2.grid(row=0, column=3, sticky="ns", pady=(40, DEFAULT_PAD))

        self.pieces_scrollframe = SelectionColumnScrollframe(
            mainframe,
            label_text="Pieces",
            card_selected_command=self.piece_selected
        )
        self.pieces_scrollframe.grid(row=0, column=4, sticky="nsew", padx=(0, SMALL_PAD), pady=(0, SMALL_PAD))

        self.button_frame = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )
        self.button_frame.grid(row=2, column=0, sticky="nsew", padx=DEFAULT_PAD, pady=(0, DEFAULT_PAD))
        self.button_frame.columnconfigure([0, 1, 2, 3, 4], weight=1, uniform="columns")
        self.button_frame.rowconfigure(0, weight=0)

        self.copy_section_button = ctk.CTkButton(
            self.button_frame,
            text="Copy section",
            font=ctk.CTkFont(**NORMAL_LABEL_FONT),
            state="disabled",
            command=self.copy_sections_clicked
        )
        self.copy_section_button.grid(row=0, column=2, sticky="ew", padx=(0, SMALL_PAD))

        self.copy_pieces_button = ctk.CTkButton(
            self.button_frame,
            text="Copy piece",
            font=ctk.CTkFont(**NORMAL_LABEL_FONT),
            state="disabled",
            command=self.copy_pieces_clicked
        )
        self.copy_pieces_button.grid(row=0, column=3, sticky="ew", padx=(0, SMALL_PAD))

        cancel_button = SecondaryButton(
            self.button_frame,
            text="Cancel",
            font=ctk.CTkFont(**NORMAL_LABEL_FONT),
            command=self.cancel_clicked
        )
        cancel_button.grid(row=0, column=4, sticky="ew")

        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=0)
        self.columnconfigure(0, weight=1)

        all_templates = dict(zip([i.id for i in self.app_engine.copy_of_template_collection.values()],
                                 [i.template_title for i in self.app_engine.copy_of_template_collection.values()]))
        self.template_scrollframe.populate_cards(all_templates)

        self.after(1, self.check_all_scrollbars)

        self.grab_set()
        self.focus_force()
        self.wait_window()

    def check_all_scrollbars(self):
        self.template_scrollframe.check_scrollbar_needed()
        self.section_scrollframe.check_scrollbar_needed()
        self.pieces_scrollframe.check_scrollbar_needed()

    def template_selected(self, template_id: str):
        chosen_sections = dict(zip(
            [i.id for i in self.app_engine.copy_of_section_collection.values() if i.template == template_id],
            [i.section_title for i in self.app_engine.copy_of_section_collection.values() if i.template == template_id]
        ))
        self.template_scrollframe.card_selected(template_id)
        self.section_scrollframe.populate_cards(chosen_sections)
        self.pieces_scrollframe.populate_cards(None)
        self.copy_pieces_button.configure(state="disabled", text="Copy piece")
        self.copy_section_button.configure(state="disabled", text="Copy section")

        self.check_all_scrollbars()

    def section_selected(self, section_id: str):
        self.section_scrollframe.compound_card_selected(section_id)

        if self.section_scrollframe.total_selected > 1:
            self.copy_section_button.configure(state="normal", text="Copy sections")
            self.pieces_scrollframe.populate_cards(None)
            self.copy_pieces_button.configure(state="disabled", text="Copy piece")
        elif self.section_scrollframe.total_selected > 0:
            self.copy_section_button.configure(state="normal", text="Copy section")
            for card in self.section_scrollframe.all_cards.values():
                if card.selected:
                    chosen_pieces = dict(zip(
                        [i.id for i in self.app_engine.copy_of_piece_collection.values() if
                         i.section == card.card_data],
                        [i.piece_text for i in self.app_engine.copy_of_piece_collection.values() if
                         i.section == card.card_data]
                    ))
                    self.pieces_scrollframe.populate_cards(chosen_pieces)
                    self.copy_pieces_button.configure(state="disabled", text="Copy piece")
                    break

        else:
            self.copy_section_button.configure(state="disabled", text="Copy section")
            self.copy_pieces_button.configure(state="disabled", text="Copy piece")
            self.pieces_scrollframe.populate_cards(None)

        self.check_all_scrollbars()

    def piece_selected(self, piece_id: str):
        self.pieces_scrollframe.compound_card_selected(piece_id)

        if self.pieces_scrollframe.total_selected > 1:
            self.copy_pieces_button.configure(state="normal", text="Copy pieces")
        elif self.pieces_scrollframe.total_selected > 0:
            self.copy_pieces_button.configure(state="normal", text="Copy piece")
        else:
            self.copy_pieces_button.configure(state="disabled", text="Copy piece")

        self.check_all_scrollbars()

    def copy_sections_clicked(self):
        selected_ids = []
        for card_id, card in self.section_scrollframe.all_cards.items():
            if card.selected:
                selected_ids.append(card_id)

        self.results["section"] = selected_ids
        self.destroy()

    def copy_pieces_clicked(self):
        selected_ids = []
        for card_id, card in self.pieces_scrollframe.all_cards.items():
            if card.selected:
                selected_ids.append(card_id)

        self.results["piece"] = selected_ids
        self.destroy()

    def cancel_clicked(self):
        self.results["cancel"] = []
        self.destroy()

    def get_results(self) -> dict[str, list[str]]:
        return self.results

