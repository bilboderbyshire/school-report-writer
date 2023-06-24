import customtkinter as ctk
from ..settings import *
from ..containers import UserVariable
from ..title_bar import TitleLabel
from ..components import SingleLineEntry, NormalLabel, SecondaryButton, WarningButton
from .new_variable_options_scrollframe import VariableOptionsScrollframe
import CTkMessagebox as ctkmb
import os
from typing import Literal


class VariableEditToplevel(ctk.CTkToplevel):
    def __init__(self, master,
                 variable_to_edit: UserVariable,
                 variable_collection: dict[str, UserVariable],
                 edit_type: Literal["edit", "copy", "add"],
                 top_level_choice_tracker: ctk.StringVar):
        super().__init__(master,
                         fg_color=ROOT_BG)

        self.choice_tracker = top_level_choice_tracker
        self.edit_type = edit_type
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
        self.name_entry.bind("<FocusOut>", lambda event: self.refill_empty_name())

        self.radio_frame = ctk.CTkFrame(self)
        self.radio_frame.grid(row=3, column=0, sticky="nsew", pady=(0, DEFAULT_PAD), padx=DEFAULT_PAD)

        self.radio_var = ctk.StringVar(value=self.new_variable.variable_type)
        self.radio_static = ctk.CTkRadioButton(
            self.radio_frame,
            font=ctk.CTkFont(**SMALL_LABEL_FONT),
            text="Static",
            variable=self.radio_var,
            value="static",
            command=self.radio_clicked
        )
        self.radio_static.grid(row=0, column=0, sticky="nsew", **DEFAULT_PAD_COMPLETE)

        self.radio_choice = ctk.CTkRadioButton(
            self.radio_frame,
            font=ctk.CTkFont(**SMALL_LABEL_FONT),
            text="Choice",
            variable=self.radio_var,
            value="choice",
            command=self.radio_clicked
        )
        self.radio_choice.grid(row=0, column=1, sticky="nsew", padx=(0, DEFAULT_PAD), pady=DEFAULT_PAD)

        self.radio_chain = ctk.CTkRadioButton(
            self.radio_frame,
            font=ctk.CTkFont(**SMALL_LABEL_FONT),
            text="Chain",
            variable=self.radio_var,
            value="chain",
            command=self.radio_clicked
        )
        self.radio_chain.grid(row=0, column=2, sticky="nsew", padx=(0, DEFAULT_PAD), pady=DEFAULT_PAD)

        self.radio_frame.rowconfigure(0, weight=0)
        self.radio_frame.columnconfigure([0, 1, 2], weight=1, uniform="columns")

        self.options_frame = VariableOptionsScrollframe(
            self, self.new_variable.variable_items.split("/") if self.new_variable.variable_items is not None else []
        )
        self.options_frame.grid(row=4, column=0, sticky="nsew", pady=(0, DEFAULT_PAD), padx=DEFAULT_PAD)

        self.buttons_frame = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )
        self.buttons_frame.grid(row=5, column=0, sticky="nsew", pady=(0, DEFAULT_PAD), padx=DEFAULT_PAD)
        self.buttons_frame.rowconfigure(0, weight=0)
        self.buttons_frame.columnconfigure([0, 1, 2, 3], weight=1, uniform="columns")

        save_button = ctk.CTkButton(
            self.buttons_frame,
            text="Save",
            font=ctk.CTkFont(**NORMAL_LABEL_FONT),
            command=self.save_clicked
        )
        save_button.grid(row=0, column=1, sticky="nsew", padx=(0, SMALL_PAD))

        cancel_button = SecondaryButton(
            self.buttons_frame,
            text="Cancel",
            font=ctk.CTkFont(**NORMAL_LABEL_FONT),
            command=self.cancel_clicked
        )
        cancel_button.grid(row=0, column=2, sticky="nsew", padx=(0, SMALL_PAD))

        delete_button = WarningButton(
            self.buttons_frame,
            text="Delete",
            font=ctk.CTkFont(**NORMAL_LABEL_FONT),
            command=self.delete_clicked
        )
        delete_button.grid(row=0, column=3, sticky="nsew", padx=(0, SMALL_PAD))

        self.rowconfigure([0, 1, 2, 3, 5], weight=0)
        self.rowconfigure(4, weight=1)
        self.columnconfigure(0, weight=1)

        self.radio_clicked()
        self.grab_set()
        self.after(10, self.name_entry.focus_set)
        self.wait_window()

    def radio_clicked(self):
        if self.radio_var.get() == "static":
            self.options_frame.disabled()
        else:
            self.options_frame.enabled()

    def refill_empty_name(self):
        if self.name_entry.get().strip() == "":
            self.name_entry.delete(0, "end")
            self.name_entry.insert(0, self.original_title)

    def delete_clicked(self):
        warning_box = ctkmb.CTkMessagebox(
            title="Warning",
            message=f"Are you sure you want to delete the variable '{self.new_variable.variable_name}'"
                    f"\n\nYou will not be able to undo this move",
            icon="cancel",
            option_2="Yes",
            option_1="No")
        warning_box.wait_window()

        if warning_box.get() == "No":
            return
        else:
            self.choice_tracker.set("delete")
            self.destroy()

    def cancel_clicked(self):
        self.choice_tracker.set("cancel")
        self.destroy()

    def save_clicked(self):
        bad_chars = set("{}@:/")

        # Name validation
        if self.name_entry.get() == "New variable":
            self.name_entry.configure(border_color=BAD_COLOR)
            warning_box = ctkmb.CTkMessagebox(
                title="Warning",
                message=f"Please provide an appropriate name",
                icon="cancel",
                option_1="OK")
            warning_box.wait_window()
            return
        elif self.edit_type == "copy" and self.name_entry.get() == self.original_title:
            self.name_entry.configure(border_color=BAD_COLOR)
            warning_box = ctkmb.CTkMessagebox(
                title="Warning",
                message=f"This variable name already exists, please change the name",
                icon="cancel",
                option_1="OK")
            warning_box.wait_window()
            return
        elif self.name_entry.get() != self.original_title:
            all_current_names = [i.variable_name.lower() for i in self.variable_collection.values()]
            if self.name_entry.get().lower() in all_current_names:
                self.name_entry.configure(border_color=BAD_COLOR)
                warning_box = ctkmb.CTkMessagebox(
                    title="Warning",
                    message=f"This variable name already exists, please change the name",
                    icon="cancel",
                    option_1="OK")
                warning_box.wait_window()
                return
            else:
                if not bad_chars.isdisjoint(set(self.name_entry.get())):
                    self.name_entry.configure(border_color=BAD_COLOR)
                    warning_box = ctkmb.CTkMessagebox(
                        title="Warning",
                        message="Illegal character found in name. Please do not use {}@: or /",
                        icon="cancel",
                        option_1="OK")
                    warning_box.wait_window()
                    return

        self.name_entry.configure(border_color=("#979DA2", "#565B5E"))

        # Option validation
        if self.radio_var.get() != "static" and len(self.options_frame.all_cards.keys()) == 0:
            warning_box = ctkmb.CTkMessagebox(
                title="Warning",
                message="Can't make a non-static variable without options. Please set type to static or add options",
                icon="cancel",
                option_1="OK")
            warning_box.wait_window()
            return
        elif self.radio_var.get() == "static":
            self.new_variable.variable_items = None
        else:
            all_options = []
            card_failed = False
            for card in self.options_frame.all_cards.values():
                card_text = card.option_text.get()
                all_options.append(card_text)
                if not bad_chars.isdisjoint(set(card_text)):
                    card.configure(border_width=2, border_color=BAD_COLOR)
                    card_failed = True
                else:
                    card.configure(border_width=0)

            if card_failed:
                warning_box = ctkmb.CTkMessagebox(
                    title="Warning",
                    message="Illegal character found in options. Please do not use {}@: or /",
                    icon="cancel",
                    option_1="OK")
                warning_box.wait_window()
                return

            self.new_variable.variable_items = "/".join(all_options)
        self.new_variable.variable_name = self.name_entry.get().lower()
        self.new_variable.variable_type = self.radio_var.get()

        self.choice_tracker.set("save")
        self.destroy()
