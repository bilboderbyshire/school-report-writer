from .database import ReportWriterInstance
import CTkMessagebox as ctkmb
from .containers import *


class AppEngine:
    def __init__(self, db_instance: ReportWriterInstance):
        self.db_instance = db_instance
        self.template_collection: dict[str, ReportTemplate] = {}
        self.piece_collection: dict[str, IndividualPiece] = {}
        self.piece_to_template_collection: dict[str, dict[int, dict[str, IndividualPiece]]] = {}
        self.load_success = False

        self.load_data()
        print(self.piece_to_template_collection)

    def load_data(self):
        # Load templates
        templates_response, templates_results = self.db_instance.get_full_list_from_collection("templates", {
            "expand": "owner",
            "sort": "-created"
        })
        if templates_results is None:
            self.run_load_error(templates_response["message"])
            self.template_collection = {}
            return
        else:
            for record in templates_results:
                self.template_collection[record.id] = ReportTemplate(record)

        # Load report pieces
        piece_response, piece_results = self.db_instance.get_full_list_from_collection("report_pieces", {
            "expand": "template",
            "sort": "-created"
        })

        if piece_results is None:
            self.run_load_error(piece_response["message"])
            self.piece_collection = {}
            return
        else:
            for record in piece_results:
                self.piece_collection[record.id] = IndividualPiece(record)

        # Create template and piece relationship
        for piece in self.piece_collection.values():
            if piece.template.id not in self.piece_to_template_collection.keys():
                self.piece_to_template_collection[piece.template.id] = {}

            if piece.section not in self.piece_to_template_collection[piece.template.id]:
                self.piece_to_template_collection[piece.template.id][piece.section] = {}

            self.piece_to_template_collection[piece.template.id][piece.section][piece.id] = piece

    def run_load_error(self, message: str):
        error_box = ctkmb.CTkMessagebox(
            title="Error",
            message=f"{message} - Please try again later",
            icon="cancel")
        error_box.wait_window()
        self.load_success = False