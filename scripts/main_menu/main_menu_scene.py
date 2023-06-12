import time
import customtkinter as ctk
from .. import title_bar as tbar
from ..settings import *
from .reports_frame import ReportsScrollableFrame


class MainMenuScene(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color=ROOT_BG)

        self.title_bar = tbar.TitleBar(self, "Report Writer")
        self.title_bar.grid(row=0, column=0, columnspan=3, sticky="nsew", **DEFAULT_PAD_COMPLETE)

        self.report_frame = ReportsScrollableFrame(
            self, None
        )
        self.report_frame.grid(row=1, column=0, columnspan=2, sticky="nsew", pady=(0, DEFAULT_PAD), padx=DEFAULT_PAD)

        self.template_frame = ctk.CTkFrame(
            self,
        )
        self.template_frame.grid(row=1, column=2, sticky="nsew", pady=(0, DEFAULT_PAD), padx=(0, DEFAULT_PAD))

        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=1)
        self.columnconfigure([0, 1, 2], weight=1)

        self.configure(cursor="watch")

        self.after(500, self.fill_frames)

        self.bind("<Configure>", lambda event: self.check_if_scroll_needed())

    def fill_frames(self):
        # simulate long task fetching database values
        time.sleep(2)

        self.report_frame.build_frame(15)

        self.check_if_scroll_needed()

        self.configure(cursor="arrow")

    def check_if_scroll_needed(self):
        self.report_frame.check_scrollbar_needed()
