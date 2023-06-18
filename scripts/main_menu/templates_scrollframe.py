import customtkinter as ctk
from ..settings import *
from ..components import AutohidingScrollableAndLoadingFrame
from .template_card import TemplateCard
from ..app_engine import AppEngine
from typing import Callable


class TemplatesScrollableFrame(AutohidingScrollableAndLoadingFrame):
    def __init__(self, master,
                 app_engine: AppEngine,
                 select_template_command: Callable,
                 card_add_command: tuple[str, Callable],
                 card_copy_command: tuple[str, Callable],
                 card_delete_command: tuple[str, Callable],
                 add_command=None):
        super().__init__(master,
                         label_font=ctk.CTkFont(**SECONDARY_TITLE_FONT),
                         label_anchor="w",
                         label_fg_color="transparent",
                         label_text="Templates",
                         fg_color=ROOT_BG,
                         button_command=add_command)

        # Right click menu option commands
        self.card_add = card_add_command
        self.card_copy = card_copy_command
        self.card_delete = card_delete_command

        self.app_engine = app_engine
        self.select_template_command = select_template_command

    def build_template_frame(self):

        for i in self.winfo_children():
            i.destroy()

        self.update_idletasks()

        templates = self.app_engine.copy_of_template_collection.values()

        for index, template in enumerate(templates):
            new_card = TemplateCard(self,
                                    self.app_engine,
                                    template,
                                    click_command=self.select_template_command,
                                    add_command=self.card_add,
                                    copy_command=self.card_copy,
                                    delete_command=self.card_delete
                                    )
            if index == len(templates) - 1:
                new_card.grid(row=index, column=0, sticky="ew", padx=DEFAULT_PAD - 7)
            else:
                new_card.grid(row=index, column=0, sticky="ew", padx=DEFAULT_PAD - 7, pady=(0, DEFAULT_PAD))

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=0)

