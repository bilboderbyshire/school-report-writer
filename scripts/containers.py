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