import customtkinter as ctk
from .. import title_bar as tbar
from ..settings import *
from .reports_scrollframe import ReportsScrollableFrame
from .templates_scrollframe import TemplatesScrollableFrame
import CTkMessagebox as ctkmb
from ..components import Separator
from ..containers import ReportTemplate
from ..app_engine import AppEngine


class MainMenuScene(ctk.CTkFrame):
    def __init__(self, master, app_engine: AppEngine):
        super().__init__(master, fg_color=ROOT_BG)

        self.app_engine = app_engine

    def __build_frame(self):

        self.title_bar = tbar.TitleBar(self, "Report Writer", refresh_command=self.refresh_frames)
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

        self.template_frame = TemplatesScrollableFrame(self,
                                                       app_engine=self.app_engine,
                                                       select_template_command=self.open_template,
                                                       add_command=self.add_template)
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

    def refresh_frames(self):
        self.change_cursor("watch")
        self.report_frame.loading_frame()
        self.template_frame.loading_frame()

        self.after(600, self.app_engine.load_data)
        self.fill_frames()

    def change_cursor(self, cursor: str) -> None:
        for i in self.winfo_children():
            i.configure(cursor=cursor)

    def add_report(self):
        print("Adding report")

    def add_template(self):
        template_scene = self.master.show_frame("template-scene")
        template_scene.change_cursor("watch")
        template_scene.previous_scene("main-menu")
        self.after(600, template_scene.refresh_frames())

    def open_template(self, template: ReportTemplate):
        template_scene = self.master.show_frame("template-scene")
        template_scene.change_cursor("watch")
        template_scene.previous_scene("main-menu")
        self.after(600, template_scene.refresh_frames(template))
