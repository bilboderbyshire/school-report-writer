import customtkinter as ctk
from ..settings import *
from ..containers import IndividualPiece, UserVariable, PupilInfo
from typing import Callable


class ReportTextFrame(ctk.CTkFrame):
    def __init__(self,
                 master,
                 variables_collection: dict[str, UserVariable],
                 pupil_info: PupilInfo,
                 text_box_edited_command: Callable):
        super().__init__(master, fg_color=DARK_FRAME_COLOR)

        self.variables_collection = variables_collection
        self.pupil_info = pupil_info
        self.text_box_edited_command = text_box_edited_command
        self.edit_after_id = None

        self.piece_textbox = ctk.CTkTextbox(
            self,
            font=ctk.CTkFont(**SMALL_LABEL_FONT),
            fg_color="transparent",
            border_width=2,
            wrap="word",
            height=10,
            undo=True,
        )
        self.piece_textbox.grid(row=0, column=0, sticky="nsew", **SMALL_PAD_COMPLETE)

        self.piece_textbox.tag_config("pronoun", foreground=PRONOUN_COLOUR)
        self.piece_textbox.tag_config("dependant", foreground=PRONOUN_DEPENDANT_COLOUR)
        self.piece_textbox.tag_config("name", foreground=NAME_COLOUR)
        self.piece_textbox.tag_config("static", foreground=USER_STATIC)
        self.piece_textbox.tag_config("choice", foreground=USER_CHOICE)
        self.piece_textbox.tag_config("chain", foreground=USER_CHAIN)

        info_frame = ctk.CTkFrame(self, fg_color="transparent")
        info_frame.grid(row=1, column=0, sticky="nsew", padx=SMALL_PAD, pady=(0, SMALL_PAD))

        info_frame.rowconfigure(0, weight=0)
        info_frame.columnconfigure(0, weight=1)

        info_title_label = ctk.CTkLabel(
            info_frame,
            fg_color="transparent",
            font=ctk.CTkFont(**NORMAL_LABEL_FONT),
            anchor="w",
            text="Info"
        )
        info_title_label.grid(row=0, column=0, sticky="w", padx=SMALL_PAD, pady=(0, SMALL_PAD))

        self.piece_textbox.bind("<KeyRelease>", lambda event: self.delayed_text_edit_refresh())

        self.rowconfigure(0, weight=2, uniform="rows")
        self.rowconfigure(1, weight=1, uniform="rows")
        self.columnconfigure(0, weight=1)

    def insert_piece(self, piece: IndividualPiece) -> dict[str, list[str]]:
        variables_found: dict[str, list[str]] = {
            "static": [],
            "choice": [],
            "chain": []
        }

        current_tag = ""
        in_tag = False
        first_char_in_sentence = True
        for char in piece.piece_text:
            if char in "?!.":
                first_char_in_sentence = True

            if not in_tag and char != "{":
                self.piece_textbox.insert("insert", char)
            elif not in_tag and char == "{":
                current_tag += char
                in_tag = True
            elif in_tag and char == "{":
                self.piece_textbox.insert("insert", current_tag)
                current_tag = char
            elif in_tag and char != "}":
                current_tag += char
            elif in_tag and char == "}":
                in_tag = False
                current_tag += char
                if current_tag == "{name}":
                    self.piece_textbox.insert("insert", self.pupil_info["forename"].capitalize(), "name")
                elif ":" in current_tag:
                    tag_name, tag_info = current_tag[1:-1].split(":")

                    if tag_name == "pronoun":
                        pronoun_options = tag_info.split("/")
                        if first_char_in_sentence:
                            pronoun_options = [i.capitalize() for i in pronoun_options]

                        if self.pupil_info["gender"].lower() == "m":
                            self.piece_textbox.insert("insert", pronoun_options[0], "pronoun")
                        elif self.pupil_info["gender"].lower() == "f":
                            self.piece_textbox.insert("insert", pronoun_options[1], "pronoun")
                        else:
                            self.piece_textbox.insert("insert", pronoun_options[2], "pronoun")
                    elif tag_name == "dependant":
                        pronoun_options = tag_info.split("/")
                        if self.pupil_info["gender"].lower() == "nb":
                            self.piece_textbox.insert("insert", pronoun_options[1], "dependant")
                        else:
                            self.piece_textbox.insert("insert", pronoun_options[0], "dependant")
                    elif tag_name in ["static", "choice", "chain"]:
                        if tag_info in [i.variable_name for i in self.variables_collection.values()]:
                            variables_found[tag_name].append(tag_info)
                            self.piece_textbox.insert("insert", current_tag, (tag_name, tag_info))
                        else:
                            self.piece_textbox.insert("insert", current_tag)
                    else:
                        self.piece_textbox.insert("insert", current_tag)
                else:
                    self.piece_textbox.insert("insert", current_tag)
                current_tag = ""

            if not in_tag and char not in "?!. ":
                first_char_in_sentence = False

        self.piece_textbox.insert("insert", " ")

        return variables_found

    def edit_variable(self, variable_type: str, variable_name: str, index: int, new_text: str):
        tag_ranges = self.piece_textbox.tag_ranges(variable_type)
        tag_range = list(zip(tag_ranges[0::2], tag_ranges[1::2]))[index]

        self.piece_textbox.delete(tag_range[0], tag_range[1])

        if new_text != "":
            if tag_range[0] == "1.0":
                new_text = new_text.capitalize()
            else:
                prev_char = self.piece_textbox.get(tag_range[0].string + "-1c")
                prev_2_char = self.piece_textbox.get(tag_range[0].string + "-2c")

                if prev_char in ["!?.\n"] or prev_2_char in ["!?.\n"]:
                    new_text = new_text.capitalize()
                else:
                    new_text = new_text.lower()

            self.piece_textbox.insert(tag_range[0], new_text, variable_type)
        else:
            self.piece_textbox.insert(tag_range[0], "{static:" + variable_name + "}", variable_type)

    def edit_static_variable(self, variable_name: str, new_text: str):
        tag_ranges = self.piece_textbox.tag_ranges(variable_name)

        current_tag_start = tag_ranges[0]
        current_tag_end = tag_ranges[1]
        for i in range(len(tag_ranges)//2):
            self.piece_textbox.delete(current_tag_start, current_tag_end)

            if new_text != "":
                if current_tag_start == "1.0":
                    new_text = new_text.capitalize()
                else:
                    prev_char = self.piece_textbox.get(current_tag_start.string + "-1c")
                    prev_2_char = self.piece_textbox.get(current_tag_start.string + "-2c")

                    if prev_char in ["!?.\n"] or prev_2_char in ["!?.\n"]:
                        new_text = new_text.capitalize()
                    else:
                        new_text = new_text.lower()

                self.piece_textbox.insert(current_tag_start, new_text, ("static", variable_name))
            else:
                self.piece_textbox.insert(current_tag_start, "{static:" + variable_name + "}",
                                          ("static", variable_name))
            try:
                current_tag_start, current_tag_end = self.piece_textbox.tag_nextrange(variable_name, current_tag_end)
            except ValueError:
                break

    def text_box_edited(self):
        variables_found: dict[str, list[str]] = {
            "static": [],
            "choice": [],
            "chain": []
        }

        for var_type in ["static", "choice", "chain"]:
            tag_ranges = self.piece_textbox.tag_ranges(var_type)
            if var_type == "static":
                for start in tag_ranges[0::2]:
                    tag_name = self.piece_textbox.tag_names(start)[1]
                    variables_found[var_type].append(tag_name)
            elif var_type == "choice":
                for start, end in zip(tag_ranges[0::2], tag_ranges[1::2]):
                    tag_value = self.piece_textbox.get(start, end)
                    variables_found[var_type].append(tag_value)
            else:
                for start, end in zip(tag_ranges[0::2], tag_ranges[1::2]):
                    tag_value = self.piece_textbox.get(start, end)
                    variables_found[var_type].append(tag_value)

        self.text_box_edited_command(variables_found)
        self.edit_after_id = None

    def delayed_text_edit_refresh(self):
        if self.edit_after_id is not None:
            self.after_cancel(self.edit_after_id)

        self.edit_after_id = self.after(1000, self.text_box_edited)
