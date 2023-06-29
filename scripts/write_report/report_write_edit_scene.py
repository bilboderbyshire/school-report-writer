import customtkinter as ctk
from ..settings import *
from ..app_engine import AppEngine
from ..containers import ReportTemplate, IndividualPiece, TemplateSection, PupilInfo
from ..title_bar import TitleBar
from ..components import Separator, SecondaryButton, LargeOptionMenu, NormalLabel, HoverTooltip
from .report_piece_scrollframe import ReportPieceScrollframe
from .report_text_frame import ReportTextFrame
from .insert_variables_frame import InsertVariablesFrame
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..root import ReportWriter


class ReportScene(ctk.CTkFrame):
    def __init__(self,
                 master,
                 app_engine: AppEngine):
        super().__init__(master, fg_color=ROOT_BG)

        self.app_engine = app_engine
        self.prev_scene_string = None
        self.report_sections: list[TemplateSection] | None = None
        self.report_template: ReportTemplate | None = None
        self.structured_pieces: dict[str, dict[str, IndividualPiece]] | None = None

        self.pupil_name_sv = ctk.StringVar(value="Sally")
        self.pupil_gender_sv = ctk.StringVar(value="NB")
        self.next_pupil_sv = ctk.StringVar(value="Barry")
        self.prev_pupil_sv = ctk.StringVar(value="Mary")

        self.pupil_info: PupilInfo = {"forename": "Sally",
                                      "surname": "Hawkins",
                                      "gender": "NB"}

    def __build_frame(self):

        title_bar = TitleBar(self, "Write Report",
                             back_command=self.go_back)
        title_bar.grid(row=0, column=0, columnspan=2, sticky="nsew", pady=(DEFAULT_PAD, 0), padx=DEFAULT_PAD)

        title_sep = Separator(self, "hor")
        title_sep.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=DEFAULT_PAD * 3, pady=DEFAULT_PAD)

        name_and_actions = ctk.CTkFrame(self, fg_color="transparent")
        name_and_actions.grid(
            row=2,
            column=0,
            columnspan=2,
            sticky="nsew",
            padx=DEFAULT_PAD,
            pady=(0, DEFAULT_PAD))

        name_and_actions.rowconfigure(0, weight=0)
        name_and_actions.columnconfigure([0, 2], weight=0)
        name_and_actions.columnconfigure(1, weight=1)

        self.pupil_gender_label = ctk.CTkLabel(
            name_and_actions,
            textvariable=self.pupil_gender_sv,
            fg_color=LABEL_CARD_COLOR,
            font=ctk.CTkFont(**SECONDARY_TITLE_FONT),
            anchor="center",
            corner_radius=8,
            padx=5,
            pady=3
        )
        self.pupil_gender_label.grid(row=0, column=0, sticky="nsew")

        self.pupil_name_label = ctk.CTkLabel(
            name_and_actions,
            textvariable=self.pupil_name_sv,
            fg_color="transparent",
            font=ctk.CTkFont(**SECONDARY_TITLE_FONT),
            anchor="w"
        )
        self.pupil_name_label.grid(row=0, column=1, sticky="nsew", padx=(DEFAULT_PAD, 0))

        pupil_button_frame = ctk.CTkFrame(name_and_actions, fg_color="transparent")
        pupil_button_frame.grid(row=0, column=2, sticky="nsew", pady=2)
        pupil_button_frame.rowconfigure(0, weight=1)
        pupil_button_frame.columnconfigure([0, 1, 2, 3], weight=0, uniform="columns")

        show_pupils_button = SecondaryButton(
            pupil_button_frame,
            text="Pupils...",
            font=ctk.CTkFont(**NORMAL_LABEL_FONT),
            width=80
        )
        show_pupils_button.grid(row=0, column=0, sticky="nsew", padx=(0, SMALL_PAD))

        previous_pupil_button = SecondaryButton(
            pupil_button_frame,
            text="Prev",
            font=ctk.CTkFont(**NORMAL_LABEL_FONT),
            width=0,
        )
        previous_pupil_button.grid(row=0, column=1, sticky="nsew", padx=(0, SMALL_PAD))

        save_pupil_button = ctk.CTkButton(
            pupil_button_frame,
            text="Save",
            font=ctk.CTkFont(**NORMAL_LABEL_FONT),
            width=0,
        )
        save_pupil_button.grid(row=0, column=2, sticky="nsew", padx=(0, SMALL_PAD))

        next_pupil_button = SecondaryButton(
            pupil_button_frame,
            text="Next",
            font=ctk.CTkFont(**NORMAL_LABEL_FONT),
            width=0,
        )
        next_pupil_button.grid(row=0, column=3, sticky="nsew")
        HoverTooltip(next_pupil_button, text_variable=self.next_pupil_sv)

        section_piece_frame = ctk.CTkFrame(self)
        section_piece_frame.grid(row=3, column=0, sticky="nsew", padx=DEFAULT_PAD, pady=(0, DEFAULT_PAD))
        section_piece_frame.rowconfigure(0, weight=0)
        section_piece_frame.rowconfigure(1, weight=1)
        section_piece_frame.columnconfigure(0, weight=1)

        section_menu = LargeOptionMenu(
            section_piece_frame,
            height=40,
            values=[i.section_title.capitalize() for i in self.report_sections],
            command=self.section_selected
        )
        section_menu.grid(row=0, column=0, sticky="w", padx=DEFAULT_PAD, pady=(DEFAULT_PAD, SMALL_PAD))

        self.piece_scrollframe = ReportPieceScrollframe(section_piece_frame, insert_piece_command=self.insert_piece)
        self.piece_scrollframe.grid(row=1, column=0, sticky="nsew", padx=(3, SMALL_PAD))

        report_and_variables_frame = ctk.CTkFrame(self)
        report_and_variables_frame.grid(row=3, column=1, sticky="nsew", padx=(0, DEFAULT_PAD), pady=(0, DEFAULT_PAD))
        report_and_variables_frame.rowconfigure(0, weight=0)
        report_and_variables_frame.rowconfigure(1, weight=1)
        report_and_variables_frame.columnconfigure(0, weight=2, uniform="columns")
        report_and_variables_frame.columnconfigure(1, weight=3, uniform="columns")

        variables_frame_title = NormalLabel(
                report_and_variables_frame,
                anchor="w",
                text="Variables")

        variables_frame_title.grid(row=0, column=0, sticky="nw", padx=15, pady=15)

        report_frame_title = NormalLabel(
            report_and_variables_frame,
            anchor="w",
            text="Report")

        report_frame_title.grid(row=0, column=1, sticky="nw", padx=15, pady=15)

        self.report_text_frame = ReportTextFrame(report_and_variables_frame,
                                                 pupil_info=self.pupil_info,
                                                 variables_collection=self.app_engine.user_variables_collection,
                                                 text_box_edited_command=self.text_box_edited)
        self.report_text_frame.grid(row=1, column=1, sticky="nsew", padx=(0, DEFAULT_PAD), pady=(0, DEFAULT_PAD))

        self.insert_variables_frame = InsertVariablesFrame(
            report_and_variables_frame,
            variables_collection=self.app_engine.user_variables_collection,
            edit_static_command=self.edit_static_variable
        )
        self.insert_variables_frame.grid(row=1, column=0, sticky="nsew", padx=(3, SMALL_PAD), pady=(0, DEFAULT_PAD))

        self.rowconfigure([0, 1, 2], weight=0)
        self.rowconfigure(3, weight=1)
        self.columnconfigure(0, weight=2)
        self.columnconfigure(1, weight=5)

        self.after(10, self.check_all_scrollbars)

    def fill_frames(self):
        for i in self.winfo_children():
            i.destroy()

        self.__build_frame()

        if self.report_sections is not None and self.report_sections:
            self.piece_scrollframe.build_pieces_frame(self.structured_pieces[self.report_sections[0].id])

    def setup_scene(self, template: ReportTemplate):
        self.report_template = template
        self.report_sections = [i for i in self.app_engine.section_collection.values()
                                if i.template == self.report_template.id]
        self.structured_pieces = self.app_engine.create_piece_to_template(self.report_template.id, copy=False)

    def previous_scene(self, name_of_prev_frame: str):
        self.prev_scene_string = name_of_prev_frame

    def go_back(self):
        self.master: ReportWriter
        new_scene = self.master.get_frame(self.prev_scene_string)
        new_scene.fill_frames()
        self.after(10, self.master.show_frame, self.prev_scene_string)
        self.prev_scene_string = None

    def check_all_scrollbars(self):
        self.piece_scrollframe.check_scrollbar_needed()

    def section_selected(self, option: str):
        id_of_section = ""
        for section in self.report_sections:
            if section.section_title.lower() == option.lower():
                id_of_section = section.id
                break

        self.piece_scrollframe.build_pieces_frame(self.structured_pieces[id_of_section])

    def insert_piece(self, piece: IndividualPiece):
        new_variables = self.report_text_frame.insert_piece(piece)

        self.insert_variables_frame.build_variable_inserts(new_variables)

    def edit_static_variable(self, variable_name: str, new_text: str):
        self.report_text_frame.edit_static_variable(
            variable_name=variable_name,
            new_text=new_text
        )

    def text_box_edited(self, new_variables: dict[str, list[str]]):
        for var_type, var_info_list in new_variables.items():
            if var_type == "static":
                current_static_vars = list(self.insert_variables_frame.static_vars.instance_dict.keys())

                print(var_info_list)
                print(current_static_vars)

                for new_var in var_info_list:
                    if new_var not in current_static_vars:
                        self.insert_variables_frame.static_vars.add_variable(new_var)

                for existing_var in current_static_vars:
                    if existing_var not in var_info_list:
                        self.insert_variables_frame.static_vars.delete_variable(existing_var)
