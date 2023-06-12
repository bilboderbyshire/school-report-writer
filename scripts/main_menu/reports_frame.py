import customtkinter as ctk
from ..settings import *
from ..database import RUNNING_DB
from ..containers import SingleReportSet
from ..components import AutohidingScrollableAndLoadingFrame


class ReportsScrollableFrame(AutohidingScrollableAndLoadingFrame):
    def __init__(self, master, reports_set: list[SingleReportSet]):
        super().__init__(master,
                         label_font=ctk.CTkFont(**NORMAL_LABEL_FONT),
                         label_anchor="w",
                         label_fg_color="transparent",
                         label_text="Reports")





