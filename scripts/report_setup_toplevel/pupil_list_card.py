import customtkinter as ctk
from ..components import ListCard
from ..settings import *
from ..containers import PupilInfo
from PIL import Image
from typing import Callable
import os


class PupilListCard(ListCard):
    def __init__(self,
                 master,
                 pupil_info: PupilInfo,
                 delete_command: Callable,
                 edit_command: Callable,
                 index: int):
        super().__init__(master, fg_color=SECONDARY_LABEL_CARD_COLOR, click_command=edit_command)

        self.card_data = index
        self.pupil_info = pupil_info
        self.delete_command = delete_command

        self.grid_propagate(True)

        forename_label = ctk.CTkLabel(
            self,
            text=f"Forename: {self.pupil_info['forename'].capitalize()}",
            font=ctk.CTkFont(**SMALL_LABEL_FONT),
            fg_color="transparent",
            justify="left",
            anchor="w",
        )
        forename_label.grid(row=0, column=0, sticky="nsew", padx=SMALL_PAD)

        surname_label = ctk.CTkLabel(
            self,
            text=f"Surname: {self.pupil_info['surname'].capitalize()}",
            font=ctk.CTkFont(**SMALL_LABEL_FONT),
            fg_color="transparent",
            justify="left",
            anchor="w",
        )
        surname_label.grid(row=1, column=0, sticky="nsew", padx=SMALL_PAD)

        gender_label = ctk.CTkLabel(
            self,
            text=f"Gender: {self.pupil_info['gender'].upper()}",
            font=ctk.CTkFont(**SMALL_LABEL_FONT),
            fg_color="transparent",
            justify="left",
            anchor="w",
        )
        gender_label.grid(row=2, column=0, sticky="nsew", padx=SMALL_PAD, pady=(0, SMALL_PAD))

        self.bind_frame()

        delete_image = ctk.CTkImage(
            light_image=Image.open(os.path.join(os.getcwd(), "images/light-close.png")),
            dark_image=Image.open(os.path.join(os.getcwd(), "images/dark-close.png")),
            size=(15, 15)
        )
        delete_button = ctk.CTkButton(
            self,
            fg_color="transparent",
            image=delete_image,
            command=lambda: self.delete_command(self.card_data),
            text="",
            width=30,
            height=30,
            hover_color=BUTTON_HOVER_COLOR,
            corner_radius=5
        )

        delete_button.grid(row=0, rowspan=3, column=1, sticky="ne", padx=(0, SMALL_PAD), pady=SMALL_PAD)

        self.rowconfigure("all", weight=0)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=0)

