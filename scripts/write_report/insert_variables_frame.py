from ..components import AutohidingScrollableAndLoadingFrame
from ..containers import UserVariable
from ..settings import *
from .chain_variable_list_card import ChainVariableListCard
from .choice_variable_list_card import ChoiceVariableListCard
from .static_variable_list_card import StaticVariableListCard
from typing import Callable


class InsertVariablesFrame(AutohidingScrollableAndLoadingFrame):
    def __init__(self,
                 master,
                 variables_collection: dict[str, UserVariable],
                 edit_static_command: Callable,
                 edit_choice_command: Callable,
                 edit_chain_command: Callable):
        super().__init__(master, fg_color=LABEL_CARD_COLOR)

        self.variables_collection = variables_collection

        self.static_vars = StaticVariableListCard(
            self,
            edit_static_command=edit_static_command)
        self.static_vars.grid(row=0, column=0, sticky="nsew", padx=(0, SMALL_PAD), pady=(0, SMALL_PAD))

        self.choice_vars = ChoiceVariableListCard(
            self,
            edit_choice_command=edit_choice_command
        )
        self.choice_vars.grid(row=1, column=0, sticky="nsew", padx=(0, SMALL_PAD), pady=(0, SMALL_PAD))

        self.chain_vars = ChainVariableListCard(
            self,
            edit_chain_command=edit_chain_command
        )
        self.chain_vars.grid(row=2, column=0, sticky="nsew", padx=(0, SMALL_PAD), pady=(0, SMALL_PAD))

        self.rowconfigure("all", weight=0)
        self.columnconfigure(0, weight=1)

    def build_variable_inserts(self,  variable_dict: dict[str, list[str]]):
        for var_type, var_name_list in variable_dict.items():
            if var_type == "static":
                for var_name in var_name_list:
                    self.static_vars.add_variable(var_name)
            elif var_type == "choice":
                for var_name in var_name_list:
                    for i in self.variables_collection.values():
                        if i.variable_name == var_name and i.variable_type == "choice":
                            self.choice_vars.add_variable(i)
                            break
            else:
                for var_name in var_name_list:
                    for i in self.variables_collection.values():
                        if i.variable_name == var_name and i.variable_type == "chain":
                            self.chain_vars.add_variable(i)
                            break

    def clear_all_frames(self):
        self.static_vars.clear_frame()
        self.chain_vars.clear_frame()
        self.choice_vars.clear_frame()