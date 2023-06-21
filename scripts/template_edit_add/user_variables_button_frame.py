import customtkinter as ctk
from ..settings import *
from ..components import SecondaryOptionmenu, SecondaryButton


class UserVariablesButtonFrame(ctk.CTkFrame):
    def __init__(self,
                 master):
        super().__init__(master,
                         fg_color="transparent")

        title_label = ctk.CTkLabel(
            self,
            font=ctk.CTkFont(**SMALL_LABEL_FONT),
            anchor="w",
            fg_color="transparent",
            text="Create variables")

        title_label.grid(row=0, column=0, columnspan=3, sticky="nw", pady=(5, 6))

        self.variable_button_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.variable_button_frame.grid(row=1, column=0, sticky="nsew", padx=(0, SMALL_PAD), pady=(0, SMALL_PAD))

        self.select_variable = SecondaryOptionmenu(
            self.variable_button_frame,
            font=ctk.CTkFont(**VERY_SMALL_FONT),
            values=["Option1",
                    "Option2"]
        )
        self.select_variable.grid(row=0, column=0, sticky="ew", pady=(0, SMALL_PAD))

        self.insert_button = ctk.CTkButton(
            self.variable_button_frame,
            font=ctk.CTkFont(**VERY_SMALL_FONT),
            text="Insert",
            state="disabled"
        )
        self.insert_button.grid(row=1, column=0, sticky="ew")

        self.variable_button_frame.rowconfigure([0, 1], weight=0)
        self.variable_button_frame.columnconfigure(0, weight=1)

        self.variable_view_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.variable_view_frame.grid(row=1, column=1, sticky="nsew", pady=(0, SMALL_PAD))

        self.variable_textbox = ctk.CTkTextbox(
            self.variable_view_frame,
            font=ctk.CTkFont(**VERY_SMALL_FONT),
            fg_color="transparent",
            text_color=FADED_TEXT_COLOR,
            border_width=2,
            wrap="word",
            height=10,
            width=10,
        )
        self.variable_textbox.grid(row=0, column=0, columnspan=3, sticky="nsew", pady=(0, SMALL_PAD))
        self.variable_textbox.insert("1.0", "hello")
        self.variable_textbox.configure(state="disabled")

        self.edit_button = SecondaryButton(
            self.variable_view_frame,
            font=ctk.CTkFont(**VERY_SMALL_FONT),
            text="Edit",
            state="disabled"
        )
        self.edit_button.grid(row=1, column=1, sticky="ew", padx=(0, SMALL_PAD), pady=(0, SMALL_PAD))

        self.copy_button = SecondaryButton(
            self.variable_view_frame,
            font=ctk.CTkFont(**VERY_SMALL_FONT),
            text="Copy",
            state="disabled"
        )
        self.copy_button.grid(row=1, column=2, sticky="ew", pady=(0, SMALL_PAD))

        self.variable_view_frame.rowconfigure(0, weight=1)
        self.variable_view_frame.rowconfigure(1, weight=0)
        self.variable_view_frame.columnconfigure([0, 1, 2], weight=1, uniform="row")

        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1, uniform="columns")
        self.columnconfigure(1, weight=2, uniform="columns")
