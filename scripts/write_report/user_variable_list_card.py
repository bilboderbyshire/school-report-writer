import customtkinter as ctk
from ..settings import *
from ..components import ListCard, Separator, NormalLabel


class UserVariableListCard(ListCard):
    def __init__(self, master,
                 variable_type: str):
        super().__init__(master, fg_color=SECONDARY_LABEL_CARD_COLOR)

        self.grid_propagate(True)

        self.variable_type = variable_type
        self.variable_count_iv = ctk.IntVar(value=0)
        self.instance_dict = {}

        title_frame = ctk.CTkFrame(self, fg_color="transparent")
        title_frame.grid(row=0, column=0, sticky="nsew")
        title_frame.rowconfigure([0, 1], weight=0)
        title_frame.columnconfigure(0, weight=1)
        title_frame.columnconfigure(1, weight=0)

        title_label = NormalLabel(title_frame, text=self.variable_type.capitalize())
        title_label.grid(row=0, column=0, sticky="w", padx=(DEFAULT_PAD, 0), pady=(SMALL_PAD, 0))

        var_count_label = NormalLabel(title_frame, textvariable=self.variable_count_iv)
        var_count_label.grid(row=0, column=1, sticky="e", padx=(0, DEFAULT_PAD), pady=(SMALL_PAD, 0))

        title_sep = Separator(title_frame, "hor", fg_color=STANDARD_TEXT_COLOR)
        title_sep.grid(row=1, column=0, columnspan=2, sticky="ew", padx=DEFAULT_PAD*2, pady=(0, DEFAULT_PAD))

        self.rowconfigure("all", weight=0)
        self.columnconfigure(0, weight=1)

    def add_variable(self, variable_to_add):
        pass

    def delete_variable(self, variable_to_delete):
        pass

    def clear_frame(self):
        for card in self.instance_dict.values():
            card.destroy()

        self.instance_dict = {}
        self.variable_count_iv.set(0)
