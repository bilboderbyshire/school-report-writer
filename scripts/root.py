import customtkinter as ctk
from .settings import *
import os


class ReportWriter(ctk.CTk):
    def __init__(self):
        super().__init__()

        ctk.set_default_color_theme(os.path.join(os.getcwd(), "scripts/app-theme.json"))

        ws = self.winfo_screenwidth()
        hs = self.winfo_screenheight()

        x = int((ws / 2) - (WIDTH / 2))
        y = int((hs / 2) - (HEIGHT / 2))

        self.geometry(f"{GEOMETRY}+{x}+{y}")
        self.title(WINDOW_TITLE)
        self.iconbitmap(default=os.path.join(os.getcwd(), "images/app-logo.ico"))
