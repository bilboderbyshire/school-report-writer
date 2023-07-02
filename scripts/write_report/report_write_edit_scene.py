import customtkinter as ctk
from ..settings import *
from ..app_engine import AppEngine
from ..containers import ReportTemplate, IndividualPiece, TemplateSection, UserVariable, IndividualReport, \
    SingleReportSet
from ..title_bar import TitleBar
from ..components import Separator, LargeOptionMenu, NormalLabel, HoverTooltip
from .report_piece_scrollframe import ReportPieceScrollframe
from .report_text_frame import ReportTextFrame
from .insert_variables_frame import InsertVariablesFrame
from typing import TYPE_CHECKING
import CTkMessagebox as ctkmb
from PIL import Image
from ..report_setup_toplevel import AddOneToplevel, ReportSetupToplevel
from .select_pupil_toplevel import SelectPupilToplevel
import os

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
        self.report_set: SingleReportSet | None = None
        self.structured_pieces: dict[str, dict[str, IndividualPiece]] | None = None
        self.all_reports: list[IndividualReport] | None = None

        self.current_report: IndividualReport | None = None
        self.current_report_index = 0
        self.prev_report_index = None
        self.next_report_index = 1
        self.next_pupil_sv = ctk.StringVar()
        self.prev_pupil_sv = ctk.StringVar()

        self.pupil_name_sv = ctk.StringVar()
        self.pupil_gender_sv = ctk.StringVar()

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
        name_and_actions.columnconfigure([0, 1, 3], weight=0)
        name_and_actions.columnconfigure(2, weight=1)

        edit_pupil_image = ctk.CTkImage(
            light_image=Image.open(os.path.join(os.getcwd(), "images/light-pencil.png")),
            dark_image=Image.open(os.path.join(os.getcwd(), "images/dark-pencil.png")),
            size=(25, 25)
        )
        edit_pupil_button = ctk.CTkButton(
            name_and_actions,
            fg_color="transparent",
            image=edit_pupil_image,
            command=self.edit_current_pupil_info,
            text="",
            width=35,
            height=35,
            hover_color=BUTTON_HOVER_COLOR,
            corner_radius=5
        )

        edit_pupil_button.grid(row=0, column=0, sticky="e", padx=(0, SMALL_PAD))

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
        self.pupil_gender_label.grid(row=0, column=1, sticky="nsew")

        self.pupil_name_label = ctk.CTkLabel(
            name_and_actions,
            textvariable=self.pupil_name_sv,
            fg_color="transparent",
            font=ctk.CTkFont(**SECONDARY_TITLE_FONT),
            anchor="w"
        )
        self.pupil_name_label.grid(row=0, column=2, sticky="nsew", padx=(DEFAULT_PAD, 0))

        pupil_button_frame = ctk.CTkFrame(name_and_actions, fg_color="transparent")
        pupil_button_frame.grid(row=0, column=3, sticky="nsew", pady=2)
        pupil_button_frame.rowconfigure(0, weight=1)
        pupil_button_frame.columnconfigure([0, 1, 2, 3], weight=0)

        save_pupil_image = ctk.CTkImage(
            light_image=Image.open(os.path.join(os.getcwd(), "images/light-save.png")),
            dark_image=Image.open(os.path.join(os.getcwd(), "images/dark-save.png")),
            size=(25, 25)
        )

        save_pupil_button = ctk.CTkButton(
            pupil_button_frame,
            fg_color="transparent",
            image=save_pupil_image,
            command=self.save_clicked,
            text="",
            width=35,
            height=35,
            hover_color=BUTTON_HOVER_COLOR,
            corner_radius=5
        )

        save_pupil_button.grid(row=0, column=0, sticky="e", padx=(0, SMALL_PAD))
        HoverTooltip(save_pupil_button, text="Save report")

        prev_pupil_image = ctk.CTkImage(
            light_image=Image.open(os.path.join(os.getcwd(), "images/light-left-arrow.png")),
            dark_image=Image.open(os.path.join(os.getcwd(), "images/dark-left-arrow.png")),
            size=(25, 25)
        )
        self.previous_pupil_button = ctk.CTkButton(
            pupil_button_frame,
            fg_color="transparent",
            image=prev_pupil_image,
            command=self.prev_pupil_clicked,
            text="",
            width=35,
            height=35,
            hover_color=BUTTON_HOVER_COLOR,
            corner_radius=5
        )

        self.previous_pupil_button.grid(row=0, column=1, sticky="e", padx=(0, SMALL_PAD))
        HoverTooltip(self.previous_pupil_button, text_variable=self.prev_pupil_sv)

        next_pupil_image = ctk.CTkImage(
            light_image=Image.open(os.path.join(os.getcwd(), "images/light-right-arrow.png")),
            dark_image=Image.open(os.path.join(os.getcwd(), "images/dark-right-arrow.png")),
            size=(25, 25)
        )
        self.next_pupil_button = ctk.CTkButton(
            pupil_button_frame,
            fg_color="transparent",
            image=next_pupil_image,
            command=self.next_pupil_clicked,
            text="",
            width=35,
            height=35,
            hover_color=BUTTON_HOVER_COLOR,
            corner_radius=5
        )

        self.next_pupil_button.grid(row=0, column=2, sticky="e", padx=(0, SMALL_PAD))
        HoverTooltip(self.next_pupil_button, text_variable=self.next_pupil_sv)

        self.report_options_menu = LargeOptionMenu(
            pupil_button_frame,
            fg_color=ROOT_BG,
            height=35,
            values=["Select pupil", "Report settings", "Export", "Delete set"],
            command=self.report_option_selected
        )
        self.report_options_menu.set("Options")

        self.report_options_menu.grid(row=0, column=3, sticky="e", padx=(0, SMALL_PAD))
        HoverTooltip(self.report_options_menu, text="Options")

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
                                                 variables_collection=self.app_engine.user_variables_collection,
                                                 text_box_edited_command=self.text_box_edited)
        self.report_text_frame.grid(row=1, column=1, sticky="nsew", padx=(0, DEFAULT_PAD), pady=(0, DEFAULT_PAD))

        self.insert_variables_frame = InsertVariablesFrame(
            report_and_variables_frame,
            variables_collection=self.app_engine.user_variables_collection,
            edit_static_command=self.edit_static_variable,
            edit_choice_command=self.edit_choice_variable,
            edit_chain_command=self.edit_chain_variable
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

        starting_report = None
        for report in self.all_reports:
            if not report.completed:
                starting_report = report
                break

        self.refresh_current_report(starting_report)

    def setup_scene(self, report_set: SingleReportSet):
        self.report_set = report_set
        unsorted_reports = [i for i in self.app_engine.copy_of_individual_report_collection.values()
                            if i.report_set == self.report_set.id]
        self.all_reports = sorted(unsorted_reports, key=lambda x: x.pupil_surname)

        self.report_template = self.app_engine.template_collection[report_set.template]
        self.report_sections = [i for i in self.app_engine.section_collection.values()
                                if i.template == self.report_template.id]
        self.structured_pieces = self.app_engine.create_piece_to_template(self.report_template.id, copy=False)

    def refresh_current_report(self, new_report: IndividualReport):
        self.current_report = new_report
        self.pupil_name_sv.set((new_report.pupil_forename.capitalize() + " " + new_report.pupil_surname.capitalize()))
        self.pupil_gender_sv.set(new_report.gender.upper())

        self.report_text_frame.change_report(self.current_report)
        self.insert_variables_frame.clear_all_frames()

        self.current_report_index = self.all_reports.index(self.current_report)

        self.prev_report_index = self.current_report_index - 1 if self.current_report_index > 0 else None
        self.next_report_index = self.current_report_index + 1 if self.current_report_index < len(
            self.all_reports) - 1 else None

        if self.prev_report_index is not None:
            self.previous_pupil_button.configure(state="normal")
            self.prev_pupil_sv.set(f"{self.all_reports[self.prev_report_index].pupil_forename.capitalize()} " +
                                   f"{self.all_reports[self.prev_report_index].pupil_surname.capitalize()}")
        else:
            self.prev_pupil_sv.set("None")
            self.previous_pupil_button.configure(state="disabled")

        if self.next_report_index is not None:
            self.next_pupil_button.configure(state="normal")
            self.next_pupil_sv.set(f"{self.all_reports[self.next_report_index].pupil_forename.capitalize()} " +
                                   f"{self.all_reports[self.next_report_index].pupil_surname.capitalize()}")
        else:
            self.next_pupil_sv.set("None")
            self.next_pupil_button.configure(state="disabled")

    def next_pupil_clicked(self):
        if not self.check_for_save():
            return
        self.save_report()
        self.refresh_current_report(self.all_reports[self.next_report_index])

    def prev_pupil_clicked(self):
        if not self.check_for_save():
            return
        self.save_report()
        self.refresh_current_report(self.all_reports[self.prev_report_index])

    def save_clicked(self):
        if not self.check_for_save():
            return
        self.save_report()

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

    def edit_choice_variable(self, chosen_value: str, variable: UserVariable, index: int):
        self.report_text_frame.edit_variable(
            variable_type="choice",
            variable_name=variable.variable_name,
            new_text=chosen_value,
            index=index
        )

    def edit_chain_variable(self, new_text: str, variable: UserVariable, index: int):
        self.report_text_frame.edit_variable(
            variable_type="chain",
            variable_name=variable.variable_name,
            new_text=new_text,
            index=index
        )

    def edit_current_pupil_info(self):
        add_one_tl = AddOneToplevel(
            self,
            self.current_report.get_pupil_info()
        )

        new_pupil_info = add_one_tl.get_pupil_info()
        if new_pupil_info is None or new_pupil_info == self.current_report.get_pupil_info():
            return

        self.current_report.pupil_forename = new_pupil_info["forename"].lower()
        self.current_report.pupil_surname = new_pupil_info["surname"].lower()
        self.current_report.gender = new_pupil_info["gender"].lower()

        self.refresh_current_report(self.current_report)


    def check_for_save(self) -> bool:
        all_tags_filled = True
        for tag in self.report_text_frame.piece_textbox.tag_names():
            tag_ranges = self.report_text_frame.piece_textbox.tag_ranges(tag)

            for start, end in zip(tag_ranges[0::2], tag_ranges[1::2]):
                current_tag = self.report_text_frame.piece_textbox.get(start, end)
                if "{" in current_tag or "}" in current_tag:
                    all_tags_filled = False

        if not all_tags_filled:
            warning_box = ctkmb.CTkMessagebox(
                title="Warning",
                message=f"You haven't filled in all the variables for this report. Are you sure you want to move on?"
                        f"\n\nYou will not be able to fill them in the future.",
                icon="cancel",
                option_1="No",
                option_2="Yes")
            warning_box.wait_window()

            if warning_box.get() == "Yes":
                return True
            else:
                return False
        else:
            return True

    def save_report(self):
        self.current_report.report_text = self.report_text_frame.piece_textbox.get("1.0", "end").strip()

        if self.current_report == self.app_engine.individual_report_collection[self.current_report.id]:
            return

        updated_report = self.app_engine.update_record(
            record_id=self.current_report.id,
            data=self.current_report.data_to_create(),
            collection="individual_reports",
            container_type=IndividualReport
        )

        if updated_report is None:
            return

        self.current_report = updated_report
        self.all_reports[self.current_report_index] = updated_report
        self.app_engine.copy_of_individual_report_collection[self.current_report.id] = updated_report
        self.app_engine.individual_report_collection[self.current_report.id] = updated_report.copy()

        self.report_text_frame.change_report(self.current_report)
        self.insert_variables_frame.clear_all_frames()

    def text_box_edited(self, new_variables: dict[str, list[str]]):
        for var_type, var_info_list in new_variables.items():
            if var_type == "static":
                current_static_vars = list(self.insert_variables_frame.static_vars.instance_dict.keys())

                # for new_var in var_info_list:
                #     if new_var not in current_static_vars:
                #         self.insert_variables_frame.static_vars.add_variable(new_var)

                for existing_var in current_static_vars:
                    if existing_var not in var_info_list:
                        self.insert_variables_frame.static_vars.delete_variable(existing_var)
            elif var_type == "choice":
                current_choice_vars = self.insert_variables_frame.choice_vars.get_all_choices()
                current_choice_keys = list(self.insert_variables_frame.choice_vars.instance_dict.keys())

                if not current_choice_keys:
                    continue

                collapsed_index = 0
                for i in var_info_list:
                    while i.lower() != current_choice_vars[collapsed_index].lower():
                        if "{" in i \
                                and var_type in i \
                                and ":" in i \
                                and current_choice_vars[collapsed_index] == "Choose variable":
                            break
                        self.insert_variables_frame.choice_vars.delete_variable(current_choice_keys[collapsed_index])
                        collapsed_index += 1
                    collapsed_index += 1

                current_choice_keys = list(self.insert_variables_frame.choice_vars.instance_dict.keys())
                collapsed_index = len(current_choice_keys) - 1
                while len(var_info_list) < len(current_choice_keys):
                    self.insert_variables_frame.choice_vars.delete_variable(current_choice_keys[collapsed_index])
                    current_choice_keys = list(self.insert_variables_frame.choice_vars.instance_dict.keys())
                    collapsed_index = len(current_choice_keys) - 1

                self.insert_variables_frame.choice_vars.reorganize_instance_dict()
            else:
                current_chain_vars = self.insert_variables_frame.chain_vars.get_all_choices()
                current_chain_keys = list(self.insert_variables_frame.chain_vars.instance_dict.keys())

                if not current_chain_keys:
                    continue

                collapsed_index = 0
                for i in var_info_list:
                    while i.lower() != current_chain_vars[collapsed_index].lower():
                        if "{" in i \
                                and var_type in i \
                                and ":" in i \
                                and current_chain_vars[collapsed_index] == "none":
                            break
                        self.insert_variables_frame.chain_vars.delete_variable(current_chain_keys[collapsed_index])
                        collapsed_index += 1
                    collapsed_index += 1

                current_chain_keys = list(self.insert_variables_frame.chain_vars.instance_dict.keys())
                collapsed_index = len(current_chain_keys) - 1
                while len(var_info_list) < len(current_chain_keys):
                    self.insert_variables_frame.chain_vars.delete_variable(current_chain_keys[collapsed_index])
                    current_chain_keys = list(self.insert_variables_frame.chain_vars.instance_dict.keys())
                    collapsed_index = len(current_chain_keys) - 1

                self.insert_variables_frame.chain_vars.reorganize_instance_dict()

    def report_option_selected(self, value_selected: str):
        self.report_options_menu.set("Options")

        if value_selected == "Report settings":
            settings_tl = ReportSetupToplevel(
                self,
                self.app_engine,
                self.report_set
            )

            new_report_set = settings_tl.get_report()

            if new_report_set is None:
                return

            self.setup_scene(new_report_set)

            try:
                self.refresh_current_report(self.current_report)
            except ValueError:
                starting_report = None
                for report in self.all_reports:
                    if not report.completed:
                        starting_report = report
                        break

                self.refresh_current_report(starting_report)

        elif value_selected == "Select pupil":
            select_pupil_tl = SelectPupilToplevel(self, self.all_reports)
            selected_pupil = select_pupil_tl.get_selected_pupil()

            if selected_pupil is None:
                return

            self.refresh_current_report(selected_pupil)
        else:
            print(f"{value_selected} was selected, but there's not code for it yet LMAO")