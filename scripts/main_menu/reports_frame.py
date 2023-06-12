import customtkinter as ctk
from ..settings import *
from ..database import RUNNING_DB
from ..containers import SingleReportSet
from ..components import AutohidingScrollableAndLoadingFrame, ListCard


class ReportsScrollableFrame(AutohidingScrollableAndLoadingFrame):
    def __init__(self, master, reports_set: list[SingleReportSet]):
        super().__init__(master,
                         label_font=ctk.CTkFont(**NORMAL_LABEL_FONT),
                         label_anchor="w",
                         label_fg_color="transparent",
                         label_text="Reports")

    def build_frame(self):
        self.loading_label.destroy()
        self.update_idletasks()

        for i in range(6):
            new_card = ListCard(self, None, command=self.card_command)
            new_card.grid(row=i, column=0, sticky="ew", padx=DEFAULT_PAD-7)

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=0)

    def card_command(self):
        print("Card clicked")



