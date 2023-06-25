import customtkinter as ctk
from ..components import ListCard
from ..containers import ReportTemplate
from ..settings import *
from ..app_engine import AppEngine
from typing import Callable
from PIL import Image
import os


class TemplateCard(ListCard):
    def __init__(self, master,
                 app_engine: AppEngine,
                 template: ReportTemplate,
                 add_command: tuple[str, Callable],
                 copy_command: tuple[str, Callable],
                 delete_command: tuple[str, Callable],
                 click_command: Callable):
        super().__init__(master, click_command=click_command)
        self.card_data = template

        # Right click menu options
        self.right_click_menu.add_command(label=add_command[0], command=add_command[1])
        self.right_click_menu.add_command(label=copy_command[0], command=lambda: copy_command[1](self.card_data))
        self.right_click_menu.add_command(label=delete_command[0], command=lambda: delete_command[1](self.card_data))

        title_text = f"{self.card_data.template_title}"
        if "@" in self.card_data.id:
            title_text = "*" + title_text

        title_label = ctk.CTkLabel(self,
                                   fg_color="transparent",
                                   text=title_text,
                                   font=ctk.CTkFont(**NORMAL_LABEL_FONT),
                                   anchor="nw",
                                   padx=0,
                                   pady=0)
        title_label.grid(row=0, column=0, columnspan=3, sticky="ew", padx=DEFAULT_PAD, pady=SMALL_PAD)

        if self.card_data.owner is None:
            owner_string = "Created by: Unknown"
        elif self.card_data.owner.id == app_engine.get_user_id():
            owner_string = "Created by: Me"
        else:
            owner_string = f"Created and shared by: {self.card_data.owner.forename} " + \
                           f"{self.card_data.owner.surname}"

        owner_label = ctk.CTkLabel(self,
                                   fg_color="transparent",
                                   text=owner_string,
                                   font=ctk.CTkFont(**SMALL_LABEL_FONT, slant="italic"),
                                   anchor="nw",
                                   padx=0,
                                   pady=0)
        owner_label.grid(row=1, column=0, sticky="ew", padx=(DEFAULT_PAD, DEFAULT_PAD // 2))

        button_frame = ctk.CTkFrame(self,
                                    fg_color="transparent")
        button_frame.grid(row=2, column=0, sticky="nsew", padx=(DEFAULT_PAD, DEFAULT_PAD // 2), pady=(0, DEFAULT_PAD))

        copy_image = ctk.CTkImage(
            light_image=Image.open(os.path.join(os.getcwd(), "images/light-copy.png")),
            dark_image=Image.open(os.path.join(os.getcwd(), "images/dark-copy.png")),
            size=(15, 15)
            )
        copy_button = ctk.CTkButton(
            button_frame,
            fg_color="transparent",
            image=copy_image,
            command=lambda: copy_command[1](self.card_data),
            text="",
            width=0,
            height=0,
            hover_color=BUTTON_HOVER_COLOR,
            corner_radius=5
        )

        copy_button.grid(row=0, column=0, sticky="e", padx=(0, SMALL_PAD))

        delete_image = ctk.CTkImage(
            light_image=Image.open(os.path.join(os.getcwd(), "images/bin.png")),
            dark_image=Image.open(os.path.join(os.getcwd(), "images/bin.png")),
            size=(15, 15)
        )
        delete_button = ctk.CTkButton(
            button_frame,
            fg_color="transparent",
            image=delete_image,
            command=lambda: delete_command[1](self.card_data),
            text="",
            width=0,
            height=0,
            hover_color=BUTTON_HOVER_COLOR,
            corner_radius=5
        )

        delete_button.grid(row=0, column=1, sticky="e", padx=(0, SMALL_PAD))

        self.rowconfigure([0, 1, 2], weight=0)
        self.columnconfigure([0], weight=1, uniform="columns")
        self.bind_frame()
