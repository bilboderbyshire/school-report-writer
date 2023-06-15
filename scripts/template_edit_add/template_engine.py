from ..containers import ReportTemplate, IndividualPiece, NewPieceRecord, Response
from typing import Literal
from ..database import RUNNING_DB
import asyncio


class TemplateEngine:
    def __init__(self, template: ReportTemplate, pieces_list: list[IndividualPiece]):
        self.template = template
        self.pieces_list = pieces_list

        # A dictionary, keyed by the section and storing a number that increments every time a new piece is added to a
        #  section. This number is used when generating placeholder ids for new pieces. This number doesn't decrement
        #  when a piece is deleted, meaning the IDs will always be unique to the section
        self.new_id_num_cache: dict[int, int] = {}

        self.pieces_structured: dict[int, dict[str, IndividualPiece]] = {}

        for piece in self.pieces_list:
            if piece.section in self.pieces_structured.keys():
                self.pieces_structured[piece.section][piece.id] = piece
                self.new_id_num_cache[piece.section] += 1
            else:
                self.pieces_structured[piece.section] = {piece.id: piece}
                self.new_id_num_cache[piece.section] = 0

        self.make_sections_sequential("main")
        self.copy_of_pieces = self.make_copy_of_structured_pieces()
        self.current_section = 1

    def make_sections_sequential(self, dict_of_choice: Literal["main", "copy"]):
        if dict_of_choice == "main":
            dict_to_change = self.pieces_structured
        else:
            dict_to_change = self.copy_of_pieces

        current_sections = sorted(dict_to_change.keys())
        temp_dict = {}

        for i in range(len(current_sections)):
            for key, value in dict_to_change[current_sections[i]].items():
                value.section = i+1
            temp_dict[i+1] = dict_to_change[current_sections[i]]

        if dict_of_choice == "main":
            self.pieces_structured = temp_dict
        else:
            self.copy_of_pieces = temp_dict

    def make_copy_of_structured_pieces(self) -> dict[int, dict[str, IndividualPiece]]:
        return_dict = {}
        for key, value in self.pieces_structured.items():
            return_dict[key] = {}
            for c_key, c_value in value.items():
                return_dict[key][c_key] = c_value.copy()

        return return_dict

    def change_current_section(self, new_section):
        self.current_section = new_section

    def get_sections_pieces(self) -> list[IndividualPiece]:
        return_list = []
        for key, value in self.copy_of_pieces[self.current_section].items():
            return_list.append(value)

        return return_list

    def get_section_nums(self) -> list[int]:
        return list(self.copy_of_pieces.keys())

    def get_working_template_dict(self) -> dict[int, dict[str, IndividualPiece]]:
        return self.copy_of_pieces

    def edit_piece(self, piece_id, new_piece):
        self.copy_of_pieces[self.current_section][piece_id].piece_text = new_piece

    def add_piece(self) -> str:
        new_id = f"@{self.new_id_num_cache[self.current_section]}"
        self.new_id_num_cache[self.current_section] += 1

        self.copy_of_pieces[self.current_section][new_id] = IndividualPiece(NewPieceRecord(new_id, self.current_section))

        return new_id

    def delete_piece(self, piece_id):
        self.copy_of_pieces[self.current_section].pop(piece_id)

    def add_section(self) -> int:
        new_section_num = max(self.copy_of_pieces.keys(), default=0) + 1
        self.new_id_num_cache[new_section_num] = 0
        self.copy_of_pieces[new_section_num] = {}
        return new_section_num

    def delete_section(self, section):
        self.copy_of_pieces.pop(section)
        self.make_sections_sequential("copy")

    def save_template_to_database(self):
        if "@" in self.template.id:
            response, created_template = RUNNING_DB.create_new_template(self.template)

            if not response["response"]:
                print(response["message"])
                return response
            else:
                self.template = ReportTemplate(created_template)

        temp_structured_pieces: dict[int, dict[str: IndividualPiece]] = {}

        for key, value in self.copy_of_pieces.items():
            temp_structured_pieces[key] = {}
            for c_key, c_value in value.items():
                response, result = self.__save_piece(c_value)
                if response["response"]:
                    temp_structured_pieces[key][result.id] = result
                else:
                    print(response["message"])
                    return response

        self.pieces_structured = temp_structured_pieces
        self.copy_of_pieces = self.make_copy_of_structured_pieces()

    def __save_piece(self, piece_to_save: IndividualPiece) -> tuple[Response, IndividualPiece]:
        if "@" in piece_to_save.id:
            print(f"Starting save for {piece_to_save.id}")
            response, result = RUNNING_DB.create_new_piece(piece_to_save, self.template)
        else:
            print(f"Starting update for {piece_to_save.id}")
            response, result = RUNNING_DB.update_piece(piece_to_save, self.template)

        return response, IndividualPiece(result)

    def check_changes(self) -> bool:
        return self.copy_of_pieces == self.pieces_structured

    def repr_copy(self, dict_to_repr="copy"):
        return_dict = {}
        if dict_to_repr == "copy":
            for key, value in self.copy_of_pieces.items():
                return_dict[key] = {}
                for c_key, c_value in value.items():
                    return_dict[key][c_key] = repr(c_value)
        else:
            for key, value in self.pieces_structured.items():
                return_dict[key] = {}
                for c_key, c_value in value.items():
                    return_dict[key][c_key] = repr(c_value)

        return_string = ""
        for key, value in return_dict.items():
            return_string += f"{key}: \n"
            for c_key, c_value in value.items():
                return_string += f"\t{c_key}: {c_value}\n"
        return return_string

    def __repr__(self):
        return self.repr_copy("main")

# print(newTest.repr_copy())
#
# # Add section
# input("Add section")
# newTest.add_section()
# print(newTest.repr_copy())
#
# # Delete section
# del_section = int(input("Delete section:"))
# newTest.delete_section(del_section)
# print(newTest.repr_copy())
#
# # New piece
# add_piece_section = int(input("New piece section"))
# newTest.add_piece(add_piece_section)
# print(newTest.repr_copy())
#
# # Edit piece
# edit_piece_section = int(input("Edit piece section:"))
# edit_piece_id = input("Edit piece id:")
# newTest.edit_piece(edit_piece_section, edit_piece_id, "CHANGES")
# print(newTest.repr_copy())
#
# # Delete piece
# del_piece_section = int(input("Delete piece section"))
# del_piece_id = input("Delete piece id:")
# newTest.delete_piece(del_piece_section, del_piece_id)
# print(newTest.repr_copy())
#
# input()
# print(newTest.check_changes())