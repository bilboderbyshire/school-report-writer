import customtkinter as ctk
from ..settings import *
from ..components import AutohidingScrollableAndLoadingFrame, ListCard
from .section_list_card import SectionCard
import random


class SectionScrollableFrame(AutohidingScrollableAndLoadingFrame):
    def __init__(self, master):
        super().__init__(master, fg_color=ROOT_BG,
                         label_font=ctk.CTkFont(**NORMAL_LABEL_FONT),
                         label_anchor="w",
                         label_fg_color="transparent",
                         label_text="Sections")

        self.given_section_number = 0
        self.added_sections = 0

    def build_section_frame(self, loopvalue):
        self.given_section_number = loopvalue
        for i in self.winfo_children():
            i.destroy()

        self.update_idletasks()

        for i in range(loopvalue + self.added_sections):
            new_section_card = SectionCard(
                self,
                i+1,
                random.randint(1, 7)
            )
            new_section_card.grid(row=i, column=0, sticky="ew", padx=DEFAULT_PAD)

        add_section = self.make_add_section_button()
        add_section.grid(row=loopvalue+self.added_sections+1, column=0, sticky="ew", padx=DEFAULT_PAD,
                         pady=(0, DEFAULT_PAD))

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=0)

    def make_add_section_button(self) -> ListCard:
        add_section_button = ListCard(
            self,
            fg_color="transparent",
            hover_color=BUTTON_HOVER_COLOR,
            height=30,
            command=self.add_section)

        add_button_text = ctk.CTkLabel(
            add_section_button,
            text=f"+ Add new section...",
            font=ctk.CTkFont(**SMALL_LABEL_FONT, slant="italic"),
            fg_color="transparent",
            anchor="w",
            pady=0,
            padx=0
        )

        add_button_text.grid(row=0, column=0, sticky="ew", padx=DEFAULT_PAD)
        add_section_button.rowconfigure(0, weight=1)
        add_section_button.columnconfigure(0, weight=1)
        add_section_button.bind_frame()

        return add_section_button

    def add_section(self):
        self.added_sections += 1
        self.build_section_frame(self.given_section_number)
        self.check_scrollbar_needed()

