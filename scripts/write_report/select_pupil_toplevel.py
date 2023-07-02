import customtkinter as ctk
from ..settings import *
from ..title_bar import TitleLabel
from ..containers import IndividualReport
from ..components import AutohidingScrollableAndLoadingFrame, ListCard, NormalLabel
import os
from typing import Callable


class SelectPupilToplevel(ctk.CTkToplevel):
    def __init__(self,
                 master,
                 reports_list: list[IndividualReport]):
        super().__init__(master,
                         fg_color=ROOT_BG)

        self.reports_list = reports_list
        self.selected_pupil: IndividualReport | None = None
        self.update_idletasks()
        ws = self.winfo_screenwidth()
        hs = self.winfo_screenheight()

        x = int((ws / 2) - (LOGIN_WIDTH / 2))
        y = int((hs / 2) - (LOGIN_HEIGHT / 2)) - 100

        self.geometry(f"{LOGIN_GEOMETRY}+{x}+{y}")

        self.title("Select pupil")

        # CTk.Toplevel source code applies default iconbitmap after 200ms (for some reason), this overrides any icon
        #  change made during initialisation of login window. This code overrides their override by rendering my icon
        #  50ms after theirs.
        self.after(250, lambda: self.iconbitmap(os.path.join(os.getcwd(), "images/app-logo.ico")))

        title_bar = TitleLabel(self,
                               "Add one...")
        title_bar.grid(row=0, column=0, sticky="w", pady=(DEFAULT_PAD, 35), padx=DEFAULT_PAD)

        self.pupil_scrollframe = AutohidingScrollableAndLoadingFrame(
            self,
            fg_color=ROOT_BG
        )

        self.pupil_scrollframe.grid(row=1, column=0, sticky="nsew", padx=DEFAULT_PAD, pady=(0, DEFAULT_PAD))
        self.pupil_scrollframe.rowconfigure("all", weight=0)
        self.pupil_scrollframe.columnconfigure(0, weight=1)

        current_index = 0
        for report in self.reports_list:
            new_card = BasicPupilListCard(
                self.pupil_scrollframe,
                report=report,
                select_pupil_command=self.card_selected_command
            )
            new_card.grid(row=current_index, column=0, sticky="nsew", pady=(SMALL_PAD, 0))
            current_index += 1

        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)

        self.after(100, self.pupil_scrollframe.check_scrollbar_needed)

        self.grab_set()
        self.wait_window()

    def card_selected_command(self, report_selected: IndividualReport):
        self.selected_pupil = report_selected
        self.destroy()

    def get_selected_pupil(self) -> IndividualReport | None:
        return self.selected_pupil


class BasicPupilListCard(ListCard):
    def __init__(self, master,
                 report: IndividualReport,
                 select_pupil_command: Callable):
        super().__init__(master,
                         height=40,
                         click_command=select_pupil_command)

        self.card_data = report

        name_label = NormalLabel(
            self,
            text=f"{report.pupil_forename.capitalize()} {report.pupil_surname.capitalize()}"
        )
        name_label.grid(row=0, column=0, **SMALL_PAD_COMPLETE)
