import customtkinter as ctk
from .. import title_bar as tbar
from ..settings import *
from .reports_scrollframe import ReportsScrollableFrame
from .templates_scrollframe import TemplatesScrollableFrame
from ..database import RUNNING_DB
import CTkMessagebox as ctkmb
from ..components import Separator


class MainMenuScene(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color=ROOT_BG)

        self.title_bar = tbar.TitleBar(self, "Report Writer", refresh_command=self.refresh_frames)
        self.title_bar.grid(row=0, column=0, columnspan=4, sticky="nsew", pady=(DEFAULT_PAD, 0), padx=DEFAULT_PAD)

        title_sep = Separator(self, "hor")
        title_sep.grid(row=1, column=0, columnspan=4, sticky="nsew", padx=DEFAULT_PAD*3, pady=DEFAULT_PAD)

        self.report_frame = ReportsScrollableFrame(self, add_command=self.add_report)
        self.report_frame.grid(row=2, column=0, columnspan=2, sticky="nsew", pady=(0, DEFAULT_PAD),
                               padx=(DEFAULT_PAD, 3))

        frame_sep = Separator(self, "ver")
        frame_sep.grid(row=2, column=2, sticky="nsew", pady=DEFAULT_PAD*3)

        self.template_frame = TemplatesScrollableFrame(self, add_command=self.add_template)
        self.template_frame.grid(row=2, column=3, sticky="nsew", pady=(0, DEFAULT_PAD), padx=(3, DEFAULT_PAD))

        self.rowconfigure([0, 1], weight=0)
        self.rowconfigure(2, weight=1)
        self.columnconfigure([0, 1, 3], weight=1)
        self.columnconfigure(2, weight=0)

        self.bind("<Configure>", lambda event: self.check_if_scroll_needed())

    def fill_frames(self):
        report_response, reports_result = RUNNING_DB.get_set_reports()
        template_response, templates_results = RUNNING_DB.get_available_templates()

        if report_response["response"] and template_response["response"]:
            self.report_frame.build_report_frame(reports_result)
            self.template_frame.build_template_frame(templates_results)
        else:
            if not report_response["response"]:
                error_box = ctkmb.CTkMessagebox(
                    title="Error",
                    message=f"{report_response['message']} - Please try again later",
                    icon="cancel")
            else:
                error_box = ctkmb.CTkMessagebox(
                    title="Error",
                    message=f"{template_response['message']} - Please try again later",
                    icon="cancel")

            error_box.wait_window()

            self.change_cursor("arrow")
            self.master.destroy()
            return

        self.check_if_scroll_needed()

        self.change_cursor("arrow")

    def check_if_scroll_needed(self):
        self.report_frame.check_scrollbar_needed()
        self.template_frame.check_scrollbar_needed()

    def refresh_frames(self):
        self.change_cursor("watch")
        self.report_frame.loading_frame()
        self.template_frame.loading_frame()

        self.after(600, self.fill_frames)

    def change_cursor(self, cursor: str) -> None:
        for i in self.winfo_children():
            i.configure(cursor=cursor)

    def add_report(self):
        print("Adding report")

    def add_template(self):
        template_scene = self.master.show_frame("template-scene")
        template_scene.previous_scene("main-menu")
        template_scene.refresh_frames()

