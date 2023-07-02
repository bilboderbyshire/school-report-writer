import customtkinter as ctk
from ..settings import *
from ..title_bar import TitleLabel
from ..components import SingleLineEntry, NormalLabel, SecondaryButton, LargeOptionMenu
from .add_one_top_level import AddOneToplevel
from .add_many_toplevel import AddManyToplevel
from .pupil_scrollframe import PupilScrollframe
from ..containers import SingleReportSet, NewReportSet, NewIndividualReport, IndividualReport
from ..app_engine import AppEngine
import os
from PIL import Image


class ReportSetupToplevel(ctk.CTkToplevel):
    def __init__(self,
                 master,
                 app_engine: AppEngine,
                 report_set: SingleReportSet | None):
        super().__init__(master,
                         fg_color=ROOT_BG)

        self.report_set = report_set
        self.app_engine = app_engine
        self.new_individual_report_tracker = 0

        self.update_idletasks()
        ws = self.winfo_screenwidth()
        hs = self.winfo_screenheight()

        x = int((ws / 2) - (VARIABLE_TOPLEVEL_WIDTH / 2))
        y = int((hs / 2) - (VARIABLE_TOPLEVEL_HEIGHT / 2)) - 100

        self.geometry(f"{VARIABLE_TOPLEVEL_GEOMETRY}+{x}+{y}")

        self.title("Setup report")

        # CTk.Toplevel source code applies default iconbitmap after 200ms (for some reason), this overrides any icon
        #  change made during initialisation of login window. This code overrides their override by rendering my icon
        #  50ms after theirs.
        self.after(250, lambda: self.iconbitmap(os.path.join(os.getcwd(), "images/app-logo.ico")))

        title_bar = TitleLabel(self,
                               "Setup report")
        title_bar.grid(row=0, column=0, sticky="w", pady=(DEFAULT_PAD, 35), padx=DEFAULT_PAD)

        report_name_entry_label = NormalLabel(
            self,
            anchor="sw",
            text="Report name"
        )
        report_name_entry_label.grid(row=1, column=0, sticky="ew", pady=(0, DEFAULT_PAD), padx=DEFAULT_PAD)

        self.report_name_entry = SingleLineEntry(
            self,
            placeholder_text="Eg, Form Report 2023"
        )
        self.report_name_entry.grid(row=2, column=0, sticky="ew", pady=(0, DEFAULT_PAD), padx=DEFAULT_PAD)

        if self.report_set is not None:
            self.report_name_entry.insert(0, self.report_set.report_title.capitalize())

        class_entry_label = NormalLabel(
            self,
            anchor="sw",
            text="Class name"
        )
        class_entry_label.grid(row=3, column=0, sticky="ew", pady=(0, DEFAULT_PAD), padx=DEFAULT_PAD)

        self.class_entry = SingleLineEntry(
            self,
            placeholder_text="Eg, 10x/cs1"
        )
        self.class_entry.grid(row=4, column=0, sticky="ew", pady=(0, DEFAULT_PAD), padx=DEFAULT_PAD)

        if self.report_set is not None:
            self.class_entry.insert(0, self.report_set.class_name.capitalize())

        self.template_selection = LargeOptionMenu(
            self,
            height=40,
            values=[i.template_title.capitalize() for i in self.app_engine.template_collection.values()]
        )
        self.template_selection.grid(row=5, column=0, sticky="ew", pady=(0, DEFAULT_PAD), padx=DEFAULT_PAD)
        if self.report_set is not None:
            self.template_selection.set(
                self.app_engine.template_collection[self.report_set.template].template_title.capitalize()
            )
            self.template_selection.configure(state="disabled")
        else:
            self.template_selection.set("Choose template...")

        pupils_label_and_action_frame = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )
        pupils_label_and_action_frame.grid(row=6, column=0, sticky="nsew", pady=(0, DEFAULT_PAD), padx=DEFAULT_PAD)
        pupils_label_and_action_frame.rowconfigure(0, weight=0)
        pupils_label_and_action_frame.columnconfigure(0, weight=1)
        pupils_label_and_action_frame.columnconfigure([1, 2], weight=0)

        pupils_label = ctk.CTkLabel(
            pupils_label_and_action_frame,
            font=ctk.CTkFont(**SECONDARY_TITLE_FONT),
            fg_color="transparent",
            anchor="w",
            text="Pupils"
        )
        pupils_label.grid(row=0, column=0, sticky="nsew", padx=(0, SMALL_PAD))

        add_one_image = ctk.CTkImage(
            light_image=Image.open(os.path.join(os.getcwd(), "images/light-add-one.png")),
            dark_image=Image.open(os.path.join(os.getcwd(), "images/dark-add-one.png")),
            size=(15, 15)
        )
        add_one_button = ctk.CTkButton(
            pupils_label_and_action_frame,
            fg_color="transparent",
            image=add_one_image,
            command=self.add_one_clicked,
            text="",
            width=25,
            height=25,
            hover_color=BUTTON_HOVER_COLOR,
            corner_radius=5
        )

        add_one_button.grid(row=0, column=1, sticky="e", padx=(0, SMALL_PAD))

        add_many_image = ctk.CTkImage(
            light_image=Image.open(os.path.join(os.getcwd(), "images/light-add-many.png")),
            dark_image=Image.open(os.path.join(os.getcwd(), "images/dark-add-many.png")),
            size=(15, 15)
        )
        add_many_button = ctk.CTkButton(
            pupils_label_and_action_frame,
            fg_color="transparent",
            image=add_many_image,
            command=self.add_many_clicked,
            text="",
            width=25,
            height=25,
            hover_color=BUTTON_HOVER_COLOR,
            corner_radius=5
        )

        add_many_button.grid(row=0, column=2, sticky="e")

        self.pupils_in_report = PupilScrollframe(self)
        self.pupils_in_report.grid(row=7, column=0, sticky="nsew", pady=(0, DEFAULT_PAD), padx=DEFAULT_PAD)

        if self.report_set is not None:
            for report in self.app_engine.individual_report_collection.values():
                if report.report_set == self.report_set.id:
                    self.pupils_in_report.add_pupil(report)

        save_report_frame = ctk.CTkFrame(self, fg_color="transparent")
        save_report_frame.grid(row=8, column=0, sticky="nsew", pady=(0, DEFAULT_PAD), padx=DEFAULT_PAD)
        save_report_frame.rowconfigure(0, weight=0)
        save_report_frame.columnconfigure([0, 1, 2, 3], weight=1, uniform="columns")

        save_button = ctk.CTkButton(
            save_report_frame,
            text="Save",
            font=ctk.CTkFont(**NORMAL_LABEL_FONT),
            command=self.save_clicked
        )
        save_button.grid(row=0, column=2, sticky="nsew", padx=(0, SMALL_PAD))

        cancel_button = SecondaryButton(
            save_report_frame,
            text="Cancel",
            font=ctk.CTkFont(**NORMAL_LABEL_FONT),
            command=self.cancel_clicked
        )
        cancel_button.grid(row=0, column=3, sticky="nsew")

        self.rowconfigure([0, 1, 2, 3, 4, 5, 6, 8], weight=0)
        self.rowconfigure(7, weight=1)
        self.columnconfigure(0, weight=1)

        self.grab_set()
        self.after(10, self.report_name_entry.focus_set)
        self.wait_window()

    def add_one_clicked(self):
        add_one_tl = AddOneToplevel(self)

        pupil_info = add_one_tl.get_pupil_info()

        if pupil_info is not None:
            new_individual_report_id = self.new_individual_report_tracker
            self.new_individual_report_tracker += 1

            new_individual_report = IndividualReport(
                NewIndividualReport(
                    report_id=new_individual_report_id,
                    forename=pupil_info["forename"].lower(),
                    surname=pupil_info["surname"].lower(),
                    gender=pupil_info["gender"].lower(),
                    user=self.app_engine.get_user_id(),
                    report_set="@0",
                    report_text=""
                )
            )
            self.pupils_in_report.add_pupil(new_individual_report)

        self.grab_set()

    def add_many_clicked(self):
        add_many_tl = AddManyToplevel(self)
        pupil_info_list = add_many_tl.get_pupil_info()

        if pupil_info_list is not None:
            for pupil in pupil_info_list:
                new_individual_report_id = self.new_individual_report_tracker
                self.new_individual_report_tracker += 1

                new_individual_report = IndividualReport(
                    NewIndividualReport(
                        report_id=new_individual_report_id,
                        forename=pupil["forename"].lower(),
                        surname=pupil["surname"].lower(),
                        gender=pupil["gender"].lower(),
                        user=self.app_engine.get_user_id(),
                        report_set="@0",
                        report_text=""
                    )
                )
                self.pupils_in_report.add_pupil(new_individual_report)

        self.grab_set()

    def save_clicked(self):
        no_errors = True

        if self.report_name_entry.get() == "":
            no_errors = False
            self.report_name_entry.configure(border_color=BAD_COLOR)
        else:
            self.report_name_entry.configure(border_color=("#979DA2", "#565B5E"))

        if self.class_entry.get() == "":
            no_errors = False
            self.class_entry.configure(border_color=BAD_COLOR)
        else:
            self.class_entry.configure(border_color=("#979DA2", "#565B5E"))

        if self.template_selection.get() == "Choose template...":
            self.template_selection.configure(button_color=BAD_COLOR, fg_color=BAD_COLOR)
            no_errors = False
        else:
            self.template_selection.configure(button_color=LABEL_CARD_COLOR, fg_color=LABEL_CARD_COLOR)

        if not no_errors:
            return
        else:
            if self.report_set is None:
                new_set_report_id = f"@{self.app_engine.create_new_record_id('report_set')}"

                template_used = ""
                for template in self.app_engine.template_collection.values():
                    if template.template_title.lower() == self.template_selection.get().lower():
                        template_used = template.id

                new_set_report = SingleReportSet(
                    NewReportSet(
                        record_id=new_set_report_id,
                        report_title=self.report_name_entry.get().strip().lower(),
                        class_name=self.class_entry.get().strip().lower(),
                        user=self.app_engine.get_user_id(),
                        template=template_used
                    )
                )

                new_set_report.report_number = len(self.pupils_in_report.all_cards.values())

                created_set_report = self.app_engine.upload_new_record(
                    data=new_set_report.data_to_create(),
                    collection="report_set",
                    container_type=SingleReportSet
                )

                if created_set_report is None:
                    self.report_set = None
                    return

                self.report_set = created_set_report

                self.app_engine.reports_set_collection[self.report_set.id] = created_set_report
                self.app_engine.copy_of_reports_set_collection[self.report_set.id] = created_set_report.copy()

                for card in self.pupils_in_report.all_cards.values():
                    card.card_data.report_set = self.report_set.id
                    created_individual_report = self.app_engine.upload_new_record(
                        data=card.card_data.data_to_create(),
                        collection="individual_reports",
                        container_type=IndividualReport
                    )

                    if created_individual_report is None:
                        return

                    self.app_engine.individual_report_collection[created_individual_report.id] = \
                        created_individual_report

                    self.app_engine.copy_of_individual_report_collection[created_individual_report.id] = \
                        created_individual_report.copy()
            else:
                working_report = self.app_engine.copy_of_reports_set_collection[self.report_set.id].copy()

                working_report.report_title = self.report_name_entry.get().strip().lower()
                working_report.class_name = self.class_entry.get().strip().lower()
                working_report.report_number = len(self.pupils_in_report.all_cards.values())

                if working_report != self.report_set:
                    updated_report = self.app_engine.update_record(
                        record_id=working_report.id,
                        data=working_report.data_to_create(),
                        collection="report_set",
                        container_type=SingleReportSet
                    )

                    if updated_report is None:
                        self.report_set = None
                        return

                    self.app_engine.reports_set_collection[updated_report.id] = updated_report
                    self.report_set = updated_report
                    self.app_engine.copy_of_reports_set_collection[updated_report.id] = updated_report.copy()

                for report_id, report in self.pupils_in_report.all_cards.items():
                    if report_id not in self.app_engine.individual_report_collection.keys():
                        report.card_data.report_set = self.report_set.id
                        created_individual_report = self.app_engine.upload_new_record(
                            data=report.card_data.data_to_create(),
                            collection="individual_reports",
                            container_type=IndividualReport
                        )

                        if created_individual_report is None:
                            return

                        self.app_engine.individual_report_collection[created_individual_report.id] = \
                            created_individual_report

                        self.app_engine.copy_of_individual_report_collection[created_individual_report.id] = \
                            created_individual_report.copy()

                    elif report.card_data != self.app_engine.individual_report_collection[report_id]:
                        updated_individual_report = self.app_engine.update_record(
                            record_id=report_id,
                            data=report.card_data.data_to_create(),
                            collection="individual_reports",
                            container_type=IndividualReport
                        )

                        if updated_individual_report is None:
                            return

                        self.app_engine.individual_report_collection[report_id] = updated_individual_report
                        self.app_engine.copy_of_individual_report_collection[report_id] = \
                            updated_individual_report.copy()

                deleted_reports = [i for i in self.app_engine.copy_of_individual_report_collection.values() if
                                   i.report_set == self.report_set.id and
                                   i.id not in self.pupils_in_report.all_cards.keys()]
                for report_to_delete in deleted_reports:
                    response = self.app_engine.delete_record(
                        report_to_delete.id,
                        collection="individual_reports"
                    )

                    if not response:
                        return

                    self.app_engine.copy_of_individual_report_collection.pop(report_to_delete.id)
                    self.app_engine.individual_report_collection.pop(report_to_delete.id)

        self.destroy()

    def cancel_clicked(self):
        self.report_set = None
        self.destroy()

    def get_report(self) -> SingleReportSet | None:
        return self.report_set
