import customtkinter as ctk
from ..settings import *
from ..components import AutohidingScrollableAndLoadingFrame
from .report_set_card import ReportSetCard
from ..app_engine import AppEngine
from typing import Callable


class ReportsScrollableFrame(AutohidingScrollableAndLoadingFrame):
    def __init__(self,
                 master,
                 app_engine: AppEngine,
                 report_set_selected_command: Callable,
                 add_command: Callable):
        super().__init__(master,
                         label_font=ctk.CTkFont(**SECONDARY_TITLE_FONT),
                         label_anchor="w",
                         label_fg_color="transparent",
                         label_text="Reports",
                         fg_color=ROOT_BG,
                         button_command=add_command)

        self.app_engine = app_engine
        self.card_selected_command = report_set_selected_command

    def build_report_frame(self):

        for i in self.winfo_children():
            i.destroy()

        self.update_idletasks()

        reports_set = self.app_engine.copy_of_reports_set_collection.values()

        for index, set_report in enumerate(reports_set):
            new_card = ReportSetCard(self, self.app_engine, set_report, click_command=self.card_selected_command)
            if index == len(reports_set) - 1:
                new_card.grid(row=index, column=0, sticky="ew", padx=DEFAULT_PAD - 7)
            else:
                new_card.grid(row=index, column=0, sticky="ew", padx=DEFAULT_PAD - 7, pady=(0, DEFAULT_PAD))

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=0)