import customtkinter as ctk
from ..components import ListCard
from ..containers import SingleReportSet
from ..settings import *
from .. import utils


class ReportSetCard(ListCard):
    def __init__(self, master, report_set: SingleReportSet, command=None):
        super().__init__(master, command=command)

        self.report_data = report_set

        self.title_label = ctk.CTkLabel(self,
                                        fg_color="transparent",
                                        text=f"{self.report_data.report_title} - " +
                                             f"Using: my first template",
                                        font=ctk.CTkFont(**NORMAL_LABEL_FONT),
                                        anchor="nw",
                                        padx=0,
                                        pady=0)
        self.title_label.grid(row=0, column=0, columnspan=3, sticky="ew", padx=DEFAULT_PAD, pady=(SMALL_PAD, DEFAULT_PAD))

        self.class_label = ctk.CTkLabel(self,
                                        fg_color="transparent",
                                        text=f"Class: {self.report_data.class_name}",
                                        font=ctk.CTkFont(**SMALL_LABEL_FONT),
                                        anchor="nw",
                                        padx=0,
                                        pady=0)
        self.class_label.grid(row=1, column=0, sticky="ew", padx=(DEFAULT_PAD, DEFAULT_PAD//2),
                              pady=(0, DEFAULT_PAD))

        self.completed_label = ctk.CTkLabel(self,
                                            fg_color="transparent",
                                            text=f"Completed: {self.report_data.report_completed}/" +
                                            f"{self.report_data.report_number}",
                                            font=ctk.CTkFont(**SMALL_LABEL_FONT),
                                            anchor="n",
                                            padx=0,
                                            pady=0)
        self.completed_label.grid(row=1, column=1, columnspan=2, sticky="ew", padx=DEFAULT_PAD, pady=(0, DEFAULT_PAD))

        completion_pct = self.report_data.report_completed / self.report_data.report_number
        self.progressbar = ctk.CTkProgressBar(self,
                                              progress_color=self.calculate_color_gradient(completion_pct),
                                              fg_color=PROGRESS_BAR_BASE_COLOR,
                                              height=5,
                                              border_width=0)
        self.progressbar.set(completion_pct)
        self.progressbar.grid(row=2, column=0, columnspan=3, sticky="ew", padx=DEFAULT_PAD, pady=(0, DEFAULT_PAD))

        self.rowconfigure([0, 1, 2], weight=0)
        self.columnconfigure([0, 1, 2], weight=1, uniform="columns")
        self.bind_frame()

    @staticmethod
    def calculate_color_gradient(percentage: float) -> str:
        if percentage <= 0.5:
            color_diffs = tuple([ALMOST_COMPLETED_COLOR[i]-NOT_COMPLETED_COLOR[i] for i in range(3)])
            real_pct = percentage/0.5
            new_color = tuple([int(NOT_COMPLETED_COLOR[i] + (real_pct * color_diffs[i])) for i in range(3)])
        else:
            color_diffs = tuple([COMPLETED_COLOR[i] - ALMOST_COMPLETED_COLOR[i] for i in range(3)])
            real_pct = (percentage - 0.5) / 0.5
            new_color = tuple([int(ALMOST_COMPLETED_COLOR[i] + (real_pct * color_diffs[i])) for i in range(3)])

        return utils.rgb_to_hex(new_color)
