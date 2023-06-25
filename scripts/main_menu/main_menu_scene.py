from __future__ import annotations
from typing import TYPE_CHECKING
import customtkinter as ctk
from .. import title_bar as tbar
from ..settings import *
from .reports_scrollframe import ReportsScrollableFrame
from .templates_scrollframe import TemplatesScrollableFrame
import CTkMessagebox as ctkmb
from ..components import Separator
from ..containers import ReportTemplate, NewTemplateRecord
from ..app_engine import AppEngine

if TYPE_CHECKING:
    from ..root import ReportWriter


class MainMenuScene(ctk.CTkFrame):
    def __init__(self, master, app_engine: AppEngine):
        super().__init__(master, fg_color=ROOT_BG)

        self.app_engine = app_engine

    def __build_frame(self):

        self.title_bar = tbar.TitleBar(self, "Report Writer", refresh_command=self.refresh_scene)
        self.title_bar.grid(row=0, column=0, columnspan=4, sticky="nsew", pady=(DEFAULT_PAD, 0), padx=DEFAULT_PAD)

        title_sep = Separator(self, "hor")
        title_sep.grid(row=1, column=0, columnspan=4, sticky="nsew", padx=DEFAULT_PAD*3, pady=DEFAULT_PAD)

        self.report_frame = ReportsScrollableFrame(self,
                                                   app_engine=self.app_engine,
                                                   add_command=self.add_report)
        self.report_frame.grid(row=2, column=0, columnspan=2, sticky="nsew", pady=(0, DEFAULT_PAD),
                               padx=(DEFAULT_PAD, 3))

        frame_sep = Separator(self, "ver")
        frame_sep.grid(row=2, column=2, sticky="nsew", pady=DEFAULT_PAD*3)

        self.template_frame = TemplatesScrollableFrame(
            self,
            app_engine=self.app_engine,
            select_template_command=self.edit_template,
            add_command=self.add_template,
            card_add_command=("Add new template", self.add_template),
            card_delete_command=("Delete", self.delete_template),
            card_copy_command=("Copy", self.copy_template)
        )
        self.template_frame.grid(row=2, column=3, sticky="nsew", pady=(0, DEFAULT_PAD), padx=(3, DEFAULT_PAD))

        self.rowconfigure([0, 1], weight=0)
        self.rowconfigure(2, weight=1)
        self.columnconfigure([0, 1, 3], weight=1)
        self.columnconfigure(2, weight=0)

        self.bind("<Configure>", lambda event: self.check_if_scroll_needed())

    def fill_frames(self):
        for i in self.winfo_children():
            i.destroy()

        self.update_idletasks()

        self.__build_frame()

        self.report_frame.build_report_frame()
        self.template_frame.build_template_frame()
        self.check_if_scroll_needed()
        self.change_cursor("arrow")

    def check_if_scroll_needed(self):
        self.report_frame.check_scrollbar_needed()
        self.template_frame.check_scrollbar_needed()

    def refresh_scene(self):
        self.change_cursor("watch")
        self.report_frame.loading_frame()
        self.template_frame.loading_frame()

        self.after(700, self.app_engine.load_data)
        self.fill_frames()

    def change_cursor(self, cursor: str) -> None:
        self.configure(cursor=cursor)
        for i in self.winfo_children():
            i.configure(cursor=cursor)

    def add_report(self):
        print("Adding report")

    def add_template(self):
        current_template_titles: list[str] = [i.template_title
                                              for i in self.app_engine.copy_of_template_collection.values()]

        max_default_title = 1
        for i in current_template_titles:
            if "My new template " == i[0:16]:
                try:
                    if i[16::] == "" and max_default_title == 1:
                        max_default_title = 2
                    elif int(i[16::]) >= max_default_title:
                        max_default_title = int(i[16::]) + 1
                except ValueError:
                    continue

        new_template_id = self.app_engine.create_new_record_id(collection="templates")
        template_title = f"My new template {max_default_title if max_default_title > 1 else ''}"
        blank_template = ReportTemplate(NewTemplateRecord(template_id=f"@{new_template_id}",
                                                          template_title=template_title,
                                                          owner=self.app_engine.user_container))
        self.app_engine.copy_of_template_collection[blank_template.id] = blank_template
        self.template_frame.build_template_frame()
        self.template_frame.check_scrollbar_needed()

    def copy_template(self, card_info: ReportTemplate) -> ReportTemplate:
        new_title = "Copy of " + card_info.template_title
        new_id = f"@{self.app_engine.create_new_record_id('templates')}"

        copied_template = card_info.copy()
        copied_template.template_title = new_title
        copied_template.owner = self.app_engine.user_container.copy()
        copied_template.id = new_id

        self.app_engine.copy_of_template_collection[new_id] = copied_template

        structured_pieces = self.app_engine.create_piece_to_template(card_info.id)
        for section_id, piece_dict in structured_pieces.items():
            new_section_id = f"@{self.app_engine.create_new_record_id('template_sections')}"
            copied_section = self.app_engine.copy_of_section_collection[section_id].copy()
            copied_section.id = new_section_id
            copied_section.template = new_id
            self.app_engine.copy_of_section_collection[new_section_id] = copied_section

            for piece_id in piece_dict.keys():
                new_piece_id = f"@{self.app_engine.create_new_record_id('report_pieces')}"
                current_piece = self.app_engine.copy_of_piece_collection[piece_id]
                copied_piece = current_piece.copy()
                copied_piece.id = new_piece_id
                copied_piece.section = new_section_id
                self.app_engine.copy_of_piece_collection[new_piece_id] = copied_piece

        self.template_frame.build_template_frame()
        self.template_frame.check_scrollbar_needed()

        return copied_template

    def delete_template(self, card_info: ReportTemplate):
        def wipe_template():
            structured_pieces = self.app_engine.create_piece_to_template(card_info.id)

            for section_id, pieces_list in structured_pieces.items():
                for piece_id in pieces_list.keys():
                    self.app_engine.copy_of_piece_collection.pop(piece_id)
                self.app_engine.copy_of_section_collection.pop(section_id)
            self.app_engine.copy_of_template_collection.pop(card_info.id)
            self.template_frame.build_template_frame()

        if card_info.owner.id != self.app_engine.get_user_id():
            warning_box = ctkmb.CTkMessagebox(
                title="Warning",
                message=f"You can't delete this template as it does not belong to you",
                icon="cancel",
                option_1="OK")
            warning_box.wait_window()
            return

        warning_message = ctkmb.CTkMessagebox(
            title="Warning",
            message=f"Are you sure you want to delete the template {card_info.template_title} including "
                    f"all the sections and pieces inside?\n\n"
                    f"You will not be able to undo this move",
            icon="warning",
            option_2="Yes",
            option_1="No"
            )
        warning_message.wait_window()
        user_choice = warning_message.get()
        if user_choice == "Yes":
            if "@" in card_info.id:
                wipe_template()
            else:
                response = self.app_engine.db_instance.delete_record("templates", card_info.id)

                if response["response"]:
                    wipe_template()
                else:
                    error_box = ctkmb.CTkMessagebox(
                        title="Error",
                        message=f"Error deleting template - {response['message']}",
                        icon="cancel")
                    error_box.wait_window()

    def edit_template(self, template: ReportTemplate):
        template_to_view = template
        if template_to_view.owner.id != self.app_engine.get_user_id():
            warning_box = ctkmb.CTkMessagebox(
                title="Warning",
                message=f"You cannot edit '{template_to_view.template_title}' because it does not belong to you.\n\n"
                        f"Would you like to make a copy to edit?",
                icon="cancel",
                option_2="Yes",
                option_1="No")
            warning_box.wait_window()

            if warning_box.get() == "Yes":
                template_to_view = self.copy_template(template)
            else:
                return

        self.master: ReportWriter
        template_scene = self.master.get_frame("template-scene")

        template_scene.previous_scene("main-menu")
        template_scene.setup_scene(template_to_view)
        template_scene.fill_frames()

        self.master.show_frame("template-scene")

