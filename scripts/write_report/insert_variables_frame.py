import customtkinter as ctk
from ..components import AutohidingScrollableAndLoadingFrame
from ..containers import UserVariable, NewUserVariableRecord
from ..settings import *
from .user_variable_list_card import UserVariableListCard
from .static_variable_list_card import StaticVariableListCard
from typing import Callable


class InsertVariablesFrame(AutohidingScrollableAndLoadingFrame):
    def __init__(self,
                 master,
                 variables_collection: dict[str, UserVariable],
                 edit_static_command: Callable):
        super().__init__(master, fg_color=LABEL_CARD_COLOR)

        self.all_cards: dict = {}
        self.variables_collection = variables_collection

        self.static_vars = StaticVariableListCard(self,
                                                  edit_static_command=edit_static_command)
        self.static_vars.grid(row=0, column=0, sticky="nsew", padx=(0, SMALL_PAD), pady=(0, SMALL_PAD))

        for index, var_type in enumerate(["choice", "chain"]):
            new_card = UserVariableListCard(self, var_type)
            new_card.grid(row=index+1, column=0, sticky="nsew", padx=(0, SMALL_PAD), pady=(0, SMALL_PAD))
            self.all_cards[var_type] = new_card

        self.rowconfigure("all", weight=0)
        self.columnconfigure(0, weight=1)

    def build_variable_inserts(self,  variable_dict: dict[str, list[str]]):
        for var_type, var_name_list in variable_dict.items():
            if var_type == "static":
                for var_name in var_name_list:
                    self.static_vars.add_variable(var_name)
