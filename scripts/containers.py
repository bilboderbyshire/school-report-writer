from typing import TypedDict


class NewPieceRecord:
    def __init__(self, piece_id: str, section: int):
        self.id = piece_id
        self.piece_text = "New piece"
        self.section = section
        self.created = "Just now"
        self.updated = "now"
        self.expand = {}


class NewTemplateRecord:
    def __init__(self, template_id, template_title):
        self.id = template_id
        self.template_title = template_title
        self.created = "Just now"
        self.updated = "Just now"
        self.owner = None
        self.expand = {}


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

    @staticmethod
    def _is_valid_operand(other):
        return hasattr(other, "username") and \
            hasattr(other, "email") and \
            hasattr(other, "forename") and \
            hasattr(other, "surname") and \
            hasattr(other, "created") and \
            hasattr(other, "updated") and \
            hasattr(other, "id")

    def copy(self):
        return User(self)

    def __eq__(self, other):
        if not self._is_valid_operand(other):
            return NotImplemented

        return ((self.id,
                 self.username,
                 self.email,
                 self.forename,
                 self.surname,
                 self.created,
                 self.updated) == (
                    other.id,
                    other.username,
                    other.email,
                    other.forename,
                    other.surname,
                    other.created,
                    other.updated
                ))

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
        self.expand = {}

        try:
            if "owner" in record.expand.keys():
                self.owner = User(record.expand["owner"])
                self.expand["owner"] = record.expand["owner"]
            else:
                self.owner = None
        except AttributeError:
            self.owner = None

    @staticmethod
    def _is_valid_operand(other):
        return hasattr(other, "template_title") and \
               hasattr(other, "created") and \
               hasattr(other, "updated") and \
               hasattr(other, "id")

    def copy(self):
        return ReportTemplate(self)

    def __eq__(self, other):
        if not self._is_valid_operand(other):
            return NotImplemented

        return ((self.id,
                 self.template_title,
                 self.owner,
                 self.created,
                 self.updated) == (
            other.id,
            other.template_title,
            other.owner,
            other.created,
            other.updated))

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

        try:
            if "template" in record.expand.keys():
                self.template = ReportTemplate(record.expand["template"])
                self.expand["template"] = record.expand["template"]
            else:
                self.template = None
        except AttributeError:
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
