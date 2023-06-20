import customtkinter as ctk
from ..settings import *
from ..containers import IndividualPiece
from typing import Callable
from .auto_insert_button_frame import AutoInsertButtons


class EditPieceFrame(ctk.CTkFrame):
    def __init__(self,
                 master,
                 edit_command: Callable):
        super().__init__(master)

        self.current_piece: IndividualPiece | None = None
        self.edit_command = edit_command

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

        self.piece_textbox.bind("<KeyRelease>", lambda event: self.refresh_tags())

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

        self.inserts_frame.rowconfigure(0, weight=0)
        self.inserts_frame.columnconfigure(0, weight=1)

        self.rowconfigure(0, weight=0)
        self.rowconfigure([1, 2], weight=1, uniform="rows")
        self.columnconfigure(0, weight=1)

    def display_piece(self, piece: IndividualPiece | None):
        if piece is not None:
            self.current_piece = piece
            self.piece_textbox.delete("1.0", "end")
            self.piece_textbox.insert("1.0", self.current_piece.piece_text)
            self.refresh_tags()
            self.piece_textbox.focus_set()
        else:
            self.piece_textbox.delete("1.0", "end")

    def refresh_tags(self):
        self.edit_command(self.current_piece, self.piece_textbox.get("1.0", "end"))
        all_tags = self.piece_textbox.tag_names()
        current_line = 1
        current_tag_start_index = -1
        current_tag_end_index = 0
        in_tag = False
        current_tag = ""
        for char in self.current_piece.piece_text:
            if char == "\n":
                current_line += 1
                current_tag_start_index = -1
                continue

            if self.piece_textbox.tag_names(f"{current_line}.{current_tag_start_index+1}"):
                current_tag_start_index += 1
            elif in_tag and char != "}":
                current_tag_end_index += 1
                current_tag += char
            elif char == "{":
                current_tag_start_index += 1
                current_tag_end_index = current_tag_start_index
                current_tag = char
                in_tag = True
            elif char == "}":
                current_tag += char
                current_tag_end_index += 1
                in_tag = False
                if ":" in current_tag:
                    final_tag = current_tag.split(":")[0][1::]
                else:
                    final_tag = current_tag[1:-1]
                if final_tag in all_tags:
                    self.piece_textbox.tag_add(
                        final_tag,
                        f"{current_line}.{current_tag_start_index}",
                        f"{current_line}.{current_tag_end_index + 1}")

                current_tag = ""
                current_tag_start_index = current_tag_end_index
                current_tag_end_index = 0
            else:
                current_tag_start_index += 1

        self.piece_textbox.update()

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

        self.piece_textbox.insert("insert", pronoun_text, "pronoun")
        self.edit_command(self.current_piece, self.piece_textbox.get("1.0", "end"))

    def insert_pronoun_dependant(self, value: str):
        new_value = "{dependant:" + value + "}"
        self.piece_textbox.insert("insert", new_value, "dependant")
        self.edit_command(self.current_piece, self.piece_textbox.get("1.0", "end"))

    def insert_name(self):
        self.piece_textbox.insert("insert", "{name}", "name")
        self.edit_command(self.current_piece, self.piece_textbox.get("1.0", "end"))
