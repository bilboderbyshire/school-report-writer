from ..settings import *
from ..components import AutohidingScrollableAndLoadingFrame
from ..containers import IndividualReport
from .pupil_list_card import PupilListCard
from .add_one_top_level import AddOneToplevel


class PupilScrollframe(AutohidingScrollableAndLoadingFrame):
    def __init__(self,
                 master):
        super().__init__(master,
                         fg_color=LABEL_CARD_COLOR)

        self.all_cards: dict[str, PupilListCard] = {}
        self.current_max_row = 0

        self.rowconfigure("all", weight=0)
        self.columnconfigure(0, weight=1)

    def add_pupil(self, report: IndividualReport):
        new_card = PupilListCard(
            self,
            report=report,
            delete_command=self.delete_pupil,
            edit_command=self.edit_pupil
        )
        if self.current_max_row > 0:
            new_card.grid(row=self.current_max_row, column=0, sticky="nsew", padx=SMALL_PAD, pady=(0, SMALL_PAD))
        else:
            new_card.grid(row=self.current_max_row, column=0, sticky="nsew", padx=SMALL_PAD, pady=SMALL_PAD)
        self.all_cards[report.id] = new_card

        self.current_max_row += 1

    def delete_pupil(self, report: IndividualReport):
        pupil_to_delete = self.all_cards.pop(report.id)
        pupil_to_delete.destroy()

    def edit_pupil(self, report: IndividualReport):
        add_one_tl = AddOneToplevel(self, pupil_info=report.get_pupil_info())
        edited_info = add_one_tl.get_pupil_info()

        self.grab_set()
        self.grab_release()

        if edited_info is not None:
            self.all_cards[report.id].refresh_info(edited_info)
