import customtkinter as ctk
from ..settings import *
from ..containers import SingleReportSet


class ReportFrame(ctk.CTkScrollableFrame):
    def __init__(self, master, all_reports_set: list[SingleReportSet] = None):
        super().__init__(master,
                         label_font=ctk.CTkFont(**NORMAL_LABEL_FONT),
                         label_text="Reports",
                         label_anchor="w",
                         label_fg_color="transparent")





