import customtkinter as ctk
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
                                  refresh_command=self.refresh_scene,
                                  back_command=self.go_back)
        title_bar.grid(row=0, column=0, columnspan=4, sticky="nsew", pady=(DEFAULT_PAD, 0), padx=DEFAULT_PAD)

        title_sep = Separator(self, "hor")
        title_sep.grid(row=2, column=0, columnspan=4, sticky="nsew", padx=DEFAULT_PAD * 3, pady=DEFAULT_PAD)

        name_entry = InvisibleEntry(self,
                                    placeholder_text=self.working_template.template_title,
                                    validate="key",
                                    validatecommand=(self.register(self.validate_name), "%P"))
        name_entry.grid(row=3, column=0, columnspan=2, sticky="ew", padx=DEFAULT_PAD * 2, pady=(0, DEFAULT_PAD+6))

        self.section_frame = SectionScrollableFrame(self,
                                                    app_engine=self.app_engine,
                                                    structured_pieces=self.structured_pieces,
                                                    select_section_command=self.new_section_selected,
                                                    card_add_command=("Add section", self.add_section),
                                                    card_delete_command=("Delete", self.delete_section))
        self.section_frame.grid(row=4, rowspan=2, column=0, sticky="nsew", padx=DEFAULT_PAD, pady=(0, DEFAULT_PAD))

        self.pieces_frame = PiecesScrollableFrame(self,
                                                  structured_pieces=self.structured_pieces,
                                                  select_piece_command=self.new_piece_selected,
                                                  card_add_command=("Add piece", self.add_piece),
                                                  card_delete_command=("Delete", self.delete_piece),
                                                  card_copy_command=("Copy", self.copy_piece))
        self.pieces_frame.grid(row=4, column=1, sticky="nsew", padx=(0, DEFAULT_PAD), pady=(0, DEFAULT_PAD))

        self.piece_info_frame = ctk.CTkFrame(self)
        self.piece_info_frame.grid(row=5, column=1, sticky="nsew", padx=(0, DEFAULT_PAD), pady=(0, DEFAULT_PAD))

        self.edit_piece_frame = EditPieceFrame(self,
                                               edit_command=self.piece_edited,
                                               variables_collection=self.app_engine.copy_of_user_variables_collection,
                                               create_variable_command=self.create_variable)
        self.edit_piece_frame.grid(row=4, rowspan=2, column=2, sticky="nsew", padx=(0, DEFAULT_PAD),
                                   pady=(0, DEFAULT_PAD))

        self.rowconfigure([0, 1, 2, 3], weight=0)
        self.rowconfigure([4, 5], weight=1, uniform="rows")
        self.columnconfigure(0, weight=1, uniform="columns")
        self.columnconfigure([1, 2], weight=2, uniform="columns")

        self.bind("<Configure>", lambda event: self.pieces_frame.update_all_text_displays())

    def fill_frames(self):
        for i in self.winfo_children():
            i.destroy()

        self.__build_frame()

        self.section_frame.build_section_frame()

        all_sections = list(self.structured_pieces.keys())
        if all_sections:
            self.selected_section = all_sections[0]
            self.section_frame.all_cards[self.selected_section].card_selected()
        else:
            self.selected_section = None

        self.pieces_frame.build_pieces_frame(self.selected_section)

        if self.selected_section is not None:
            self.new_piece_selected()

        self.change_cursor("arrow")

        self.check_if_scroll_needed()
        self.focus_set()

    def setup_scene(self, template: ReportTemplate):
        self.working_template = template
        self.structured_pieces = self.app_engine.create_piece_to_template(self.working_template.id)

    def refresh_scene(self):
        self.change_cursor("watch")
        self.section_frame.loading_frame()
        self.pieces_frame.loading_frame()

        self.after(700, self.app_engine.load_data)

        self.structured_pieces = self.app_engine.create_piece_to_template(self.working_template.id)
        self.fill_frames()

    def check_if_scroll_needed(self):
        self.section_frame.check_scrollbar_needed()
        self.pieces_frame.check_scrollbar_needed()

    def change_cursor(self, cursor: str) -> None:
        self.configure(cursor=cursor)
        for i in self.winfo_children():
            i.configure(cursor=cursor)

    def previous_scene(self, name_of_prev_frame: str):
        self.prev_scene_string = name_of_prev_frame

    def go_back(self):
        new_scene = self.master.show_frame(self.prev_scene_string)
        new_scene.fill_frames()
        self.prev_scene_string = None

    def validate_name(self, P):
        if len(P) <= 40:
            self.app_engine.copy_of_template_collection[self.working_template.id].template_title = P
            return True
        else:
            return False

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
        self.section_frame.build_section_frame()
        self.pieces_frame.build_pieces_frame(new_section_id)

        self.new_section_selected(new_section)
        self.new_piece_selected()
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
        self.section_frame.build_section_frame()

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

        self.pieces_frame.build_pieces_frame(self.selected_section)
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

        self.pieces_frame.build_pieces_frame(self.selected_section)

        if piece.id == self.selected_piece:
            self.new_piece_selected()
        else:
            self.pieces_frame.all_cards[self.selected_piece].card_selected()

    def copy_piece(self, piece: IndividualPiece):
        new_piece_id = f"@{self.app_engine.create_new_record_id('report_pieces')}"
        new_piece = piece.copy()
        new_piece.id = new_piece_id

        self.app_engine.copy_of_piece_collection[new_piece_id] = new_piece
        self.structured_pieces[self.selected_section][new_piece_id] = new_piece

        self.section_frame.reload_card_subtitles()

        self.pieces_frame.build_pieces_frame(self.selected_section)
        self.new_piece_selected(new_piece)

        self.check_if_scroll_needed()

    def piece_edited(self, piece: IndividualPiece, new_text: str):
        if new_text.strip() == "":
            piece.piece_text = "Empty piece"
        else:
            piece.piece_text = new_text.strip()
        self.pieces_frame.all_cards[piece.id].update_display_text()

    def create_variable(self):
        new_variable_id = f"@{self.app_engine.create_new_record_id('user_variables')}"
        new_variable = UserVariable(NewUserVariableRecord(
            new_variable_id,
            "New variable",
            self.app_engine.get_user_id()
        ))
        VariableEditToplevel(self.master, new_variable, self.app_engine.copy_of_user_variables_collection)
        self.grab_set()
