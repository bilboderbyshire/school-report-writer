import customtkinter as ctk
from .settings import *
from PIL import Image
import os
from .components import TitleLabel


def change_theme():
    """
    This function changes the theme of the app, is called by the button on the title bar
    """

    if ctk.get_appearance_mode() == "Dark":
        ctk.set_appearance_mode("light")
    else:
        ctk.set_appearance_mode("dark")


class TitleBar(ctk.CTkFrame):
    """
    The title bar that is present in every frame, the text in the title can be changed by a given method
    """
    def __init__(self, master, title_text, refresh_command=None):
        super().__init__(master,
                         fg_color="transparent")

        # The label containing the text that explains what the current scene is showing
        self.title_label = TitleLabel(self,
                                      title_text)

        self.title_label.grid(row=0, column=0, sticky="nsew", pady=DEFAULT_PAD)

        # The image within the theme change button
        self.theme_image = ctk.CTkImage(
            light_image=Image.open(os.path.join(os.getcwd(), "images/dark-theme.png")),
            dark_image=Image.open(os.path.join(os.getcwd(), "images/light-theme.png")),
            size=(30, 30)
        )

        # The button that changes the theme when clicked
        self.theme_button = ctk.CTkButton(
            self,
            fg_color="transparent",
            image=self.theme_image,
            command=change_theme,
            text="",
            width=45,
            height=45,
            hover_color=BUTTON_HOVER_COLOR,
            corner_radius=8
        )
        self.theme_button.grid(row=0, column=2, sticky="e", pady=DEFAULT_PAD)

        self.command = refresh_command

        if self.command is not None:
            self.refresh_image = ctk.CTkImage(
                light_image=Image.open(os.path.join(os.getcwd(), "images/light-refresh.png")),
                dark_image=Image.open(os.path.join(os.getcwd(), "images/dark-refresh.png")),
                size=(30, 30)
            )

            self.refresh_button = ctk.CTkButton(
                self,
                fg_color="transparent",
                image=self.refresh_image,
                command=self.command,
                text="",
                width=45,
                height=45,
                hover_color=BUTTON_HOVER_COLOR,
                corner_radius=8
            )

            self.refresh_button.grid(row=0, column=1, sticky="e", **DEFAULT_PAD_COMPLETE)

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure([1, 2], weight=0)
