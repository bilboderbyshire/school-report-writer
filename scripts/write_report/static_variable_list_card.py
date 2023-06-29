from .user_variable_list_card import UserVariableListCard
import customtkinter as ctk
from ..components import SmallLabel
from ..settings import *
from typing import Callable


class StaticVariableListCard(UserVariableListCard):
    def __init__(self, master,
                 edit_static_command: Callable):
        super().__init__(master, variable_type="static")

        self.instance_dict: dict[str, StaticVariableListCard]
        self.edit_command = edit_static_command
        self.current_max_rows = 1

    def add_variable(self, variable_to_add: str):
        if variable_to_add in self.instance_dict.keys():
            return

        new_var_entry = StaticVariableEdit(
            self,
            variable_name=variable_to_add,
            entry_edited_command=self.validation_test,
        )
        self.current_max_rows += 1
        new_var_entry.grid(row=self.current_max_rows, column=0, sticky="nsew", padx=SMALL_PAD, pady=(0, SMALL_PAD))
        self.instance_dict[variable_to_add] = new_var_entry

        self.variable_count_iv.set(self.variable_count_iv.get() + 1)

    def delete_variable(self, variable_to_delete: str):
        instance_to_delete = self.instance_dict.pop(variable_to_delete)
        instance_to_delete.destroy()
        self.variable_count_iv.set(self.variable_count_iv.get() - 1)

    def validation_test(self, p: str, variable_name: str):
        self.edit_command(variable_name, p)
        return True


class StaticVariableEdit(ctk.CTkFrame):
    def __init__(self, master, variable_name: str, entry_edited_command: Callable):
        super().__init__(master, fg_color="transparent")

        self.variable_name = variable_name

        name_label = SmallLabel(
            self,
            text=f"{self.variable_name.capitalize()}:",
            anchor="w"
        )
        name_label.grid(row=0, column=0, sticky="nsew", pady=(0, SMALL_PAD))

        self.name_entry = ctk.CTkEntry(
            self,
            validate="key",
            validatecommand=(self.register(entry_edited_command), "%P", self.variable_name)
        )
        self.name_entry.grid(row=1, column=0, sticky="nsew")

        self.rowconfigure("all", weight=0)
        self.columnconfigure(0, weight=1)

    def get_entry_text(self):
        return self.name_entry.get()
