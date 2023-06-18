import customtkinter as ctk
from .. import title_bar as tbar
from ..settings import *
from ..components import Separator, InvisibleEntry
from ..app_engine import AppEngine
from .section_scrollframe import SectionScrollableFrame
from .pieces_scrollframe import PiecesScrollableFrame
from .template_engine import TemplateEngine
from ..containers import ReportTemplate, NewTemplateRecord, NewPieceRecord, IndividualPiece
import CTkMessagebox as ctkmb


class TemplateScene(ctk.CTkFrame):
    def __init__(self, master, app_engine: AppEngine):
        super().__init__(master, fg_color=ROOT_BG)

        self.app_engine = app_engine
        self.prev_scene_string = None
        self.working_template: ReportTemplate = None
        self.structured_pieces: dict[int, dict[str, IndividualPiece]] = None

        self.selected_section: int = None

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
        name_entry.grid(row=3, column=0, columnspan=2, sticky="ew", padx=DEFAULT_PAD * 2, pady=DEFAULT_PAD)

        self.section_frame = SectionScrollableFrame(self,
                                                    structured_pieces=self.structured_pieces,
                                                    select_section_command=self.new_section_selected,
                                                    card_add_command=("Add section", self.add_section),
                                                    card_delete_command=("Delete", self.delete_section))
        self.section_frame.grid(row=4, rowspan=2, column=0, sticky="nsew", padx=DEFAULT_PAD, pady=(0, DEFAULT_PAD))
        #
        # self.pieces_frame = PiecesScrollableFrame(self,
        #                                           app_engine=self.app_engine)
        # self.pieces_frame.grid(row=4, column=1, sticky="nsew", padx=(0, DEFAULT_PAD), pady=(0, DEFAULT_PAD))
        #
        # self.piece_info_frame = ctk.CTkFrame(self)
        # self.piece_info_frame.grid(row=5, column=1, sticky="nsew", padx=(0, DEFAULT_PAD), pady=(0, DEFAULT_PAD))
        #
        # self.edit_piece_frame = ctk.CTkFrame(self)
        # self.edit_piece_frame.grid(row=4, rowspan=2, column=2, sticky="nsew", padx=(0, DEFAULT_PAD),
        #                            pady=(0, DEFAULT_PAD))

        self.rowconfigure([0, 1, 2, 3], weight=0)
        self.rowconfigure([4, 5], weight=1, uniform="rows")
        self.columnconfigure(0, weight=1, uniform="columns")
        self.columnconfigure([1, 2], weight=2, uniform="columns")

    def fill_frames(self):
        for i in self.winfo_children():
            i.destroy()

        self.update_idletasks()

        self.__build_frame()

        self.section_frame.build_section_frame()
        # self.pieces_frame.build_pieces_frame()
        self.check_if_scroll_needed()

        all_sections = list(self.structured_pieces.keys())
        if all_sections:
            self.selected_section = all_sections[0]

        self.section_frame.all_cards[self.selected_section].card_selected()

        self.change_cursor("arrow")

    def setup_scene(self, template: ReportTemplate):
        self.working_template = template
        self.structured_pieces = self.app_engine.create_piece_to_template(self.working_template.id)

    def refresh_scene(self):
        self.change_cursor("watch")
        self.section_frame.loading_frame()
        # self.pieces_frame.loading_frame()

        self.after(700, self.app_engine.load_data)

        self.structured_pieces = self.app_engine.create_piece_to_template(self.working_template.id)
        self.fill_frames()

    def check_if_scroll_needed(self):
        self.section_frame.check_scrollbar_needed()
        # self.pieces_frame.check_scrollbar_needed()

    def change_cursor(self, cursor: str) -> None:
        self.configure(cursor=cursor)
        for i in self.winfo_children():
            i.configure(cursor=cursor)

    def previous_scene(self, name_of_prev_frame: str):
        self.prev_scene_string = name_of_prev_frame

    def go_back(self):
        self.master.show_frame(self.prev_scene_string)
        self.prev_scene_string = None

    def new_section_selected(self, section_num: int):
        self.section_frame.all_cards[self.selected_section].card_deselected()
        self.selected_section = section_num
        self.section_frame.all_cards[self.selected_section].card_selected()
        # self.pieces_frame.build_pieces_frame()

    def validate_name(self, P):
        if len(P) <= 40:
            self.app_engine.copy_of_template_collection[self.working_template.id].template_title = P
            return True
        else:
            return False

    def add_section(self, _):
        new_section_num = max(self.structured_pieces.keys(), default=0) + 1

        self.structured_pieces[new_section_num] = {}

        self.section_frame.build_section_frame()
        self.section_frame.check_scrollbar_needed()
        self.new_section_selected(new_section_num)

    def delete_section(self, section: int):
        if self.structured_pieces[section]:
            warning_box = ctkmb.CTkMessagebox(
                title="Warning",
                message=f"Are you sure you want to delete section {section} and all the pieces inside?\n"
                        f"You will not be able to undo this move",
                icon="cancel",
                option_2="Yes",
                option_1="No")
            warning_box.wait_window()

            if warning_box.get() == "No":
                return

        for piece_id, piece in self.structured_pieces[section].items():
            self.app_engine.copy_of_piece_collection.pop(piece_id)

        self.structured_pieces.pop(section)
        self.section_frame.build_section_frame()
        self.section_frame.check_scrollbar_needed()

        if section == self.selected_section:
            all_sections = list(self.structured_pieces.keys())
            if all_sections:
                self.selected_section = all_sections[0]
                self.section_frame.all_cards[self.selected_section].card_selected()
            else:
                self.selected_section = None
        else:
            self.section_frame.all_cards[self.selected_section].card_selected()
