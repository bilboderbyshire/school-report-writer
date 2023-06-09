from __future__ import annotations
import customtkinter as ctk
from typing import TYPE_CHECKING
from .. import title_bar as tbar
from ..settings import *
from ..components import Separator, InvisibleEntry
from ..app_engine import AppEngine
from .section_scrollframe import SectionScrollableFrame
from .pieces_scrollframe import PiecesScrollableFrame
from .edit_piece_frame import EditPieceFrame
from ..containers import ReportTemplate, NewPieceRecord, IndividualPiece, TemplateSection, NewSectionRecord, \
    NewUserVariableRecord, UserVariable
import CTkMessagebox as ctkmb
from ..variable_edit_toplevel import VariableEditToplevel
from ..copy_template_from_toplevel import CopyTemplateFromToplevel
from PIL import Image
import os

if TYPE_CHECKING:
    from ..root import ReportWriter


class TemplateScene(ctk.CTkFrame):
    def __init__(self, master, app_engine: AppEngine):
        super().__init__(master, fg_color=ROOT_BG)

        self.app_engine = app_engine
        self.prev_scene_string = None
        self.working_template: ReportTemplate = None
        self.structured_pieces: dict[str, dict[str, IndividualPiece]] = None

        self.selected_section: str | None = None
        self.selected_piece: str | None = None

    def __build_frame(self):

        title_bar = tbar.TitleBar(self, "Edit template",
                                  back_command=self.go_back)
        title_bar.grid(row=0, column=0, columnspan=4, sticky="nsew", pady=(DEFAULT_PAD, 0), padx=DEFAULT_PAD)

        title_sep = Separator(self, "hor")
        title_sep.grid(row=2, column=0, columnspan=4, sticky="nsew", padx=DEFAULT_PAD * 3, pady=DEFAULT_PAD)

        template_name_and_actions_frame = ctk.CTkFrame(self, fg_color="transparent")
        template_name_and_actions_frame.grid(row=3,
                                             column=0,
                                             columnspan=4,
                                             sticky="nsew",
                                             padx=DEFAULT_PAD * 2,
                                             pady=(0, DEFAULT_PAD+6))
        template_name_and_actions_frame.rowconfigure(0, weight=0)
        template_name_and_actions_frame.columnconfigure(0, weight=1)
        template_name_and_actions_frame.columnconfigure([1, 2], weight=0)

        self.name_entry = InvisibleEntry(template_name_and_actions_frame,
                                         placeholder_text=self.working_template.template_title,
                                         validate="key",
                                         validatecommand=(self.register(self.validate_name), "%P"))
        self.name_entry.grid(row=0, column=0, sticky="ew")

        save_image = ctk.CTkImage(
            light_image=Image.open(os.path.join(os.getcwd(), "images/light-save.png")),
            dark_image=Image.open(os.path.join(os.getcwd(), "images/dark-save.png")),
            size=(25, 25)
        )
        save_button = ctk.CTkButton(
            template_name_and_actions_frame,
            fg_color="transparent",
            image=save_image,
            command=self.save_clicked,
            text="",
            width=35,
            height=35,
            hover_color=BUTTON_HOVER_COLOR,
            corner_radius=5
        )

        save_button.grid(row=0, column=1, sticky="e", padx=SMALL_PAD)

        share_image = ctk.CTkImage(
            light_image=Image.open(os.path.join(os.getcwd(), "images/light-share.png")),
            dark_image=Image.open(os.path.join(os.getcwd(), "images/dark-share.png")),
            size=(25, 25)
        )
        share_button = ctk.CTkButton(
            template_name_and_actions_frame,
            fg_color="transparent",
            image=share_image,
            command=lambda: print("Shared"),
            text="",
            width=35,
            height=35,
            hover_color=BUTTON_HOVER_COLOR,
            corner_radius=5
        )

        share_button.grid(row=0, column=2, sticky="e", padx=(0, SMALL_PAD))

        self.section_frame = SectionScrollableFrame(self,
                                                    app_engine=self.app_engine,
                                                    structured_pieces=self.structured_pieces,
                                                    select_section_command=self.new_section_selected,
                                                    card_add_command=("Add section", self.add_section),
                                                    card_delete_command=("Delete", self.delete_section))
        self.section_frame.grid(row=4, column=0, sticky="nsew", padx=DEFAULT_PAD, pady=(0, DEFAULT_PAD))

        self.pieces_frame = PiecesScrollableFrame(self,
                                                  structured_pieces=self.structured_pieces,
                                                  select_piece_command=self.new_piece_selected,
                                                  card_add_command=("Add piece", self.add_piece),
                                                  card_delete_command=("Delete", self.delete_piece),
                                                  card_duplicate_command=("Duplicate", self.duplicate_piece),
                                                  copy_from_command=self.copy_from)
        self.pieces_frame.grid(row=4, column=1, sticky="nsew", padx=(0, DEFAULT_PAD), pady=(0, DEFAULT_PAD))

        self.edit_piece_frame = EditPieceFrame(self,
                                               edit_command=self.piece_edited,
                                               variables_collection=self.app_engine.copy_of_user_variables_collection,
                                               create_variable_command=self.create_variable,
                                               edit_variable_command=self.edit_variable,
                                               copy_variable_command=self.copy_variable)
        self.edit_piece_frame.grid(row=4, column=2, sticky="nsew", padx=(0, DEFAULT_PAD),
                                   pady=(0, DEFAULT_PAD))

        self.rowconfigure([0, 1, 2, 3], weight=0)
        self.rowconfigure([4], weight=1)
        self.columnconfigure(0, weight=1, uniform="columns")
        self.columnconfigure([1, 2], weight=2, uniform="columns")

        self.bind("<Configure>", lambda event: self.pieces_frame.update_all_text_displays())

    def fill_frames(self):
        for i in self.winfo_children():
            i.destroy()

        self.__build_frame()

        all_sections = list(self.structured_pieces.keys())
        if all_sections:
            self.selected_section = all_sections[0]
            self.section_frame.all_cards[self.selected_section].card_selected()
        else:
            self.selected_section = None

        self.pieces_frame.build_pieces_frame(self.selected_section)

        if self.selected_section is not None:
            self.new_piece_selected()

        self.change_cursor("")

        self.check_if_scroll_needed()
        self.focus_set()

    def setup_scene(self, template: ReportTemplate):
        self.working_template = template
        self.structured_pieces = self.app_engine.create_piece_to_template(self.working_template.id)

    def check_if_scroll_needed(self):
        self.section_frame.check_scrollbar_needed()
        self.pieces_frame.check_scrollbar_needed()

    def change_cursor(self, cursor: str) -> None:
        self.configure(cursor=cursor)

    def previous_scene(self, name_of_prev_frame: str):
        self.prev_scene_string = name_of_prev_frame

    def go_back(self):
        self.master: ReportWriter
        new_scene = self.master.get_frame(self.prev_scene_string)
        new_scene.fill_frames()
        self.after(10, self.master.show_frame, self.prev_scene_string)
        self.prev_scene_string = None

    def validate_name(self, p):
        if len(p) <= 40:
            self.app_engine.copy_of_template_collection[self.working_template.id].template_title = p
            return True
        else:
            return False

    def copy_from(self, _) -> None:
        choice_tracker = ctk.StringVar(value="cancel")
        new_toplevel = CopyTemplateFromToplevel(
            self,
            app_engine=self.app_engine,
            choice_tracker=choice_tracker
        )
        results = new_toplevel.get_results()

        for collection, ids in results.items():
            if collection == "section":
                for section_id in ids:
                    new_section_id = f"@{self.app_engine.create_new_record_id('template_sections')}"
                    section_copy = self.app_engine.copy_of_section_collection[section_id].copy()
                    old_id = section_copy.id
                    section_copy.id = new_section_id
                    section_copy.template = self.working_template.id

                    self.structured_pieces[new_section_id] = {}
                    self.app_engine.copy_of_section_collection[new_section_id] = section_copy

                    ids_to_copy = []
                    for piece in self.app_engine.copy_of_piece_collection.values():
                        if piece.section == old_id:
                            ids_to_copy.append(piece.id)

                    for piece_id in ids_to_copy:
                        new_piece_id = f"@{self.app_engine.create_new_record_id('report_pieces')}"
                        piece_copy = self.app_engine.copy_of_piece_collection[piece_id].copy()
                        piece_copy.id = new_piece_id
                        piece_copy.section = new_section_id
                        self.structured_pieces[new_section_id][new_piece_id] = piece_copy
                        self.app_engine.copy_of_piece_collection[new_piece_id] = piece_copy

                    self.section_frame.add_card(section_copy)
            elif collection == "piece":
                if self.selected_section is None:
                    print("Oops, this shouldn't have happened. It looks like you tried copying pieces into an " +
                          "unselected section")
                    return
                for piece_id in ids:
                    new_piece_id = f"@{self.app_engine.create_new_record_id('report_pieces')}"
                    piece_copy = self.app_engine.copy_of_piece_collection[piece_id]
                    piece_copy.id = new_piece_id
                    piece_copy.section = self.selected_section
                    self.structured_pieces[self.selected_section][new_piece_id] = piece_copy
                    self.app_engine.copy_of_piece_collection[new_piece_id] = piece_copy
                    self.pieces_frame.add_card(piece_copy)

        self.grab_set()
        self.grab_release()

    def new_section_selected(self, section: TemplateSection):
        if self.selected_section is not None:
            if section.id == self.selected_section:
                return

            self.section_frame.all_cards[self.selected_section].card_deselected()

        self.selected_section = section.id
        self.section_frame.all_cards[self.selected_section].card_selected()
        self.pieces_frame.build_pieces_frame(self.selected_section)
        self.new_piece_selected()
        self.pieces_frame.check_scrollbar_needed()

    def add_section(self, _):
        current_section_titles = []

        for section in self.app_engine.copy_of_section_collection.values():
            if section.template == self.working_template.id:
                current_section_titles.append(section.section_title)
        max_title_number = 1
        for title in current_section_titles:
            if title[0:12] == "New section ":
                try:
                    if title[12::] == "" and max_title_number == 1:
                        max_title_number = 2
                    elif int(title[12::]) >= max_title_number:
                        max_title_number = int(title[12::]) + 1
                except ValueError:
                    continue

        new_section_name = f"New section {max_title_number if max_title_number > 1 else ''}"
        new_section_id = f"@{self.app_engine.create_new_record_id('template_sections')}"

        new_section = TemplateSection(NewSectionRecord(
            section_id=new_section_id,
            section_title=new_section_name,
            template_id=self.working_template.id
        ))

        self.structured_pieces[new_section_id] = {}
        self.app_engine.copy_of_section_collection[new_section_id] = new_section
        self.section_frame.add_card(new_section)
        self.pieces_frame.build_pieces_frame(new_section_id)

        self.new_section_selected(new_section)
        self.check_if_scroll_needed()

        self.section_frame.all_cards[new_section_id].entry_enabled()

    def delete_section(self, section: TemplateSection):
        if self.structured_pieces[section.id]:
            warning_box = ctkmb.CTkMessagebox(
                title="Warning",
                message=f"Are you sure you want to delete section '{section.section_title}' and all the pieces "
                        f"inside?\n\nYou will not be able to undo this move",
                icon="cancel",
                option_2="Yes",
                option_1="No")
            warning_box.wait_window()

            if warning_box.get() == "No":
                return

        for piece_id, piece in self.structured_pieces[section.id].items():
            self.app_engine.copy_of_piece_collection.pop(piece_id)

        self.structured_pieces.pop(section.id)
        self.app_engine.copy_of_section_collection.pop(section.id)
        self.section_frame.delete_card(section)

        if section.id == self.selected_section:
            all_sections = list(self.structured_pieces.keys())
            if all_sections:
                self.selected_section = all_sections[0]
                self.section_frame.all_cards[self.selected_section].card_selected()
            else:
                self.selected_section = None

            self.pieces_frame.build_pieces_frame(self.selected_section)
            self.new_piece_selected()
        else:
            self.section_frame.all_cards[self.selected_section].card_selected()

        self.check_if_scroll_needed()

    def add_piece(self, _):
        new_piece_id = f"@{self.app_engine.create_new_record_id('report_pieces')}"
        new_piece = IndividualPiece(NewPieceRecord(new_piece_id, self.selected_section))

        self.app_engine.copy_of_piece_collection[new_piece_id] = new_piece
        self.structured_pieces[self.selected_section][new_piece_id] = new_piece

        self.section_frame.reload_card_subtitles()

        self.pieces_frame.add_card(new_piece)
        self.new_piece_selected(new_piece)
        self.check_if_scroll_needed()

    def new_piece_selected(self, piece: IndividualPiece | None = None):
        if piece is not None:
            if piece.id == self.selected_piece:
                return
            if self.selected_piece is not None:
                self.pieces_frame.all_cards[self.selected_piece].card_deselected()
            self.selected_piece = piece.id
            self.pieces_frame.all_cards[self.selected_piece].card_selected()
            self.edit_piece_frame.display_piece(piece)
        elif self.selected_section is not None:
            all_pieces = list(self.structured_pieces[self.selected_section].keys())
            if all_pieces:
                self.selected_piece = all_pieces[0]
                self.pieces_frame.all_cards[self.selected_piece].card_selected()
                self.edit_piece_frame.display_piece(self.app_engine.copy_of_piece_collection[self.selected_piece])
            else:
                self.edit_piece_frame.display_piece(piece)
                self.selected_piece = None
        else:
            self.edit_piece_frame.display_piece(piece)
            self.selected_piece = None

    def delete_piece(self, piece: IndividualPiece):
        self.structured_pieces[self.selected_section].pop(piece.id)
        self.app_engine.copy_of_piece_collection.pop(piece.id)

        self.section_frame.reload_card_subtitles()

        self.pieces_frame.delete_card(piece)

        if piece.id == self.selected_piece:
            self.new_piece_selected()
        else:
            self.pieces_frame.all_cards[self.selected_piece].card_selected()

    def duplicate_piece(self, piece: IndividualPiece):
        new_piece_id = f"@{self.app_engine.create_new_record_id('report_pieces')}"
        new_piece = piece.copy()
        new_piece.id = new_piece_id

        self.app_engine.copy_of_piece_collection[new_piece_id] = new_piece
        self.structured_pieces[self.selected_section][new_piece_id] = new_piece

        self.section_frame.reload_card_subtitles()

        self.pieces_frame.add_card(new_piece)
        self.new_piece_selected(new_piece)

        self.check_if_scroll_needed()

    def piece_edited(self, piece: IndividualPiece, new_text: str):
        if new_text.strip() == "":
            piece.piece_text = "Empty piece"
        else:
            piece.piece_text = new_text.strip()
        self.pieces_frame.all_cards[piece.id].update_display_text()

    def create_variable(self):
        tracker_var = ctk.StringVar(value="cancel")
        new_variable_id = f"@{self.app_engine.create_new_record_id('user_variables')}"
        new_variable = UserVariable(NewUserVariableRecord(
            new_variable_id,
            "New variable",
            self.app_engine.get_user_id()
        ))
        VariableEditToplevel(self.master,
                             variable_to_edit=new_variable,
                             variable_collection=self.app_engine.copy_of_user_variables_collection,
                             edit_type="add",
                             top_level_choice_tracker=tracker_var)
        self.grab_set()
        self.grab_release()
        if tracker_var.get() == "save":
            new_variable = self.app_engine.upload_new_record(
                data=new_variable.data_to_create(),
                collection="user_variables",
                container_type=UserVariable)
            self.app_engine.copy_of_user_variables_collection[new_variable.id] = new_variable
            self.app_engine.user_variables_collection[new_variable_id] = new_variable.copy()
            self.edit_piece_frame.user_inserts.refresh_variable_dropdown(new_variable)
        else:
            self.edit_piece_frame.user_inserts.refresh_variable_dropdown(None)

    def edit_variable(self, variable: UserVariable):
        tracker_var = ctk.StringVar(value="cancel")
        VariableEditToplevel(self.master,
                             variable_to_edit=variable,
                             variable_collection=self.app_engine.copy_of_user_variables_collection,
                             edit_type="edit",
                             top_level_choice_tracker=tracker_var)
        self.grab_set()
        self.grab_release()
        if tracker_var.get() == "delete":
            self.app_engine.delete_record(variable.id, "user_variables")
            self.app_engine.copy_of_user_variables_collection.pop(variable.id)
            self.app_engine.user_variables_collection.pop(variable.id)
            self.edit_piece_frame.user_inserts.refresh_variable_dropdown(None)
        elif tracker_var.get() == "cancel":
            self.edit_piece_frame.user_inserts.refresh_variable_dropdown(variable)
        else:
            updated_variable = self.app_engine.update_record(
                record_id=variable.id,
                data=variable.data_to_create(),
                collection="user_variables",
                container_type=UserVariable
            )
            self.edit_piece_frame.user_inserts.refresh_variable_dropdown(variable)
            self.app_engine.copy_of_user_variables_collection[variable.id] = variable
            self.app_engine.user_variables_collection[variable.id] = updated_variable.copy()

    def copy_variable(self, variable: UserVariable):
        tracker_var = ctk.StringVar(value="cancel")
        new_variable_id = f"@{self.app_engine.create_new_record_id('user_variables')}"
        copied_variable = variable.copy()
        copied_variable.id = new_variable_id

        VariableEditToplevel(self.master,
                             variable_to_edit=copied_variable,
                             variable_collection=self.app_engine.copy_of_user_variables_collection,
                             edit_type="copy",
                             top_level_choice_tracker=tracker_var)
        self.grab_set()
        self.grab_release()
        if tracker_var.get() == "save":
            new_variable = self.app_engine.upload_new_record(
                data=copied_variable.data_to_create(),
                collection="user_variables",
                container_type=UserVariable)
            self.app_engine.copy_of_user_variables_collection[new_variable.id] = new_variable
            self.app_engine.user_variables_collection[new_variable_id] = new_variable.copy()
            self.edit_piece_frame.user_inserts.refresh_variable_dropdown(new_variable)
        else:
            self.edit_piece_frame.user_inserts.refresh_variable_dropdown(variable)

    def save_clicked(self):
        self.change_cursor("watch")
        self.update()
        self.after(700, self.save_template)

    def save_template(self) -> None:
        # Keep track of old IDs for matching sections made in new templates
        old_template_id = self.working_template.id

        # Save changes to template record first
        template_save = self.save_template_record(old_template_id)
        if not template_save:
            self.change_cursor("")
            return

        # Save changes to any sections (and the pieces inside them)
        section_save = self.save_section_records(old_template_id)
        if not section_save:
            self.change_cursor("")
            return

        # Check if any pieces or sections were deleted, and save that action to the database
        deletion_save = self.save_deleted_records(old_template_id)
        if not deletion_save:
            self.change_cursor("")
            return

        # Refresh the current structured pieces with new/updated data
        self.structured_pieces = self.app_engine.create_piece_to_template(self.working_template.id)

        # Rebuild the scene
        self.fill_frames()

        self.change_cursor("")

    def save_template_record(self, old_template_id: str) -> bool:
        # Save template name
        current_template_titles = [i.template_title for i in self.app_engine.copy_of_template_collection.values()
                                   if i.id != self.working_template.id]
        if self.working_template.template_title in current_template_titles:
            self.name_entry.text_entry.configure(border_width=2, border_color=BAD_COLOR)
            warning_box = ctkmb.CTkMessagebox(
                title="Warning",
                message=f"Template title '{self.working_template.template_title}' already exists. Please try a new one",
                icon="cancel",
                option_1="OK")
            warning_box.wait_window()
            return False
        else:
            self.name_entry.text_entry.configure(border_width=0)

        if "@" in self.working_template.id:
            old_owner = self.working_template.owner
            new_template = self.app_engine.upload_new_record(
                data=self.working_template.data_to_create(),
                collection="templates",
                container_type=ReportTemplate
            )

            if new_template is None:
                return False

            new_template.owner = old_owner

            self.app_engine.copy_of_template_collection.pop(old_template_id)
            self.app_engine.copy_of_template_collection[new_template.id] = new_template
            self.working_template = new_template

            self.app_engine.template_collection[new_template.id] = new_template.copy()
        elif self.app_engine.copy_of_template_collection[self.working_template.id] != \
                self.app_engine.template_collection[self.working_template.id]:

            old_owner = self.working_template.owner
            updated_template = self.app_engine.update_record(
                record_id=self.working_template.id,
                data=self.working_template.data_to_create(),
                collection="templates",
                container_type=ReportTemplate
            )
            if updated_template is None:
                return False

            updated_template.owner = old_owner

            self.app_engine.copy_of_template_collection[self.working_template.id] = updated_template
            self.working_template = updated_template
            self.app_engine.template_collection[self.working_template.id] = updated_template.copy()

        return True

    def save_section_records(self, old_template_id: str) -> bool:
        # Save sections
        relevant_sections = [i for i in self.app_engine.copy_of_section_collection.values()
                             if i.template == old_template_id]

        # Validate section titles first
        all_titles_valid = True
        for section in relevant_sections:
            current_section_names = [i.section_title.lower() for i in relevant_sections if i.id != section.id]
            if section.section_title.lower() in current_section_names:
                all_titles_valid = False
                self.section_frame.all_cards[section.id].section_name.configure(text_color=BAD_COLOR)
            else:
                self.section_frame.all_cards[section.id].section_name.configure(text_color=STANDARD_TEXT_COLOR)

        if not all_titles_valid:
            warning_box = ctkmb.CTkMessagebox(
                title="Warning",
                message=f"Some section names are not unique. Please rename them",
                icon="cancel",
                option_1="OK")
            warning_box.wait_window()
            return False

        # Upload sections first
        for section in relevant_sections:
            old_section_id = section.id
            new_section_id = section.id
            if "@" in section.id:
                section.template = self.working_template.id
                new_section = self.app_engine.upload_new_record(
                    data=section.data_to_create(),
                    collection="template_sections",
                    container_type=TemplateSection
                )
                if new_section is None:
                    return False

                self.app_engine.copy_of_section_collection.pop(old_section_id)
                self.app_engine.copy_of_section_collection[new_section.id] = new_section

                self.app_engine.section_collection[new_section.id] = new_section.copy()

                new_section_id = new_section.id

            elif section != self.app_engine.section_collection[section.id]:
                updated_section = self.app_engine.update_record(
                    record_id=section.id,
                    data=section.data_to_create(),
                    collection="template_sections",
                    container_type=TemplateSection
                )

                if updated_section is None:
                    return False

                self.app_engine.copy_of_section_collection[updated_section.id] = updated_section
                self.app_engine.section_collection[updated_section.id] = updated_section.copy()

            return self.save_piece_records(old_section_id, new_section_id)

    def save_piece_records(self, old_section_id, new_section_id) -> bool:
        relevant_pieces = [i for i in self.app_engine.copy_of_piece_collection.values()
                           if i.section == old_section_id]

        for piece in relevant_pieces:
            old_piece_id = piece.id

            if piece.section != new_section_id:
                piece.section = new_section_id

            if "@" in piece.id:
                new_piece = self.app_engine.upload_new_record(
                    data=piece.data_to_create(),
                    collection="report_pieces",
                    container_type=IndividualPiece
                )
                if new_piece is None:
                    return False

                self.app_engine.copy_of_piece_collection.pop(old_piece_id)
                self.app_engine.copy_of_piece_collection[new_piece.id] = new_piece

                self.app_engine.piece_collection[new_piece.id] = new_piece.copy()
            elif piece != self.app_engine.piece_collection[piece.id]:
                updated_piece = self.app_engine.update_record(
                    record_id=piece.id,
                    data=piece.data_to_create(),
                    collection="report_pieces",
                    container_type=IndividualPiece
                )
                if updated_piece is None:
                    return False

                self.app_engine.copy_of_piece_collection[updated_piece.id] = updated_piece
                self.app_engine.piece_collection[updated_piece.id] = updated_piece.copy()

        return True

    def save_deleted_records(self, old_template_id: str) -> bool:
        # Catch database records that have been deleted
        deleted_sections = [i for i in self.app_engine.section_collection.values()
                            if i.template == old_template_id
                            and i.id not in self.app_engine.copy_of_section_collection.keys()]
        if deleted_sections:
            for section in deleted_sections:
                response = self.app_engine.delete_record(
                    record_id=section.id,
                    collection="template_sections"
                )
                if not response:
                    return response

                self.app_engine.section_collection.pop(section.id)

                pieces_to_cascade_delete = [i.id for i in self.app_engine.piece_collection.values()
                                            if i.section == section.id]
                for piece_id in pieces_to_cascade_delete:
                    self.app_engine.piece_collection.pop(piece_id)

        deleted_pieces = [i for i in self.app_engine.piece_collection.values()
                          if self.app_engine.section_collection[i.section].template == old_template_id
                          and i.id not in self.app_engine.copy_of_piece_collection.keys()]

        if deleted_pieces:
            for piece in deleted_pieces:
                response = self.app_engine.delete_record(
                    record_id=piece.id,
                    collection="report_pieces"
                )
                if not response:
                    return response

                self.app_engine.piece_collection.pop(piece.id)

        return True
