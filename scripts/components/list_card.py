import customtkinter as ctk
from ..settings import *
from ..containers import SingleReportSet


class ListCard(ctk.CTkFrame):
    def __init__(self, master, report_set: SingleReportSet,
                 fg_color=ROOT_BG, text_color=STANDARD_TEXT_COLOR):
        super().__init__(master,
                         height=80,
                         fg_color=fg_color)
