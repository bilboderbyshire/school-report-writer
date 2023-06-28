from .user_variable_list_card import UserVariableListCard
import customtkinter as ctk
from ..containers import UserVariable
from ..components import SmallLabel
from ..settings import *
from typing import Callable


class StaticVariableListCard(UserVariableListCard):
    def __init__(self, master,
                 edit_static_command: Callable):
        super().__init__(master, variable_type="static")

        self.instance_dict: dict[int, ctk.CTkEntry]
        self.edit_command = edit_static_command

    def add_variable(self, variable_to_add: str):
        next_index = max(list(self.instance_dict.keys()), default=-1) + 1

        new_var_entry = StaticVariableEdit(
            self,
            variable_name=variable_to_add,
            entry_edited_command=self.validation_test,
            index=next_index
        )

        new_var_entry.grid(row=next_index+1, column=0, sticky="nsew", padx=SMALL_PAD, pady=(0, SMALL_PAD))
        self.instance_dict[next_index] = new_var_entry

        self.variable_count_iv.set(self.variable_count_iv.get() + 1)

    def validation_test(self, p: str, index: int, variable_name: str):
        self.edit_command(variable_name, int(index), p)
        return True


class StaticVariableEdit(ctk.CTkFrame):
    def __init__(self, master, variable_name: str, entry_edited_command: Callable, index: int):
        super().__init__(master, fg_color="transparent")

        self.instance_index = index
        self.variable_name = variable_name

        name_label = SmallLabel(
            self,
            text=f"{self.variable_name.capitalize()}:",
            anchor="w"
        )
        name_label.grid(row=0, column=0, sticky="nsew", pady=(0, SMALL_PAD))

        name_entry = ctk.CTkEntry(
            self,
            validate="key",
            validatecommand=(self.register(entry_edited_command), "%P", self.instance_index, self.variable_name)
        )
        name_entry.grid(row=1, column=0, sticky="nsew")

        self.rowconfigure("all", weight=0)
        self.columnconfigure(0, weight=1)
