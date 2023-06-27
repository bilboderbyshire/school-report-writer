from typing import TypedDict
from . import utils
import customtkinter as ctk


class NewUserVariableRecord:
    def __init__(self, var_id: str,
                 variable_name: str,
                 owner_id: str,
                 variable_items: str = None,
                 variable_type: str = "static",
                 ):
        self.id = var_id
        self.variable_name = variable_name
        self.variable_items = variable_items
        self.variable_type = variable_type
        self.owner = owner_id
        self.created = "Just now"
        self.updated = "Now"


class NewSectionRecord:
    def __init__(self, section_id: str,
                 section_title: str,
                 template_id: str):
        self.id = section_id
        self.section_title = section_title
        self.template = template_id
        self.created = "Just now"
        self.updated = "Now"
        self.expand = {}


class NewPieceRecord:
    def __init__(self, piece_id: str, section_id: str, piece_text: str = "New piece"):
        self.id = piece_id
        self.piece_text = piece_text
        self.section = section_id
        self.created = "Just now"
        self.updated = "Now"
        self.expand = {}


class NewTemplateRecord:
    def __init__(self, template_id: str, template_title: str, owner):
        self.id = template_id
        self.template_title = template_title
        self.created = "Just now"
        self.updated = "Now"
        self.owner: User = owner
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
    def __init__(self, record, password: str = None, password_confirm: str = None) -> None:
        self.response_object = record
        self.id = record.id
        self.username = record.username
        self.email = record.email
        self.email_visibility = record.email_visibility
        self.forename = record.forename
        self.surname = record.surname
        self.created = record.created
        self.updated = record.updated
        self.password = password
        self.password_confirm = password_confirm

    def copy(self):
        return User(self)

    def data_to_create(self) -> dict:
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "emailVisibility": self.email_visibility,
            "password": self.password,
            "passwordConfirm": self.password_confirm,
            "forename": self.forename,
            "surname": self.surname
        }

    @staticmethod
    def _is_valid_operand(other) -> bool:
        return hasattr(other, "username") and \
               hasattr(other, "email") and \
               hasattr(other, "forename") and \
               hasattr(other, "surname") and \
               hasattr(other, "created") and \
               hasattr(other, "updated") and \
               hasattr(other, "id")

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
    def __init__(self, record) -> None:
        self.response_object = record
        self.id = record.id
        self.template_title = record.template_title
        self.owner = None
        self.created = record.created
        self.updated = record.updated
        self.expand = {}

        try:
            if "owner" in record.expand.keys():
                self.owner = User(record.expand["owner"])
                self.expand["owner"] = record.expand["owner"]
            else:
                self.owner = record.owner
        except AttributeError:
            self.owner = record.owner

    def copy(self):
        return ReportTemplate(self)

    def data_to_create(self) -> dict:
        return {
            "template_title": self.template_title,
            "owner": self.owner if isinstance(self.owner, str) else self.owner.id
        }

    @staticmethod
    def _is_valid_operand(other):
        return hasattr(other, "template_title") and \
            hasattr(other, "owner") and \
            hasattr(other, "created") and \
            hasattr(other, "updated") and \
            hasattr(other, "id")

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
    def __init__(self, record) -> None:
        self.response_object = record
        self.id = record.id
        self.report_title = record.report_title
        self.class_name = record.class_name
        self.report_number = record.report_number
        self.report_completed = record.report_completed
        self.user = None
        self.template = None
        self.created = record.created
        self.updated = record.updated
        self.expand = {}

        try:
            if "user" in record.expand.keys():
                self.user = User(record.expand["user"])
                self.expand["user"] = record.expand["user"]
            else:
                self.user = record.user
        except AttributeError:
            self.user = record.user

        try:
            if "template" in record.expand.keys():
                self.template = ReportTemplate(record.expand["template"])
                self.expand["template"] = record.expand["template"]
            else:
                self.template = record.template
        except AttributeError:
            self.template = record.template

    def copy(self):
        return SingleReportSet(self)

    def data_to_create(self) -> dict:
        return {
            "report_title": self.report_title,
            "class_name": self.class_name,
            "report_number": self.report_number,
            "report_completed": self.report_completed,
            "user": self.user.id if self.user is not None else None,
            "template": self.template.id if self. template is not None else None
        }

    @staticmethod
    def _is_valid_operand(other):
        return hasattr(other, "id") and \
               hasattr(other, "report_title") and \
               hasattr(other, "class_name") and \
               hasattr(other, "report_number") and \
               hasattr(other, "report_completed") and \
               hasattr(other, "created") and \
               hasattr(other, "updated") and \
               hasattr(other, "user") and \
               hasattr(other, "template")

    def __eq__(self, other):
        if not self._is_valid_operand(other):
            return NotImplemented

        return ((self.id,
                 self.report_title,
                 self.class_name,
                 self.report_number,
                 self.report_completed,
                 self.user,
                 self.template,
                 self.created,
                 self.updated) == (
            other.id,
            other.report_title,
            other.class_name,
            other.report_number,
            other.report_completed,
            other.user,
            other.template,
            other.created,
            other.updated))

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
    def __init__(self, record) -> None:
        self.response_object = record
        self.id = record.id
        self.pupil_forename = record.pupil_forename
        self.pupil_surname = record.pupil_surname
        self.gender = record.gender
        self.report_text = record.report_text
        self.completed = record.completed
        self.user = None
        self.report_set = None
        self.created = record.created
        self.updated = record.updated
        self.expand = {}

        try:
            if "user" in record.expand.keys():
                self.user = User(record.expand["user"])
                self.expand["user"] = record.expand["user"]
            else:
                self.user = record.user
        except AttributeError:
            self.user = record.user

        try:
            if "report_set" in record.expand.keys():
                self.report_set = SingleReportSet(record.expand["report_set"])
                self.expand["report_set"] = record.expand["report_set"]
            else:
                self.report_set = record.report_set
        except AttributeError:
            self.report_set = record.report_set

    def copy(self):
        return IndividualReport(self)

    def data_to_create(self) -> dict:
        return {
            "pupil_forename": self.pupil_forename,
            "pupil_surname": self.pupil_surname,
            "gender": self.gender,
            "report_text": self.report_text,
            "completed": self.completed,
            "user": self.user if isinstance(self.user, str) else self.user.id,
            "report_set": self.report_set if isinstance(self.report_set, str) else self.report_set.id
        }

    @staticmethod
    def _is_valid_operand(other):
        return hasattr(other, "id") and \
               hasattr(other, "pupil_forename") and \
               hasattr(other, "pupil_surname") and \
               hasattr(other, "gender") and \
               hasattr(other, "report_text") and \
               hasattr(other, "completed") and \
               hasattr(other, "user") and \
               hasattr(other, "report_set") and \
               hasattr(other, "created") and \
               hasattr(other, "updated")

    def __eq__(self, other):
        if not self._is_valid_operand(other):
            return NotImplemented

        return ((self.id,
                 self.pupil_forename,
                 self.pupil_surname,
                 self.gender,
                 self.report_text,
                 self.user,
                 self.report_set,
                 self.completed,
                 self.created,
                 self.updated) == (
            other.id,
            other.pupil_forename,
            other.pupil_surname,
            other.gender,
            other.report_text,
            other.user,
            other.report_set,
            other.completed,
            other.created,
            other.updated))

    def __repr__(self):
        return str({
            "id": self.id,
            "pupil_forename": self.pupil_forename,
            "pupil_surname": self.pupil_surname,
            "gender": self.gender,
            "report_text": self.report_text,
            "completed": self.completed,
            "user": repr(self.user),
            "report_set": repr(self.report_set),
            "created": self.created,
            "updated": self.updated
        })


class TemplateSection:
    def __init__(self, record) -> None:
        self.response_object = record
        self.id = record.id
        self.section_title = record.section_title
        self.template = None
        self.created = record.created
        self.updated = record.updated
        self.expand = {}

        try:
            if "template" in record.expand.keys():
                self.template = ReportTemplate(record.expand["template"])
                self.expand["template"] = record.expand["template"]
            else:
                self.template = record.template
        except AttributeError:
            self.template = record.template

    def copy(self):
        return TemplateSection(self)

    def data_to_create(self) -> dict:
        return {
            "section_title": self.section_title,
            "template": self.template if isinstance(self.template, str) else self.template.id
        }

    @staticmethod
    def _is_valid_operand(other):
        return hasattr(other, "id") and \
               hasattr(other, "section_title") and \
               hasattr(other, "template") and \
               hasattr(other, "created") and \
               hasattr(other, "updated")

    def __eq__(self, other):
        if not self._is_valid_operand(other):
            return NotImplemented

        return ((self.id,
                 self.section_title,
                 self.template,
                 self.created,
                 self.updated) == (
            other.id,
            other.section_title,
            other.template,
            other.created,
            other.updated
        ))

    def __repr__(self):
        return str({
            "id": self.id,
            "section_title": self.section_title,
            "template": repr(self.template),
            "created": self.created,
            "updated": self.updated
        })


class UserVariable:
    def __init__(self, record):
        self.record_object = record
        self.id = record.id
        self.variable_name = record.variable_name
        self.variable_items = record.variable_items
        self.variable_type = record.variable_type
        self.owner = None
        self.created = record.created
        self.updated = record.updated
        self.expand = {}

        try:
            if "owner" in record.expand.keys():
                self.owner = User(record.expand["owner"])
                self.expand["owner"] = record.expand["owner"]
            else:
                self.owner = record.owner
        except AttributeError:
            self.owner = record.owner

    def copy(self):
        return UserVariable(self)

    def data_to_create(self) -> dict:
        return {
            "variable_name": self.variable_name,
            "variable_items": self.variable_items,
            "variable_type": self.variable_type,
            "owner": self.owner if isinstance(self.owner, str) else self.owner.id
        }

    @staticmethod
    def _is_valid_operand(other):
        return hasattr(other, "id") and \
            hasattr(other, "variable_name") and \
            hasattr(other, "variable_items") and \
            hasattr(other, "variable_type") and \
            hasattr(other, "owner") and \
            hasattr(other, "created") and \
            hasattr(other, "updated")

    def __eq__(self, other):
        if not self._is_valid_operand(other):
            return NotImplemented

        return ((self.id,
                 self.variable_name,
                 self.variable_items,
                 self.variable_type,
                 self.owner,
                 self.created,
                 self.updated) == (
            other.id,
            other.variable_name,
            other.variable_items,
            other.variable_type,
            other.owner,
            other.created,
            other.updated
                ))

    def __repr__(self):
        return str({
            "id": self.id,
            "variable_name": self.variable_name,
            "variable_items": self.variable_items,
            "variable_type": self.variable_type,
            "owner": repr(self.owner),
            "created": self.created,
            "updated": self.updated
        })


class IndividualPiece:
    def __init__(self, record) -> None:
        self.response_object = record
        self.id = record.id
        self.piece_text = record.piece_text
        self.section = None
        self.created = record.created
        self.updated = record.updated
        self.expand = {}
        self.variables: dict[str, list[str]] = {}

        try:
            if "section" in record.expand.keys():
                self.section = TemplateSection(record.expand["section"])
                self.expand["section"] = record.expand["section"]
            else:
                self.section = record.section
        except AttributeError:
            self.section = record.section

    def copy(self):
        return IndividualPiece(self)

    def data_to_create(self) -> dict:
        return {
            "piece_text": self.piece_text,
            "section": self.section if isinstance(self.section, str) else self.section.id
        }

    def find_tags_in_piece(self, textbox: ctk.CTkTextbox, user_variables: dict[str, UserVariable]):
        self.variables = utils.find_tags_in_text(self.piece_text, textbox, user_variables)

    @staticmethod
    def _is_valid_operand(other):
        return hasattr(other, "piece_text") and \
               hasattr(other, "section") and \
               hasattr(other, "created") and \
               hasattr(other, "updated") and \
               hasattr(other, "id")

    def __eq__(self, other):
        if not self._is_valid_operand(other):
            return NotImplemented

        return ((self.id,
                 self.piece_text,
                 self.section,
                 self.created,
                 self.updated) == (
            other.id,
            other.piece_text,
            other.section,
            other.created,
            other.updated
        ))

    def __repr__(self):
        return str({
            "id": self.id,
            "piece_text": self.piece_text,
            "section": repr(self.section),
            "created": self.created,
            "updated": self.updated
        })


class TemplateShared:
    def __init__(self, record):
        self.record_object = record
        self.id = record.id
        self.template = None
        self.shared_with = None
        self.created = record.created
        self.updated = record.updated
        self.expand = {}

        try:
            if "template" in record.expand.keys():
                self.template = ReportTemplate(record.expand["template"])
                self.expand["template"] = record.expand["template"]
            else:
                self.template = record.template
        except AttributeError:
            self.template = record.template

        try:
            if "shared_with" in record.expand.keys():
                self.shared_with = User(record.expand["shared_with"])
                self.expand["shared_with"] = record.expand["shared_with"]
            else:
                self.shared_with = record.shared_with
        except AttributeError:
            self.shared_with = record.shared_with

    def copy(self):
        return TemplateShared(self)

    def data_to_create(self) -> dict:
        return {
            "template": self.template.id if self.template is not None else None,
            "shared_with": self.shared_with.id if self.shared_with is not None else None
        }

    @staticmethod
    def _is_valid_operand(other):
        return hasattr(other, "id") and \
               hasattr(other, "template") and \
               hasattr(other, "shared_with") and \
               hasattr(other, "created") and \
               hasattr(other, "updated")

    def __eq__(self, other):
        if not self._is_valid_operand(other):
            return NotImplemented

        return ((self.id,
                 self.template,
                 self.shared_with,
                 self.created,
                 self.updated) == (
            other.id,
            other.template,
            other.shared_with,
            other.created,
            other.updated
        ))

    def __repr__(self):
        return str({
            "id": self.id,
            "template": repr(self.template),
            "shared_with": repr(self.shared_with),
            "created": self.created,
            "updated": self.updated
        })
