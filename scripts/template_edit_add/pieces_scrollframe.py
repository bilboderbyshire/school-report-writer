import customtkinter as ctk
from ..settings import *
from ..components import AutohidingScrollableAndLoadingFrame, ListCard
from .pieces_list_card import PieceListCard
from .template_engine import TemplateEngine


class PiecesScrollableFrame(AutohidingScrollableAndLoadingFrame):
    def __init__(self, master, engine: TemplateEngine):
        super().__init__(master,
                         label_font=ctk.CTkFont(**NORMAL_LABEL_FONT),
                         label_anchor="w",
                         label_fg_color="transparent",
                         label_text="Pieces",
                         border_width=2)

        self.configure(border_color=self.cget("fg_color"))

        self.engine = engine

    def build_pieces_frame(self):
        for i in self.winfo_children():
            i.destroy()

        self.update_idletasks()

        for index, value in enumerate(self.engine.get_sections_pieces()):
            new_section_card = PieceListCard(self,
                                             value)
            new_section_card.grid(row=index, column=0, sticky="ew", padx=DEFAULT_PAD)

        add_section = self.make_add_piece_button()
        add_section.grid(row=len(self.engine.get_sections_pieces()) + 1, column=0, sticky="ew", padx=DEFAULT_PAD,
                         pady=(0, DEFAULT_PAD))

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=0)

    def make_add_piece_button(self) -> ListCard:
        add_piece_button = ListCard(
            self,
            fg_color="transparent",
            height=30,
            command=self.add_piece)

        add_button_text = ctk.CTkLabel(
            add_piece_button,
            text=f"+ Add new piece...",
            font=ctk.CTkFont(**SMALL_LABEL_FONT, slant="italic"),
            fg_color="transparent",
            anchor="w",
            pady=0,
            padx=0
        )

        add_button_text.grid(row=0, column=0, sticky="ew", padx=DEFAULT_PAD)
        add_piece_button.rowconfigure(0, weight=1)
        add_piece_button.columnconfigure(0, weight=1)
        add_piece_button.bind_frame()

        return add_piece_button

    def add_piece(self, _):
        self.engine.add_piece()
        self.build_pieces_frame()
        self.check_scrollbar_needed()
