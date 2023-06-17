from typing import Type
from .database import ReportWriterInstance
import CTkMessagebox as ctkmb
from .containers import *


class AppEngine:
    """
    The engine that runs all the data handling within the app. The UI contains a single instance of the app engine, and
    refreshes to reflect changes in the app engine. The UIs interactive widgets will call a specific method in the app
    engine.
    """
    def __init__(self, db_instance: ReportWriterInstance):
        self.db_instance = db_instance
        self.template_collection: dict[str, ReportTemplate] = {}
        self.piece_collection: dict[str, IndividualPiece] = {}
        self.reports_set_collection: dict[str, SingleReportSet] = {}
        self.individual_report_collection: dict[str, IndividualReport] = {}

        self.piece_to_template_collection: dict[str, dict[int, list[str]]] = {}
        self.reports_to_set_reports_collection: dict[str, list[str]] = {}
        self.load_success = False

        self.load_data()
        self.__create_report_to_report_set()
        self.__create_piece_to_template()

        print(self.reports_to_set_reports_collection)
        print(self.piece_to_template_collection)

    def load_data(self) -> None:
        """A public method that will force the app engine to load data from the database in order to refresh local data.
        Will overwrite any local changes, so a save check should be made if any changes have been made"""

        # Refresh users authorisation token to ensure the db connection is still valid
        self.db_instance.refresh_auth()

        # Set all collection dictionaries to be emtpy
        self.template_collection: dict[str, ReportTemplate] = {}
        self.piece_collection: dict[str, IndividualPiece] = {}
        self.reports_set_collection: dict[str, SingleReportSet] = {}
        self.individual_report_collection: dict[str, IndividualReport] = {}

        # Create load_values dictionary for all data to be collected. Load values includes the database collection as
        #  the key linked to a tuple that contains the dictionary to populate, and the data container to wrap around
        #  the records returned for that collection
        load_values: dict[str, tuple[dict, Type[ReportTemplate | IndividualPiece | IndividualReport | SingleReportSet]]] = {
            "templates": (self.template_collection, ReportTemplate),
            "report_pieces": (self.piece_collection, IndividualPiece),
            "report_set": (self.reports_set_collection, SingleReportSet),
            "individual_reports": (self.individual_report_collection, IndividualReport)
        }

        for collection_name, dict_and_class in load_values.items():
            # Call a list collection with the database, using the current key (collection_name)
            response, results = self.db_instance.get_full_list_from_collection(collection_name, {
                "sort": "-created"
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

    def __create_piece_to_template(self) -> None:
        """Create template and piece relationship"""

        for piece in self.piece_collection.values():
            if piece.template not in self.piece_to_template_collection.keys():
                # If the current piece's template doesn't exist in the dictionary, create the key with the template ID
                #  and initialise with an empty dictionary
                self.piece_to_template_collection[piece.template] = {}

            if piece.section not in self.piece_to_template_collection[piece.template].keys():
                # If the section doesn't exist within the templates dictionary, create a key using the section and
                #  initialise with an empty dictionary
                self.piece_to_template_collection[piece.template][piece.section] = []

            # Create a new key, value pair using the piece's id and the piece itself, place that inside the relevant
            #  section key, which is then inside the relevant template key.
            self.piece_to_template_collection[piece.template][piece.section].append(piece.id)

    def __create_report_to_report_set(self) -> None:
        """Create report to reports set relationship"""

        for report in self.individual_report_collection.values():
            # If the current report's report set doesn't exist in the dictionary, create the key with the report set ID
            #  and initialise with an empty dictionary
            if report.report_set not in self.reports_to_set_reports_collection.keys():
                self.reports_to_set_reports_collection[report.report_set] = []

            # Create a new key, value pair with the report's id and the report itself, place that inside the relevant
            #  report set dictionary
            self.reports_to_set_reports_collection[report.report_set].append(report.id)

    def run_load_error(self, message: str) -> None:

        error_box = ctkmb.CTkMessagebox(
            title="Error",
            message=f"{message} - Please try again later",
            icon="cancel")
        error_box.wait_window()
        self.load_success = False
