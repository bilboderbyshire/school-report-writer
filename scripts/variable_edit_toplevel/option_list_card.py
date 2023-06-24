import customtkinter as ctk
from ..settings import *
from ..components import ListCard
from typing import Callable
from PIL import Image
import os


class OptionListCard(ListCard):
    def __init__(self, master,
                 add_option_command: Callable,
                 delete_option_command: Callable,
                 card_id: int,
                 card_text: str = "New option"):
        super().__init__(master, fg_color=SECONDARY_LABEL_CARD_COLOR)

        self.grid_propagate(True)
        self.card_data = card_id

        self.add_variable_command = add_option_command
        self.delete_variable_command = lambda: delete_option_command(self.card_data)

        self.option_text = ctk.StringVar(value=card_text)

        self.entry_frame = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        self.entry_frame.grid(row=0, column=0, sticky="nsew", **SMALL_PAD_COMPLETE)
        self.entry_frame.rowconfigure(0, weight=1)
        self.entry_frame.columnconfigure(0, weight=1)

        self.option_entry = ctk.CTkTextbox(
            self.entry_frame,
            font=ctk.CTkFont(**VERY_SMALL_FONT),
            border_width=2,
            fg_color=("#F9F9FA", "#F9F9FA"),
            text_color="#252525",
            border_color=("#979DA2", "#565B5E"),
            activate_scrollbars=False,
            wrap="word",
            height=0,
            border_spacing=0,
        )
        self.option_entry.grid(row=0, column=0, sticky="nsew")
        self.option_entry.insert("1.0", self.option_text.get())

        self.label_frame = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        self.label_frame.grid(row=0, column=0, sticky="nsew", **SMALL_PAD_COMPLETE)
        self.label_frame.rowconfigure(0, weight=1)
        self.label_frame.columnconfigure(0, weight=1)

        self.option_label = ctk.CTkLabel(
            self.label_frame,
            font=ctk.CTkFont(**VERY_SMALL_FONT),
            fg_color="transparent",
            textvariable=self.option_text,
            padx=3,
            pady=3,
            justify="left",
            anchor="w"
        )
        self.option_label.grid(row=0, column=0, sticky="nsew", **SMALL_PAD_COMPLETE)

        self.label_frame.tkraise(self.entry_frame)

        self.option_label.bind("<Double-Button-1>", lambda event: self.edit_text())
        self.label_frame.bind("<Double-Button-1>", lambda event: self.edit_text())
        self.bind("<Double-Button-1>", lambda event: self.edit_text())
        self.option_label.bind("<Enter>", lambda event: self.on_hover())
        self.label_frame.bind("<Enter>", lambda event: self.on_hover())
        self.option_label.bind("<Leave>", lambda event: self.on_mouse_leave())
        self.label_frame.bind("<Leave>", lambda event: self.on_mouse_leave())
        self.option_label.bind("<Configure>", lambda event: self.resize_label())

        self.entry_frame.bind("<Enter>", lambda event: self.on_hover())
        self.option_entry.bind("<Enter>", lambda event: self.on_hover())
        self.entry_frame.bind("<Leave>", lambda event: self.on_mouse_leave())
        self.option_entry.bind("<Leave>", lambda event: self.on_mouse_leave())

        self.option_entry.bind("<Shift-Return>", lambda event: self.option_entry.focus_set())
        self.option_entry.bind("<Return>", lambda event: self.return_pressed())
        self.option_entry.bind("<FocusOut>", lambda event: self.defocus_text())
        self.option_entry.bind("<KeyRelease>", lambda event: self.resize_entry())

        self.label_frame.bind("<Button-3>", lambda event: self.right_clicked(event))
        self.option_label.bind("<Button-3>", lambda event: self.right_clicked(event))
        self.entry_frame.bind("<Button-3>", lambda event: self.right_clicked(event))
        self.option_entry.bind("<Button-3>", lambda event: self.right_clicked(event))

        self.right_click_menu.add_command(label="Edit item", command=self.edit_text)
        self.right_click_menu.add_command(label="Add item", command=lambda: self.add_variable_command(None))
        self.right_click_menu.add_command(label="Delete item", command=self.delete_variable_command)

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=0)
        self.resize_label()
        self.bind_frame()

        close_image = ctk.CTkImage(
            light_image=Image.open(os.path.join(os.getcwd(), "images/light-close.png")),
            dark_image=Image.open(os.path.join(os.getcwd(), "images/dark-close.png")),
            size=(15, 15)
        )

        self.close_button = ctk.CTkButton(
            self,
            fg_color="transparent",
            image=close_image,
            text="",
            hover_color=BUTTON_HOVER_COLOR,
            corner_radius=5,
            width=0,
            command=self.delete_variable_command
        )

        self.close_button.grid(row=0, column=1, sticky="ne", padx=(0, SMALL_PAD), pady=(SMALL_PAD, 0))

    def resize_label(self):
        self.label_frame.update()
        self.option_label.update()
        self.option_label.configure(wraplength=int(self.option_entry._current_width)-15)

    def resize_entry(self):
        self.option_text.set(self.option_entry.get("1.0", "end-1c"))
        self.option_label.update()
        self.label_frame.update()
        self.option_entry.update()

    def edit_text(self):
        self.option_entry.delete("1.0", "end")
        self.option_entry.insert("1.0", self.option_text.get())
        self.entry_frame.tkraise(self.label_frame)
        self.option_entry.focus_set()

    def return_pressed(self):
        self.focus_set()
        return "break"

    def defocus_text(self):
        self.option_text.set(self.option_entry.get("1.0", "end-1c"))
        self.label_frame.tkraise(self.entry_frame)
        self.resize_label()
