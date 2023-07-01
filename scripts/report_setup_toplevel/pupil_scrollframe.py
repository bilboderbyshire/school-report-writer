from ..settings import *
from ..components import AutohidingScrollableAndLoadingFrame
from ..containers import PupilInfo
from .pupil_list_card import PupilListCard
from .add_one_top_level import AddOneToplevel


class PupilScrollframe(AutohidingScrollableAndLoadingFrame):
    def __init__(self,
                 master):
        super().__init__(master,
                         fg_color=LABEL_CARD_COLOR)

        self.all_cards: dict[int, PupilListCard] = {}
        self.current_max_row = 0

        self.rowconfigure("all", weight=0)
        self.columnconfigure(0, weight=1)

    def add_pupil(self, pupil_info: PupilInfo):
        new_card = PupilListCard(
            self,
            pupil_info,
            self.delete_pupil,
            index=self.current_max_row,
            edit_command=self.edit_pupil
        )
        if self.current_max_row > 0:
            new_card.grid(row=self.current_max_row, column=0, sticky="nsew", padx=SMALL_PAD, pady=(0, SMALL_PAD))
        else:
            new_card.grid(row=self.current_max_row, column=0, sticky="nsew", padx=SMALL_PAD, pady=SMALL_PAD)
        self.all_cards[self.current_max_row] = new_card

        self.current_max_row += 1

    def delete_pupil(self, index: int):
        pupil_to_delete = self.all_cards.pop(index)
        pupil_to_delete.destroy()

    def edit_pupil(self, index: int):
        pupil_to_edit = self.all_cards.pop(index)

        add_one_tl = AddOneToplevel(self, pupil_info=pupil_to_edit.pupil_info)
        edited_info = add_one_tl.get_pupil_info()

        self.grab_set()
        self.grab_release()

        if edited_info is not None:
            pupil_to_edit.destroy()

            new_card = PupilListCard(
                self,
                edited_info,
                self.delete_pupil,
                index=index,
                edit_command=self.edit_pupil
            )
            new_card.grid(row=index, column=0, sticky="nsew", padx=SMALL_PAD, pady=(0, SMALL_PAD))

            self.all_cards[index] = new_card
