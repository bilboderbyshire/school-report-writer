import customtkinter as ctk
from ..components import AutohidingScrollableAndLoadingFrame
from ..containers import UserVariable, NewUserVariableRecord
from ..settings import *
from .user_variable_list_card import UserVariableListCard
from .static_variable_list_card import StaticVariableListCard


class InsertVariablesFrame(AutohidingScrollableAndLoadingFrame):
    def __init__(self,
                 master,
                 variables_collection: dict[str, UserVariable]):
        super().__init__(master, fg_color=LABEL_CARD_COLOR)

        self.all_cards: dict = {}
        self.variables_collection = variables_collection

        self.static_vars = StaticVariableListCard(self)
        self.static_vars.grid(row=0, column=0, sticky="nsew", padx=(0, SMALL_PAD), pady=(0, SMALL_PAD))

        new_static_var = UserVariable(NewUserVariableRecord("@0", "project title", "bob", variable_type="static"))
        self.static_vars.add_variable(new_static_var)

        for index, var_type in enumerate(["choice", "chain"]):
            new_card = UserVariableListCard(self, var_type)
            new_card.grid(row=index+1, column=0, sticky="nsew", padx=(0, SMALL_PAD), pady=(0, SMALL_PAD))
            self.all_cards[var_type] = new_card


        self.rowconfigure("all", weight=0)
        self.columnconfigure(0, weight=1)


