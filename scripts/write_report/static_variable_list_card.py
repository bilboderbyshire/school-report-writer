from .user_variable_list_card import UserVariableListCard
import customtkinter as ctk
from ..containers import UserVariable
from ..components import SmallLabel
from ..settings import *
from typing import Callable


class StaticVariableListCard(UserVariableListCard):
    def __init__(self, master):
        super().__init__(master, variable_type="static")

        self.instance_dict: dict[int, ctk.CTkEntry]

    def add_variable(self, variable_to_add: UserVariable):
        new_var_entry = StaticVariableEdit(
            self,
            variable_name=variable_to_add.variable_name,
            entry_edited_command=self.validation_test
        )

        next_index = max(list(self.instance_dict.keys()), default=0) + 1
        new_var_entry.grid(row=next_index, column=0, sticky="nsew", padx=SMALL_PAD, pady=(0, SMALL_PAD))
        self.instance_dict[next_index] = new_var_entry

        self.variable_count_iv.set(self.variable_count_iv.get() + 1)

    def validation_test(self, p):
        print(f"{p} typed")
        return True


class StaticVariableEdit(ctk.CTkFrame):
    def __init__(self, master, variable_name: str, entry_edited_command: Callable):
        super().__init__(master, fg_color="transparent")

        name_label = SmallLabel(
            self,
            text=f"{variable_name.capitalize()}:",
            anchor="w"
        )
        name_label.grid(row=0, column=0, sticky="nsew", pady=(0, SMALL_PAD))

        name_entry = ctk.CTkEntry(
            self,
            validate="key",
            validatecommand=(self.register(entry_edited_command), "%P")
        )
        name_entry.grid(row=1, column=0, sticky="nsew")

        self.rowconfigure("all", weight=0)
        self.columnconfigure(0, weight=1)
