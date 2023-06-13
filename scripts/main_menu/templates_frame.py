import customtkinter as ctk
from ..settings import *
from ..containers import ReportTemplate
from ..components import AutohidingScrollableAndLoadingFrame
from .template_card import TemplateCard


class TemplatesScrollableFrame(AutohidingScrollableAndLoadingFrame):
    def __init__(self, master, add_command=None):
        super().__init__(master,
                         label_font=ctk.CTkFont(**SECONDARY_TITLE_FONT),
                         label_anchor="w",
                         label_fg_color="transparent",
                         label_text="Templates",
                         fg_color=ROOT_BG,
                         button_command=add_command)

    def build_template_frame(self, reports_set: list[ReportTemplate]):

        for i in self.winfo_children():
            i.destroy()

        self.update_idletasks()

        for index, i in enumerate(reports_set):
            new_card = TemplateCard(self, i, command=self.card_command)
            if index == len(reports_set) - 1:
                new_card.grid(row=index, column=0, sticky="ew", padx=DEFAULT_PAD - 7)
            else:
                new_card.grid(row=index, column=0, sticky="ew", padx=DEFAULT_PAD - 7, pady=(0, DEFAULT_PAD))

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=0)

    def card_command(self):
        print("Card clicked")
