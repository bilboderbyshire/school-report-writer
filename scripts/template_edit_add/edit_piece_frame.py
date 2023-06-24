import customtkinter as ctk
from ..settings import *
from ..containers import IndividualPiece, UserVariable
from ..components import NormalLabel
from typing import Callable
from .auto_insert_button_frame import AutoInsertButtons
from .user_variables_button_frame import UserVariablesButtonFrame


class EditPieceFrame(ctk.CTkFrame):
    def __init__(self,
                 master,
                 variables_collection: dict[str, UserVariable],
                 edit_command: Callable,
                 create_variable_command: Callable,
                 edit_variable_command: Callable,
                 copy_variable_command: Callable):
        super().__init__(master)

        self.current_piece: IndividualPiece | None = None
        self.variables_collection = variables_collection
        self.edit_command = edit_command
        self.create_variable_command = create_variable_command
        self.edit_variable_command = edit_variable_command
        self.copy_variable_command = copy_variable_command
        self.after_cancel_id = None

        title_label = NormalLabel(
            self,
            anchor="w",
            text="Edit piece")

        title_label.grid(row=0, column=0, sticky="nw", padx=13, pady=(5, 6))

        self.piece_textbox = ctk.CTkTextbox(
            self,
            font=ctk.CTkFont(**SMALL_LABEL_FONT),
            fg_color="transparent",
            border_width=2,
            wrap="word",
            height=10,
            undo=True,
        )
        self.piece_textbox.grid(row=1, column=0, sticky="nsew", padx=13, pady=SMALL_PAD)

        self.piece_textbox.bind("<KeyPress>", lambda event: self.refresh_tags())
        self.piece_textbox.bind("<KeyRelease>", lambda event: self.edit_command(self.current_piece,
                                                                                self.piece_textbox.get("1.0", "end")))

        self.piece_textbox.tag_config("pronoun", foreground=PRONOUN_COLOUR)
        self.piece_textbox.tag_config("dependant", foreground=PRONOUN_DEPENDANT_COLOUR)
        self.piece_textbox.tag_config("name", foreground=NAME_COLOUR)
        self.piece_textbox.tag_config("static", foreground=USER_STATIC)
        self.piece_textbox.tag_config("choice", foreground=USER_CHOICE)
        self.piece_textbox.tag_config("chain", foreground=USER_CHAIN)

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
            self.inserts_frame,
            variables_collection=variables_collection,
            insert_variable_command=self.insert_user_variable,
            create_variable_command=self.create_variable_command,
            edit_variable_command=self.edit_variable_command,
            copy_variable_command=self.copy_variable_command
        )
        self.user_inserts.grid(row=1, column=0, sticky="nsew")

        self.piece_textbox.tag_bind("choice", "<Button-1>", lambda event: self.tag_clicked(event, "choice"))
        self.piece_textbox.tag_bind("static", "<Button-1>", lambda event: self.tag_clicked(event, "static"))
        self.piece_textbox.tag_bind("chain", "<Button-1>", lambda event: self.tag_clicked(event, "chain"))

        self.inserts_frame.rowconfigure(0, weight=0)
        self.inserts_frame.rowconfigure(1, weight=1)
        self.inserts_frame.columnconfigure(0, weight=1)

        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=2, uniform="rows")
        self.rowconfigure(2, weight=3, uniform="rows")
        self.columnconfigure(0, weight=1)

    def tag_clicked(self, event, tag):
        index = self.piece_textbox.index("@%s,%s" % (event.x, event.y))
        # get the indices of all "adj" tags
        tag_indices = list(self.piece_textbox.tag_ranges(tag))

        variable = ""
        # iterate them pairwise (start and end index)
        for start, end in zip(tag_indices[0::2], tag_indices[1::2]):
            # check if the tag matches the mouse click index
            if self.piece_textbox.compare(start, '<=', index) and self.piece_textbox.compare(index, '<', end):
                # return string between tag start and end
                variable = self.piece_textbox.get(start, end).split(":")[1][0:-1]

        self.user_inserts.variable_selected(variable)
        self.user_inserts.select_variable.set(variable.capitalize())

    def display_piece(self, piece: IndividualPiece | None):
        if piece is not None:
            self.piece_textbox.configure(state="normal")
            self.current_piece = piece
            self.piece_textbox.delete("1.0", "end")
            self.piece_textbox.insert("1.0", self.current_piece.piece_text)
            self.current_piece.find_tags_in_piece(self.piece_textbox, self.variables_collection)
            self.piece_textbox.focus_set()
            self.auto_inserts.enable_all()
            self.user_inserts.enable_all()
        else:
            self.piece_textbox.delete("1.0", "end")
            self.piece_textbox.configure(state="disabled")
            self.auto_inserts.disable_all()
            self.user_inserts.disable_all()

    def refresh_tags(self):
        if self.after_cancel_id is not None:
            self.after_cancel(self.after_cancel_id)

        self.after_cancel_id = self.after(1000, self.current_piece.find_tags_in_piece,
                                          self.piece_textbox,
                                          self.variables_collection)

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

    def insert_user_variable(self, user_variable: UserVariable):
        variable = "{" + f"{user_variable.variable_type}:" + user_variable.variable_name + "}"
        variable_name = user_variable.variable_type
        self.new_variable_inserted(variable, variable_name)
