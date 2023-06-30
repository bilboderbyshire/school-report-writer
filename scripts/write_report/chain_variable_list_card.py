from .user_variable_list_card import UserVariableListCard
import customtkinter as ctk
from ..components import SmallLabel, SecondaryOptionmenu, ListCard
from ..containers import UserVariable
from ..settings import *
from typing import Callable


class ChainVariableListCard(UserVariableListCard):
    def __init__(self, master,
                 edit_chain_command: Callable):
        super().__init__(master, variable_type="chain")

        self.instance_dict: dict[int, ChainVariableEdit]
        self.edit_command = edit_chain_command

    def add_variable(self, variable_to_add: UserVariable):
        new_index = max(self.instance_dict.keys(), default=-1) + 1

        new_var_entry = ChainVariableEdit(
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
            total_list.append(edit_frame.card_data)

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


class ChainVariableEdit(ctk.CTkFrame):
    def __init__(self, master,
                 variable_used: UserVariable,
                 index: int,
                 variable_edited_command: Callable):
        super().__init__(master, fg_color="transparent")

        self.variable = variable_used
        self.index = index
        self.all_option_cards: dict[str, OptionListCard] = {}
        self.edit_command = variable_edited_command
        self.card_data = "none"

        name_label = SmallLabel(
            self,
            text=f"{self.variable.variable_name.capitalize()}:",
            anchor="w"
        )
        name_label.grid(row=0, column=0, sticky="nsew", pady=(0, SMALL_PAD))

        radio_frame = ctk.CTkFrame(self, fg_color="transparent")
        radio_frame.grid(row=1, column=0, sticky="nsew", pady=(0, SMALL_PAD))
        radio_frame.rowconfigure(0, weight=1)
        radio_frame.columnconfigure([0, 1], weight=1, uniform="columns")

        self.radio_var = ctk.StringVar(value="and")

        self.radio_and = ctk.CTkRadioButton(
            radio_frame,
            font=ctk.CTkFont(**SMALL_LABEL_FONT),
            text="And",
            variable=self.radio_var,
            value="and",
            command=self.generate_final_sentence
        )
        self.radio_and.grid(row=0, column=0, sticky="nsew", padx=(0, SMALL_PAD))

        self.radio_or = ctk.CTkRadioButton(
            radio_frame,
            font=ctk.CTkFont(**SMALL_LABEL_FONT),
            text="Or",
            variable=self.radio_var,
            value="or",
            command=self.generate_final_sentence
        )
        self.radio_or.grid(row=0, column=1, sticky="nsew")

        current_row = 2
        for option in self.variable.variable_items.split("/"):
            new_list_card = OptionListCard(
                self,
                option_text=option,
                click_command=self.card_clicked
            )
            new_list_card.grid(row=current_row, column=0, sticky="nsew")
            self.all_option_cards[option] = new_list_card
            current_row += 1

        self.rowconfigure("all", weight=0)
        self.columnconfigure(0, weight=1)

    def card_clicked(self, selected_option: str):
        if self.all_option_cards[selected_option].selected:
            self.all_option_cards[selected_option].card_deselected()
        else:
            self.all_option_cards[selected_option].card_selected()

        self.generate_final_sentence()

    def generate_final_sentence(self):
        selected_options = [i.card_data for i in self.all_option_cards.values() if i.selected]
        if selected_options:
            if len(selected_options) > 1:
                final_sentence = ", ".join(selected_options[0:-1])
                final_sentence += f" {self.radio_var.get()} {selected_options[-1]}"
            else:
                final_sentence = selected_options[0]

            self.edit_command(final_sentence, self.variable, self.index)
            self.card_data = final_sentence


class OptionListCard(ListCard):
    def __init__(self, master,
                 option_text: str,
                 click_command: Callable):
        super().__init__(master, click_command=click_command)

        self.card_data = option_text
        self.grid_propagate(True)

        option_label = SmallLabel(
            self,
            text=self.card_data.capitalize(),
            anchor="w"
        )
        option_label.grid(row=0, column=0, sticky="nsew", padx=SMALL_PAD)

        self.rowconfigure(0, weight=0)
        self.columnconfigure(0, weight=1)

        self.bind_frame()
