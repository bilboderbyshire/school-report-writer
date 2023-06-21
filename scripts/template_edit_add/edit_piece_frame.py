import customtkinter as ctk
from ..settings import *
from ..containers import IndividualPiece
from typing import Callable
from .auto_insert_button_frame import AutoInsertButtons
from .user_variables_button_frame import UserVariablesButtonFrame


class EditPieceFrame(ctk.CTkFrame):
    def __init__(self,
                 master,
                 edit_command: Callable):
        super().__init__(master)

        self.current_piece: IndividualPiece | None = None
        self.edit_command = edit_command
        self.after_cancel_id = None

        title_label = ctk.CTkLabel(
            self,
            font=ctk.CTkFont(**NORMAL_LABEL_FONT),
            anchor="w",
            fg_color="transparent",
            text="Edit piece")

        title_label.grid(row=0, column=0, sticky="nw", padx=13, pady=(5, 6))

        self.piece_textbox = ctk.CTkTextbox(
            self,
            font=ctk.CTkFont(**SMALL_LABEL_FONT),
            fg_color="transparent",
            border_width=2,
            wrap="word",
            undo=True,
        )
        self.piece_textbox.grid(row=1, column=0, sticky="nsew", padx=13, pady=DEFAULT_PAD)

        self.piece_textbox.bind("<KeyPress>", lambda event: self.refresh_tags())
        self.piece_textbox.bind("<KeyRelease>", lambda event: self.edit_command(self.current_piece,
                                                                                self.piece_textbox.get("1.0", "end")))

        self.piece_textbox.tag_config("pronoun", foreground=PRONOUN_COLOUR)
        self.piece_textbox.tag_config("dependant", foreground=PRONOUN_DEPENDANT_COLOUR)
        self.piece_textbox.tag_config("name", foreground=NAME_COLOUR)

        self.inserts_frame = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )
        self.inserts_frame.grid(row=2, column=0, sticky="nsew", padx=13, pady=(0, DEFAULT_PAD))

        self.auto_inserts = AutoInsertButtons(
            self.inserts_frame,
            insert_pronoun_command=self.insert_pronoun,
            insert_pronoun_dependant_command=self.insert_pronoun_dependant,
            insert_name_command=self.insert_name
        )
        self.auto_inserts.grid(row=0, column=0, sticky="nsew", pady=(0, SMALL_PAD))

        self.user_inserts = UserVariablesButtonFrame(
            self.inserts_frame
        )
        self.user_inserts.grid(row=1, column=0, sticky="nsew")

        self.inserts_frame.rowconfigure(0, weight=0)
        self.inserts_frame.rowconfigure(1, weight=1)
        self.inserts_frame.columnconfigure(0, weight=1)

        self.rowconfigure(0, weight=0)
        self.rowconfigure([1, 2], weight=1, uniform="rows")
        self.columnconfigure(0, weight=1)

    def display_piece(self, piece: IndividualPiece | None):
        if piece is not None:
            self.current_piece = piece
            self.piece_textbox.delete("1.0", "end")
            self.piece_textbox.insert("1.0", self.current_piece.piece_text)
            self.current_piece.find_tags_in_piece(self.piece_textbox)
            self.piece_textbox.focus_set()
        else:
            self.piece_textbox.delete("1.0", "end")

    def refresh_tags(self):
        if self.after_cancel_id is not None:
            self.after_cancel(self.after_cancel_id)

        self.after_cancel_id = self.after(1000, self.current_piece.find_tags_in_piece, self.piece_textbox)

    def insert_pronoun(self, value: str):
        new_pronoun = value.split(":")[0].lower()

        if new_pronoun == "subjective":
            pronoun_text = "{pronoun:he/she/they}"
        elif new_pronoun == "objective":
            pronoun_text = "{pronoun:him/her/them}"
        elif new_pronoun == "possessive":
            pronoun_text = "{pronoun:his/her/their}"
        elif new_pronoun == "possessive adj":
            pronoun_text = "{pronoun:his/hers/theirs}"
        elif new_pronoun == "reflexive":
            pronoun_text = "{pronoun:himself/herself/themself}"
        else:
            pronoun_text = "{Unknown pronoun}"

        self.new_variable_inserted(pronoun_text, "pronoun")

    def insert_pronoun_dependant(self, value: str):
        new_value = "{dependant:" + value + "}"
        self.new_variable_inserted(new_value, "dependant")

    def insert_name(self):
        self.new_variable_inserted("{name}", "name")

    def new_variable_inserted(self, variable: str, variable_name: str):
        self.piece_textbox.insert("insert", variable, variable_name)
        self.edit_command(self.current_piece, self.piece_textbox.get("1.0", "end"))

        if variable_name in self.current_piece.variables.keys():
            self.current_piece.variables[variable_name].append(variable)
        else:
            self.current_piece.variables[variable_name] = [variable]
