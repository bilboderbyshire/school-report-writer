from .user_variable_list_card import UserVariableListCard
import customtkinter as ctk
from ..components import SmallLabel, SecondaryOptionmenu
from ..containers import UserVariable
from ..settings import *
from typing import Callable


class ChoiceVariableListCard(UserVariableListCard):
    def __init__(self, master,
                 edit_choice_command: Callable):
        super().__init__(master, variable_type="choice")

        self.instance_dict: dict[int, ChoiceVariableEdit]
        self.edit_command = edit_choice_command

    def add_variable(self, variable_to_add: UserVariable):
        new_index = max(self.instance_dict.keys(), default=-1) + 1

        new_var_entry = ChoiceVariableEdit(
            self,
            variable_used=variable_to_add,
            index=new_index,
            variable_edited_command=self.edit_command
        )
        new_var_entry.grid(row=new_index+1, column=0, sticky="nsew", padx=SMALL_PAD, pady=(0, SMALL_PAD))
        self.instance_dict[new_index] = new_var_entry

        self.variable_count_iv.set(self.variable_count_iv.get() + 1)

    def delete_variable(self, variable_to_delete: int):
        deleted_variable = self.instance_dict.pop(variable_to_delete)
        deleted_variable.destroy()
        self.variable_count_iv.set(self.variable_count_iv.get() - 1)

    def get_all_choices(self) -> list[str]:
        total_list = []
        for edit_frame in self.instance_dict.values():
            total_list.append(edit_frame.get_choice_menu())

        return total_list

    def reorganize_instance_dict(self):
        current_sorted_keys = sorted(list(self.instance_dict.keys()))
        temp_instance_dict = {}
        for index, key in enumerate(current_sorted_keys):
            current_frame = self.instance_dict[key]
            current_frame.index = index
            current_frame.grid(row=index + 1, column=0, sticky="nsew", padx=SMALL_PAD, pady=(0, SMALL_PAD))
            temp_instance_dict[index] = current_frame

        self.instance_dict = temp_instance_dict


class ChoiceVariableEdit(ctk.CTkFrame):
    def __init__(self, master, variable_used: UserVariable, index: int, variable_edited_command: Callable):
        super().__init__(master, fg_color="transparent")

        self.variable = variable_used
        self.index = index
        self.default_option_value = "Choose variable"

        name_label = SmallLabel(
            self,
            text=f"{self.variable.variable_name.capitalize()}:",
            anchor="w"
        )
        name_label.grid(row=0, column=0, sticky="nsew", pady=(0, SMALL_PAD))

        self.choice_option_menu = SecondaryOptionmenu(
            self,
            values=[i.capitalize() for i in variable_used.variable_items.split("/")],
            command=lambda value: variable_edited_command(value, self.variable, self.index)
        )
        self.choice_option_menu.grid(row=1, column=0, sticky="nsew")
        self.choice_option_menu.set(self.default_option_value)

        self.rowconfigure("all", weight=0)
        self.columnconfigure(0, weight=1)

    def get_choice_menu(self):
        return self.choice_option_menu.get()

    def __str__(self):
        return str(self.index)