import random
from typing import TypedDict, Any



class Response(TypedDict):
    response: bool
    message: str


class UserCreation(TypedDict):
    forename: str
    surname: str
    email: str
    emailVisibility: bool
    password: str
    passwordConfirm: str


class User:
    def __init__(self, record):
        self.response_object = record
        self.id = record.id
        self.username = record.username
        self.email = record.email
        self.forename = record.forename
        self.surname = record.surname
        self.created = record.created
        self.updated = record.updated

    def __repr__(self):
        return str({
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'forename': self.forename,
            'created': self.created,
            'updated': self.updated
        })


class ReportTemplate:
    def __init__(self, record):
        self.response_object = record
        self.id = record.id
        self.template_title = record.template_title
        self.created = record.created
        self.updated = record.updated

        if "owner" in record.expand.keys():
            self.owner = User(record.expand["owner"])
        else:
            self.owner = None

    def __repr__(self):
        return str({
            "id": self.id,
            "template_title": self.template_title,
            "owner": repr(self.owner),
            "created": self.created,
            "updated": self.updated
        })


class SingleReportSet:
    def __init__(self, record):
        self.response_object = record
        self.id = record.id
        self.report_title = record.report_title
        self.class_name = record.class_name
        self.report_number = record.report_number
        self.report_completed = record.report_completed
        self.created = record.created
        self.updated = record.updated

        if "user" in record.expand.keys():
            self.user = User(record.expand["user"])
        else:
            self.user = None

        if "template" in record.expand.keys():
            self.template = ReportTemplate(record.expand["template"])
        else:
            self.template = None

    def __repr__(self):
        return str({
            "id": self.id,
            "report_title": self.report_title,
            "class_name": self.class_name,
            "report_number": self.report_number,
            "report_completed": self.report_completed,
            "user": repr(self.user),
            "template": repr(self.template),
            "created": self.created,
            "updated": self.updated
        })


class IndividualReport:
    def __init__(self, record):
        self.response_object = record
        self.id = record.id
        self.report_text = record.report_text
        self.completed = record.completed
        self.created = record.created
        self.updated = record.updated

        if "user" in record.expand.keys():
            self.user = User(record.expand["user"])
        else:
            self.user = None

        if "report_set" in record.expand.keys():
            self.report_set = SingleReportSet(record.expand["report_set"])
        else:
            self.report_set = None

    def __repr__(self):
        return str({
            "id": self.id,
            "report_text": self.report_text,
            "completed": self.completed,
            "user": repr(self.user),
            "report_set": repr(self.report_set),
            "created": self.created,
            "updated": self.updated
        })


class IndividualPiece:
    def __init__(self, record):
        self.response_object = record
        self.id = record.id
        self.piece_text = record.piece_text
        self.section = record.section
        self.created = record.created
        self.updated = record.updated
        self.expand = {}

        if "template" in record.expand.keys():
            self.template = ReportTemplate(record.expand["template"])
            self.expand["template"] = record.expand["template"]
        else:
            self.template = None

    @staticmethod
    def _is_valid_operand(other):
        return hasattr(other, "piece_text") and \
               hasattr(other, "section") and \
               hasattr(other, "created") and \
               hasattr(other, "updated") and \
               hasattr(other, "template") and \
               hasattr(other, "id")

    def copy(self):
        return IndividualPiece(self)

    def __eq__(self, other):
        if not self._is_valid_operand(other):
            return NotImplemented

        return ((self.id,
                 self.piece_text,
                 self.section,
                 self.created,
                 self.updated,
                 self.template) == (
            other.id,
            other.piece_text,
            other.section,
            other.created,
            other.updated,
            other.template
        ))

    def __repr__(self):
        return str({
            "id": self.id,
            "piece_text": self.piece_text,
            "template": repr(self.template),
            "section": self.section,
            "created": self.created,
            "updated": self.updated
        })


class TemplateWithPieces:
    def __init__(self, template: ReportTemplate | None, pieces_list: list[IndividualPiece]):
        self.template = template
        self.pieces_list = pieces_list

        self.pieces_structured: dict[int, list[IndividualPiece]] = {}

        for piece in self.pieces_list:
            if piece.section in self.pieces_structured.keys():
                self.pieces_structured[piece.section].append(piece)
            else:
                self.pieces_structured[piece.section] = [piece]

        self.copy_of_pieces = self.make_copy_of_structured_pieces()

        print(self.copy_of_pieces == self.pieces_structured)

        self.copy_of_pieces[1][0].piece_text = "changed"

        print(self.copy_of_pieces == self.pieces_structured)

        print(self.pieces_structured)
        print(self.copy_of_pieces)

    def __repr__(self):
        return_dict = {}
        for key, value in self.pieces_structured.items():
            return_dict[key] = [repr(i) for i in value]
        return_string = ""
        for key, value in return_dict.items():
            return_string += f"{key}: "
            for j in value:
                return_string += f"{j}\n"
        return return_string

    def make_copy_of_structured_pieces(self):
        return_dict = {}
        for key, value in self.pieces_structured.items():
            return_dict[key] = [i.copy() for i in value]

        return return_dict


class TestPieceRecord:
    def __init__(self, section, piece_num):
        self.id = "aegergadfgarg"
        self.piece_text = f"piece {piece_num}"
        self.section = section
        self.created = "yesterday"
        self.updated = "now"
        self.expand = {}


list_of_pieces = [IndividualPiece(TestPieceRecord(random.randint(1, 3), i)) for i in range(7)]
copy_of_pieces = list_of_pieces.copy()


newTest = TemplateWithPieces(None, list_of_pieces)


# print(list_of_pieces == copy_of_pieces)
#
# copy_of_pieces[0].piece_text = "Changed"
#
# print(list_of_pieces == copy_of_pieces)
#
# print(list_of_pieces)
# print(copy_of_pieces)



