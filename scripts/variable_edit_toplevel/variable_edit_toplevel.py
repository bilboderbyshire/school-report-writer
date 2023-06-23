import customtkinter as ctk
from ..settings import *
from ..containers import UserVariable
from ..title_bar import TitleLabel
from ..components import SingleLineEntry, NormalLabel
from .new_variable_options_scrollframe import VariableOptionsScrollframe
import os


class VariableEditToplevel(ctk.CTkToplevel):
    def __init__(self, master,
                 variable_to_edit: UserVariable,
                 variable_collection: dict[str, UserVariable]):
        super().__init__(master,
                         fg_color=ROOT_BG)

        self.new_variable = variable_to_edit
        self.variable_collection = variable_collection
        self.original_title = self.new_variable.variable_name

        self.update_idletasks()
        ws = self.winfo_screenwidth()
        hs = self.winfo_screenheight()

        x = int((ws / 2) - (VARIABLE_TOPLEVEL_WIDTH / 2))
        y = int((hs / 2) - (VARIABLE_TOPLEVEL_HEIGHT / 2)) - 100

        self.geometry(f"{VARIABLE_TOPLEVEL_GEOMETRY}+{x}+{y}")

        self.title("Variable edit")

        # CTk.Toplevel source code applies default iconbitmap after 200ms (for some reason), this overrides any icon
        #  change made during initialisation of login window. This code overrides their override by rendering my icon
        #  50ms after theirs.
        self.after(250, lambda: self.iconbitmap(os.path.join(os.getcwd(), "images/app-logo.ico")))

        title_bar = TitleLabel(self,
                               "Edit Variable")
        title_bar.grid(row=0, column=0, sticky="w", pady=(DEFAULT_PAD, 35), padx=DEFAULT_PAD)

        name_entry_label = NormalLabel(
            self,
            anchor="sw",
            text="Variable name:"
        )
        name_entry_label.grid(row=1, column=0, sticky="ew", pady=(0, DEFAULT_PAD), padx=DEFAULT_PAD)

        self.name_entry = SingleLineEntry(self)
        self.name_entry.grid(row=2, column=0, sticky="ew", pady=(0, DEFAULT_PAD), padx=DEFAULT_PAD)
        self.name_entry.insert(0, self.original_title)

        self.radio_frame = ctk.CTkFrame(self)
        self.radio_frame.grid(row=3, column=0, sticky="nsew", pady=(0, DEFAULT_PAD), padx=DEFAULT_PAD)

        self.radio_var = ctk.StringVar(value="static")
        self.radio_static = ctk.CTkRadioButton(
            self.radio_frame,
            font=ctk.CTkFont(**SMALL_LABEL_FONT),
            text="Static",
            variable=self.radio_var,
            value="static"
        )
        self.radio_static.grid(row=0, column=0, sticky="nsew", **DEFAULT_PAD_COMPLETE)

        self.radio_choice = ctk.CTkRadioButton(
            self.radio_frame,
            font=ctk.CTkFont(**SMALL_LABEL_FONT),
            text="Choice",
            variable=self.radio_var,
            value="choice"
        )
        self.radio_choice.grid(row=0, column=1, sticky="nsew", padx=(0, DEFAULT_PAD), pady=DEFAULT_PAD)

        self.radio_chain = ctk.CTkRadioButton(
            self.radio_frame,
            font=ctk.CTkFont(**SMALL_LABEL_FONT),
            text="Chain",
            variable=self.radio_var,
            value="chain"
        )
        self.radio_chain.grid(row=0, column=2, sticky="nsew", padx=(0, DEFAULT_PAD), pady=DEFAULT_PAD)

        self.radio_frame.rowconfigure(0, weight=0)
        self.radio_frame.columnconfigure([0, 1, 2], weight=1, uniform="columns")

        options_label = NormalLabel(self, text="Options:", anchor="sw")
        options_label.grid(row=4, column=0, sticky="ew", padx=DEFAULT_PAD, pady=(0, DEFAULT_PAD))

        self.options_frame = VariableOptionsScrollframe(
            self, self.new_variable.variable_items.split("/") if self.new_variable.variable_items is not None else []
        )
        self.options_frame.grid(row=5, column=0, sticky="nsew", pady=(0, DEFAULT_PAD), padx=DEFAULT_PAD)

        self.rowconfigure([0, 1, 2, 3, 4], weight=0)
        self.rowconfigure(5, weight=1)
        self.columnconfigure(0, weight=1)

        self.grab_set()
        self.after(10, self.name_entry.focus_set)
        self.wait_window()
