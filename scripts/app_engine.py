from typing import Type, Literal
from .database import ReportWriterInstance
import CTkMessagebox as ctkmb
from .containers import *


def create_copy_of_collection(collection: dict[str, ReportTemplate | TemplateSection | IndividualReport |
                                               IndividualPiece | SingleReportSet]) -> \
        dict[str, ReportTemplate | TemplateSection | IndividualReport | IndividualPiece | SingleReportSet]:
    new_dict = {}
    for key, value in collection.items():
        new_dict[key] = value.copy()

    return new_dict


class AppEngine:
    """
    The engine that runs all the data handling within the app. The UI contains a single instance of the app engine, and
    refreshes to reflect changes in the app engine. The UIs interactive widgets will call a specific method in the app
    engine.
    """
    def __init__(self, db_instance: ReportWriterInstance):
        self.db_instance = db_instance
        self.template_collection: dict[str, ReportTemplate] = {}
        self.section_collection: dict[str, TemplateSection] = {}
        self.piece_collection: dict[str, IndividualPiece] = {}
        self.reports_set_collection: dict[str, SingleReportSet] = {}
        self.individual_report_collection: dict[str, IndividualReport] = {}

        self.copy_of_template_collection: dict[str, ReportTemplate] = {}
        self.copy_of_section_collection: dict[str, TemplateSection] = {}
        self.copy_of_piece_collection: dict[str, IndividualPiece] = {}
        self.copy_of_reports_set_collection: dict[str, SingleReportSet] = {}
        self.copy_of_individual_report_collection: dict[str, IndividualReport] = {}

        self.user_container = User(self.db_instance.user_model)

        self.load_success = False

        self.load_data()

    def get_user_id(self) -> str:
        return self.db_instance.get_users_id()[1]

    def load_data(self) -> None:
        """A public method that will force the app engine to load data from the database in order to refresh local data.
        Will overwrite any local changes, so a save check should be made if any changes have been made"""

        # Refresh users authorisation token to ensure the db connection is still valid
        self.db_instance.refresh_auth()

        # Set all collection dictionaries to be emtpy
        self.template_collection: dict[str, ReportTemplate] = {}
        self.section_collection: dict[str, TemplateSection] = {}
        self.piece_collection: dict[str, IndividualPiece] = {}
        self.reports_set_collection: dict[str, SingleReportSet] = {}
        self.individual_report_collection: dict[str, IndividualReport] = {}

        self.copy_of_template_collection: dict[str, ReportTemplate] = {}
        self.copy_of_section_collection: dict[str, TemplateSection] = {}
        self.copy_of_piece_collection: dict[str, IndividualPiece] = {}
        self.copy_of_reports_set_collection: dict[str, SingleReportSet] = {}
        self.copy_of_individual_report_collection: dict[str, IndividualReport] = {}

        # Create load_values dictionary for all data to be collected. Load values includes the database collection as
        #  the key linked to a tuple that contains the dictionary to populate, and the data container to wrap around
        #  the records returned for that collection
        load_values: dict[str, tuple[dict, Type[ReportTemplate | TemplateSection | IndividualPiece | IndividualReport
                                                | SingleReportSet]]] = {
            "templates": (self.template_collection, ReportTemplate),
            "template_sections": (self.section_collection, TemplateSection),
            "report_pieces": (self.piece_collection, IndividualPiece),
            "report_set": (self.reports_set_collection, SingleReportSet),
            "individual_reports": (self.individual_report_collection, IndividualReport)
        }

        for collection_name, dict_and_class in load_values.items():
            # Call a list collection with the database, using the current key (collection_name)
            if collection_name != "templates":
                response, results = self.db_instance.get_full_list_from_collection(collection_name, {
                    "sort": "-created"
                })
            else:
                response, results = self.db_instance.get_full_list_from_collection(collection_name, {
                    "sort": "-created",
                    "expand": "owner"
                })

            if results is None:
                # If the returned results is None, the collection attempt failed. Throw up an error message and escape
                #  the load_data method.
                self.run_load_error(response["message"])
                return
            else:
                # If results are returned, use the given container class to generate an object with each returned record
                for record in results:
                    dict_and_class[0][record.id] = dict_and_class[1](record)

        self.copy_of_template_collection: dict[str, ReportTemplate] = \
            create_copy_of_collection(self.template_collection)

        self.copy_of_section_collection: dict[str, TemplateSection] = create_copy_of_collection(self.section_collection)

        self.copy_of_piece_collection: dict[str, IndividualPiece] = create_copy_of_collection(self.piece_collection)

        self.copy_of_reports_set_collection: dict[str, SingleReportSet] = \
            create_copy_of_collection(self.reports_set_collection)

        self.copy_of_individual_report_collection: dict[str, IndividualReport] = \
            create_copy_of_collection(self.individual_report_collection)

    def create_piece_to_template(self, template_id: str) -> dict[str, dict[str, IndividualPiece]]:
        """Create template and piece relationship"""

        new_relationship: dict[str, dict[str, IndividualPiece]] = {}

        for section in self.copy_of_section_collection.values():
            if section.template == template_id:
                new_relationship[section.id] = {}

        for piece in self.copy_of_piece_collection.values():
            if self.copy_of_section_collection[piece.section].template == template_id:
                # Create a new key, value pair using the piece's id and the piece itself, place that inside the relevant
                #  section key, which is then inside the relevant template key.
                new_relationship[piece.section][piece.id] = piece

        return new_relationship

    def create_report_to_report_set(self) -> None:
        """Create report to reports set relationship"""
        pass
        # for report in self.copy_of_individual_report_collection.values():
        #     # If the current report's report set doesn't exist in the dictionary, create the key with the report set ID
        #     #  and initialise with an empty dictionary
        #     if report.report_set not in self.reports_to_set_reports_collection.keys():
        #         self.reports_to_set_reports_collection[report.report_set] = []
        #
        #     # Create a new key, value pair with the report's id and the report itself, place that inside the relevant
        #     #  report set dictionary
        #     self.reports_to_set_reports_collection[report.report_set].append(report.id)

    def create_new_record_id(self, collection: Literal["templates",
                                                       "report_set",
                                                       "template_sections",
                                                       "individual_reports",
                                                       "report_pieces"]) -> int:
        collections = {
            "templates": self.copy_of_template_collection,
            "template_sections": self.copy_of_section_collection,
            "report_set": self.copy_of_reports_set_collection,
            "individual_reports": self.copy_of_individual_report_collection,
            "report_pieces": self.copy_of_piece_collection
        }

        current_ids: list[str] = list(collections[collection].keys())

        max_blank_id = 0
        for i in current_ids:
            if "@" in i:
                if int(i[1::]) >= max_blank_id:
                    max_blank_id = int(i[1::]) + 1

        return max_blank_id

    def run_load_error(self, message: str) -> None:

        error_box = ctkmb.CTkMessagebox(
            title="Error",
            message=f"{message} - Please try again later",
            icon="cancel")
        error_box.wait_window()
        self.load_success = False
