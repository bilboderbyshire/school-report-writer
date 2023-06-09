import customtkinter as ctk
from ..settings import *
from ..components import SecondaryOptionmenu, SecondaryButton
from ..containers import UserVariable
from typing import Callable


class UserVariablesButtonFrame(ctk.CTkFrame):
    def __init__(self,
                 master,
                 variables_collection: dict[str, UserVariable],
                 insert_variable_command: Callable,
                 create_variable_command: Callable,
                 edit_variable_command: Callable,
                 copy_variable_command: Callable):
        super().__init__(master,
                         fg_color="transparent")

        title_label = ctk.CTkLabel(
            self,
            font=ctk.CTkFont(**SMALL_LABEL_FONT),
            anchor="w",
            fg_color="transparent",
            text="Create variables")

        title_label.grid(row=0, column=0, columnspan=3, sticky="nw", pady=(5, 6))

        self.variables_collection = variables_collection
        self.chosen_variable: UserVariable | None = None

        self.variable_button_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.variable_button_frame.grid(row=1, column=0, sticky="nsew", padx=(0, SMALL_PAD), pady=(0, SMALL_PAD))

        self.select_variable = SecondaryOptionmenu(
            self.variable_button_frame,
            font=ctk.CTkFont(**VERY_SMALL_FONT),
            values=[i.variable_name.capitalize() for i in self.variables_collection.values()],
            command=self.variable_selected
        )
        self.select_variable.grid(row=0, column=0, sticky="ew", pady=(0, SMALL_PAD))
        self.select_variable.set("Choose...")

        self.create_variable_button = SecondaryButton(
            self.variable_button_frame,
            font=ctk.CTkFont(**VERY_SMALL_FONT),
            text="Create new...",
            state="normal",
            command=create_variable_command
        )
        self.create_variable_button.grid(row=1, column=0, sticky="ew", pady=(0, SMALL_PAD))

        self.insert_button = ctk.CTkButton(
            self.variable_button_frame,
            font=ctk.CTkFont(**VERY_SMALL_FONT),
            text="Insert",
            state="disabled",
            command=lambda: insert_variable_command(self.chosen_variable)
        )
        self.insert_button.grid(row=2, column=0, sticky="ew")

        self.variable_button_frame.rowconfigure([0, 1, 2], weight=0)
        self.variable_button_frame.columnconfigure(0, weight=1)

        self.variable_view_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.variable_view_frame.grid(row=1, column=1, sticky="nsew", pady=(0, SMALL_PAD))

        self.variable_textbox = ctk.CTkTextbox(
            self.variable_view_frame,
            font=ctk.CTkFont(**VERY_SMALL_FONT),
            fg_color="transparent",
            text_color=FADED_TEXT_COLOR,
            border_width=2,
            wrap="word",
            height=10,
            width=10,
        )
        self.variable_textbox.grid(row=0, column=0, columnspan=3, sticky="nsew", pady=(0, SMALL_PAD))
        self.variable_textbox.configure(state="disabled")

        self.edit_button = SecondaryButton(
            self.variable_view_frame,
            font=ctk.CTkFont(**VERY_SMALL_FONT),
            text="Edit",
            state="disabled",
            command=lambda: edit_variable_command(self.chosen_variable)
        )
        self.edit_button.grid(row=1, column=1, sticky="ew", padx=(0, SMALL_PAD), pady=(0, SMALL_PAD))

        self.copy_button = SecondaryButton(
            self.variable_view_frame,
            font=ctk.CTkFont(**VERY_SMALL_FONT),
            text="Copy",
            state="disabled",
            command=lambda: copy_variable_command(self.chosen_variable)
        )
        self.copy_button.grid(row=1, column=2, sticky="ew", pady=(0, SMALL_PAD))

        self.variable_view_frame.rowconfigure(0, weight=1)
        self.variable_view_frame.rowconfigure(1, weight=0)
        self.variable_view_frame.columnconfigure([0, 1, 2], weight=1, uniform="row")

        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1, uniform="columns")
        self.columnconfigure(1, weight=2, uniform="columns")

    def disable_all(self):
        self.select_variable.set("Choose...")
        self.select_variable.configure(state="disabled")
        self.insert_button.configure(state="disabled")
        self.copy_button.configure(state="disabled")
        self.edit_button.configure(state="disabled")
        self.variable_textbox.configure(state="normal")
        self.variable_textbox.delete("1.0", "end")
        self.variable_textbox.configure(state="disabled")

    def enable_all(self):
        self.select_variable.configure(state="enabled")

    def variable_selected(self, variable_name: str | None):
        self.variable_textbox.configure(state="normal")
        self.variable_textbox.delete("1.0", "end")

        if variable_name is None:
            self.variable_textbox.configure(state="disabled")
            return

        for i in self.variables_collection.values():
            if i.variable_name.lower() == variable_name.lower():
                self.chosen_variable = i
                break

        if self.chosen_variable is not None:
            self.insert_button.configure(state="normal")
            self.copy_button.configure(state="normal")
            self.edit_button.configure(state="normal")
            if self.chosen_variable.variable_type == "static":
                self.variable_textbox.insert("1.0", self.chosen_variable.variable_name + " { }\n")
            else:
                self.variable_textbox.insert("1.0", self.chosen_variable.variable_name + " {\n")
                current_line = 2
                all_items = self.chosen_variable.variable_items.split("/")

                for value in all_items:
                    self.variable_textbox.insert(f"{current_line}.0", f"\t{value},\n")
                    current_line += 1

                self.variable_textbox.insert(f"{current_line}.0", "}")

        self.variable_textbox.configure(state="disabled")

    def refresh_variable_dropdown(self, variable_to_watch: UserVariable | None):
        self.select_variable.configure(values=[i.variable_name.capitalize() for i in self.variables_collection.values()])
        if variable_to_watch is None:
            self.select_variable.set("Choose...")
            self.variable_selected(None)
        else:
            self.select_variable.set(variable_to_watch.variable_name.capitalize())
            self.variable_selected(variable_to_watch.variable_name)
