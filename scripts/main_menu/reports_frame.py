import customtkinter as ctk
from ..settings import *
from ..containers import SingleReportSet
from ..components import AutohidingScrollableAndLoadingFrame
from .report_set_card import ReportSetCard


class ReportsScrollableFrame(AutohidingScrollableAndLoadingFrame):
    def __init__(self, master):
        super().__init__(master,
                         label_font=ctk.CTkFont(**SECONDARY_TITLE_FONT),
                         label_anchor="w",
                         label_fg_color="transparent",
                         label_text="Reports",
                         fg_color=ROOT_BG)

    def build_report_frame(self, reports_set: list[SingleReportSet]):
        for i in self.winfo_children():
            i.destroy()

        self.update_idletasks()

        for index, i in enumerate(reports_set):
            new_card = ReportSetCard(self, i, command=self.card_command)
            if index == len(reports_set) - 1:
                new_card.grid(row=index, column=0, sticky="ew", padx=DEFAULT_PAD - 7)
            else:
                new_card.grid(row=index, column=0, sticky="ew", padx=DEFAULT_PAD - 7, pady=(0, DEFAULT_PAD))

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=0)

    def card_command(self):
        print("Card clicked")
