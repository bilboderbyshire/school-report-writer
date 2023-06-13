import customtkinter as ctk
from ..settings import *
import os
from PIL import Image


class AutohidingScrollableAndLoadingFrame(ctk.CTkScrollableFrame):
    def __init__(self, master,
                 scrollbar_button_color=STANDARD_SCROLLBAR_BUTTON_COLOR,
                 scrollbar_button_hover_color=STANDARD_SCROLLBAR_BUTTON_HOVER_COLOR,
                 button_command=None,
                 **kwargs):

        super().__init__(master,
                         scrollbar_button_color=scrollbar_button_color,
                         scrollbar_button_hover_color=scrollbar_button_hover_color,
                         **kwargs)

        self.button_command = button_command
        self.scrollbar_color = scrollbar_button_color
        self.scrollbar_hover_color = scrollbar_button_hover_color

        self._label.configure(anchor="w")
        self._label.winfo_children()[1].configure(pady=0, anchor="w")
        self._label.winfo_children()[1].grid_configure(pady=0, sticky="nw")

        if self.button_command is not None:
            self.plus_image = ctk.CTkImage(
                light_image=Image.open(os.path.join(os.getcwd(), "images/light-plus.png")),
                dark_image=Image.open(os.path.join(os.getcwd(), "images/dark-plus.png")),
                size=(20, 20)
            )

            self.new_button = ctk.CTkButton(self._label,
                                            image=self.plus_image,
                                            text="",
                                            width=40,
                                            height=40,
                                            hover_color=BUTTON_HOVER_COLOR,
                                            fg_color="transparent",
                                            font=ctk.CTkFont(**SECONDARY_TITLE_FONT),
                                            border_width=2,
                                            border_color=SEPERATOR_COLOR,
                                            anchor="center",
                                            command=self.button_command)
            self.new_button.grid(row=0, column=1, sticky="w")

        self._label.rowconfigure(0, weight=1)
        self._label.columnconfigure(0, weight=1)
        self._label.columnconfigure(1, weight=0)


    def loading_frame(self):
        for i in self.winfo_children():
            i.destroy()

        loading_label = ctk.CTkLabel(self,
                                     fg_color="transparent",
                                     text="Loading...",
                                     font=ctk.CTkFont(**TITLE_FONT),
                                     anchor="center")
        loading_label.grid(row=0, column=0, sticky="nsew", pady=50)

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.check_scrollbar_needed()

    def build_frame(self):
        self.update_idletasks()

        for i in range(6):
            new_label = ctk.CTkLabel(
                self,
                height=80,
                text=f"Label {i}",
                fg_color="blue"
            )
            new_label.grid(row=i, column=0, sticky="ew", pady=(0, DEFAULT_PAD))

    def check_scrollbar_needed(self):
        self.update_idletasks()
        if self._parent_canvas.winfo_height() > self.winfo_height():
            current_fg = tuple(self.cget("fg_color"))
            self.configure(scrollbar_button_color=current_fg,
                           scrollbar_button_hover_color=current_fg)
        else:
            self.configure(scrollbar_button_color=self.scrollbar_color,
                           scrollbar_button_hover_color=self.scrollbar_hover_color)





