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

        self.app_engine = AppEngine
        self.prev_scene_string = None
        self.title_bar = None
        self.name_entry = None
        self.section_frame = None
        self.pieces_frame = None
        self.piece_info_frame = None
        self.edit_piece_frame = None
        self.template_engine = None

    def __build_frame(self, engine: TemplateEngine):
        self.template_engine = engine

        self.title_bar = tbar.TitleBar(self, "Templates",
                                       refresh_command=self.database_refresh_scene,
                                       back_command=self.go_back)
        self.title_bar.grid(row=0, column=0, columnspan=4, sticky="nsew", pady=(DEFAULT_PAD, 0), padx=DEFAULT_PAD)

        title_sep = Separator(self, "hor")
        title_sep.grid(row=2, column=0, columnspan=4, sticky="nsew", padx=DEFAULT_PAD * 3, pady=DEFAULT_PAD)

        self.name_entry = InvisibleEntry(self, placeholder_text=self.template_engine.template.template_title)
        self.name_entry.grid(row=3, column=0, columnspan=2, sticky="ew", padx=DEFAULT_PAD*2, pady=DEFAULT_PAD)

        self.section_frame = SectionScrollableFrame(self,
                                                    engine=self.template_engine,
                                                    select_section_command=self.new_section_selected)
        self.section_frame.grid(row=4, rowspan=2, column=0, sticky="nsew", padx=DEFAULT_PAD, pady=(0, DEFAULT_PAD))

        self.pieces_frame = PiecesScrollableFrame(self, self.template_engine)
        self.pieces_frame.grid(row=4, column=1, sticky="nsew", padx=(0, DEFAULT_PAD), pady=(0, DEFAULT_PAD))

        self.piece_info_frame = ctk.CTkFrame(self)
        self.piece_info_frame.grid(row=5, column=1, sticky="nsew", padx=(0, DEFAULT_PAD), pady=(0, DEFAULT_PAD))

        self.edit_piece_frame = ctk.CTkFrame(self)
        self.edit_piece_frame.grid(row=4, rowspan=2, column=2, sticky="nsew", padx=(0, DEFAULT_PAD),
                                   pady=(0, DEFAULT_PAD))

        self.rowconfigure([0, 1, 2, 3], weight=0)
        self.rowconfigure([4, 5], weight=1, uniform="rows")
        self.columnconfigure(0, weight=1, uniform="columns")
        self.columnconfigure([1, 2], weight=2, uniform="columns")

    def fill_frames(self):
        self.section_frame.build_section_frame()
        self.pieces_frame.build_pieces_frame()
        self.check_if_scroll_needed()

        self.change_cursor("arrow")

    def refresh_frames(self, template: ReportTemplate = None):
        if self.section_frame is not None:
            self.section_frame.loading_frame()
            self.pieces_frame.loading_frame()

        if template is not None:
            # Todo response, results = RUNNING_DB.get_pieces_in_template(template.id)
            #  if response["response"]:
            #      for i in self.winfo_children():
            #          i.destroy()
            #      new_engine = TemplateEngine(template, results)
            #      self.__build_frame(new_engine)
            #      self.fill_frames()
            #  else:
            #      error_box = ctkmb.CTkMessagebox(
            #          title="Error",
            #          message=f"{response['message']} - Please try again later",
            #          icon="cancel")
            #      error_box.wait_window()
            #      self.change_cursor("arrow")
            #      self.master.destroy()
            pass
        else:
            new_template = ReportTemplate(NewTemplateRecord("@000", "My new template"))
            new_piece = IndividualPiece(NewPieceRecord("@1", 1))
            new_engine = TemplateEngine(new_template, [new_piece])
            self.__build_frame(new_engine)
            self.fill_frames()

    def check_if_scroll_needed(self):
        self.section_frame.check_scrollbar_needed()
        self.pieces_frame.check_scrollbar_needed()

    def change_cursor(self, cursor: str) -> None:
        for i in self.winfo_children():
            i.configure(cursor=cursor)

    def previous_scene(self, name_of_prev_frame: str):
        self.prev_scene_string = name_of_prev_frame

    def go_back(self):
        if not self.discard_unsaved_changes():
            return
        self.master.show_frame(self.prev_scene_string)
        self.prev_scene_string = None
        self.title_bar = None
        self.name_entry = None
        self.section_frame = None
        self.pieces_frame = None
        self.piece_info_frame = None
        self.edit_piece_frame = None
        self.template_engine = None

    def database_refresh_scene(self):
        self.template_engine: TemplateEngine
        if not self.discard_unsaved_changes():
            return

        self.refresh_frames(self.template_engine.template)

    def new_section_selected(self, section_num):
        self.template_engine.change_current_section(section_num)
        self.pieces_frame.build_pieces_frame()

    def discard_unsaved_changes(self) -> bool:
        if not self.template_engine.check_changes():
            warning_box = ctkmb.CTkMessagebox(
                title="Warning",
                message="You have unsaved changes, are you sure you want to do this?",
                icon="warning",
                option_2="Yes",
                option_1="Cancel")

            warning_box.wait_window()

            if warning_box.get() == "Cancel":
                return False

        return True
