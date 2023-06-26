import customtkinter as ctk
from ..settings import *
from ..app_engine import AppEngine
from ..containers import ReportTemplate
from ..title_bar import TitleBar
from ..components import Separator, SecondaryButton
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..root import ReportWriter


class ReportScene(ctk.CTkFrame):
    def __init__(self, master, app_engine: AppEngine):
        super().__init__(master, fg_color=ROOT_BG)

        self.app_engine = app_engine
        self.prev_scene_string = None
        self.report_template: ReportTemplate = None

        self.pupil_name_sv = ctk.StringVar(value="Sally")
        self.pupil_gender_sv = ctk.StringVar(value="NB")

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
        name_and_actions.columnconfigure([0, 2], weight=0)
        name_and_actions.columnconfigure(1, weight=1)

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
        self.pupil_gender_label.grid(row=0, column=0, sticky="nsew")

        self.pupil_name_label = ctk.CTkLabel(
            name_and_actions,
            textvariable=self.pupil_name_sv,
            fg_color="transparent",
            font=ctk.CTkFont(**SECONDARY_TITLE_FONT),
            anchor="w"
        )
        self.pupil_name_label.grid(row=0, column=1, sticky="nsew", padx=(DEFAULT_PAD, 0))

        pupil_button_frame = ctk.CTkFrame(name_and_actions, fg_color="transparent")
        pupil_button_frame.grid(row=0, column=2, sticky="nsew", pady=2)
        pupil_button_frame.rowconfigure(0, weight=1)
        pupil_button_frame.columnconfigure([0, 1, 2, 3], weight=0, uniform="columns")

        show_pupils_button = SecondaryButton(
            pupil_button_frame,
            text="Pupils...",
            font=ctk.CTkFont(**NORMAL_LABEL_FONT),
            width=80
        )
        show_pupils_button.grid(row=0, column=0, sticky="nsew", padx=(0, SMALL_PAD))

        previous_pupil_button = SecondaryButton(
            pupil_button_frame,
            text="Prev",
            font=ctk.CTkFont(**NORMAL_LABEL_FONT),
            width=0,
        )
        previous_pupil_button.grid(row=0, column=1, sticky="nsew", padx=(0, SMALL_PAD))

        save_pupil_button = ctk.CTkButton(
            pupil_button_frame,
            text="Save",
            font=ctk.CTkFont(**NORMAL_LABEL_FONT),
            width=0,
        )
        save_pupil_button.grid(row=0, column=2, sticky="nsew", padx=(0, SMALL_PAD))

        next_pupil_button = SecondaryButton(
            pupil_button_frame,
            text="Next",
            font=ctk.CTkFont(**NORMAL_LABEL_FONT),
            width=0,
        )
        next_pupil_button.grid(row=0, column=3, sticky="nsew")

        section_piece_frame = ctk.CTkFrame(self)
        section_piece_frame.grid(row=3, column=0, sticky="nsew", padx=DEFAULT_PAD, pady=(0, DEFAULT_PAD))

        report_frame = ctk.CTkFrame(self)
        report_frame.grid(row=3, column=1, sticky="nsew", padx=(0, DEFAULT_PAD), pady=(0, DEFAULT_PAD))

        self.rowconfigure([0, 1, 2], weight=0)
        self.rowconfigure(3, weight=1)
        self.columnconfigure(0, weight=2)
        self.columnconfigure(1, weight=5)

    def fill_frames(self):
        for i in self.winfo_children():
            i.destroy()

        self.__build_frame()

    def previous_scene(self, name_of_prev_frame: str):
        self.prev_scene_string = name_of_prev_frame

    def go_back(self):
        self.master: ReportWriter
        new_scene = self.master.get_frame(self.prev_scene_string)
        new_scene.fill_frames()
        self.after(10, self.master.show_frame, self.prev_scene_string)
        self.prev_scene_string = None
