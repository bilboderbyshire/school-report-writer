import customtkinter as ctk
from ..settings import *
from ..title_bar import TitleLabel
from ..components import SingleLineEntry, NormalLabel, SecondaryButton, LargeOptionMenu
from .add_one_top_level import AddOneToplevel
import os
from PIL import Image


class ReportSetupToplevel(ctk.CTkToplevel):
    def __init__(self,
                 master,
                 template_selectable: bool = True):
        super().__init__(master,
                         fg_color=ROOT_BG)

        self.template_selectable = template_selectable

        self.update_idletasks()
        ws = self.winfo_screenwidth()
        hs = self.winfo_screenheight()

        x = int((ws / 2) - (VARIABLE_TOPLEVEL_WIDTH / 2))
        y = int((hs / 2) - (VARIABLE_TOPLEVEL_HEIGHT / 2)) - 100

        self.geometry(f"{VARIABLE_TOPLEVEL_GEOMETRY}+{x}+{y}")

        self.title("Setup report")

        # CTk.Toplevel source code applies default iconbitmap after 200ms (for some reason), this overrides any icon
        #  change made during initialisation of login window. This code overrides their override by rendering my icon
        #  50ms after theirs.
        self.after(250, lambda: self.iconbitmap(os.path.join(os.getcwd(), "images/app-logo.ico")))

        title_bar = TitleLabel(self,
                               "Setup report")
        title_bar.grid(row=0, column=0, sticky="w", pady=(DEFAULT_PAD, 35), padx=DEFAULT_PAD)

        report_name_entry_label = NormalLabel(
            self,
            anchor="sw",
            text="Report name"
        )
        report_name_entry_label.grid(row=1, column=0, sticky="ew", pady=(0, DEFAULT_PAD), padx=DEFAULT_PAD)

        self.report_name_entry = SingleLineEntry(
            self,
            placeholder_text="Eg, Form Report 2023"
        )
        self.report_name_entry.grid(row=2, column=0, sticky="ew", pady=(0, DEFAULT_PAD), padx=DEFAULT_PAD)

        class_entry_label = NormalLabel(
            self,
            anchor="sw",
            text="Class name"
        )
        class_entry_label.grid(row=3, column=0, sticky="ew", pady=(0, DEFAULT_PAD), padx=DEFAULT_PAD)

        self.class_entry = SingleLineEntry(
            self,
            placeholder_text="Eg, 10x/cs1"
        )
        self.class_entry.grid(row=4, column=0, sticky="ew", pady=(0, DEFAULT_PAD), padx=DEFAULT_PAD)

        self.template_selection = LargeOptionMenu(
            self,
            height=40,
            values=["hi", "there", "bye"]
        )
        self.template_selection.grid(row=5, column=0, sticky="ew", pady=(0, DEFAULT_PAD), padx=DEFAULT_PAD)
        self.template_selection.set("Choose template...")

        if not self.template_selectable:
            self.template_selection.configure(state="disabled")

        pupils_label_and_action_frame = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )
        pupils_label_and_action_frame.grid(row=6, column=0, sticky="nsew", pady=(0, DEFAULT_PAD), padx=DEFAULT_PAD)
        pupils_label_and_action_frame.rowconfigure(0, weight=0)
        pupils_label_and_action_frame.columnconfigure(0, weight=1)
        pupils_label_and_action_frame.columnconfigure([1, 2], weight=0)

        pupils_label = ctk.CTkLabel(
            pupils_label_and_action_frame,
            font=ctk.CTkFont(**SECONDARY_TITLE_FONT),
            fg_color="transparent",
            anchor="w",
            text="Pupils"
        )
        pupils_label.grid(row=0, column=0, sticky="nsew", padx=(0, SMALL_PAD))

        add_one_image = ctk.CTkImage(
            light_image=Image.open(os.path.join(os.getcwd(), "images/light-add-one.png")),
            dark_image=Image.open(os.path.join(os.getcwd(), "images/dark-add-one.png")),
            size=(15, 15)
        )
        add_one_button = ctk.CTkButton(
            pupils_label_and_action_frame,
            fg_color="transparent",
            image=add_one_image,
            command=self.add_one_clicked,
            text="",
            width=25,
            height=25,
            hover_color=BUTTON_HOVER_COLOR,
            corner_radius=5
        )

        add_one_button.grid(row=0, column=1, sticky="e", padx=(0, SMALL_PAD))

        add_many_image = ctk.CTkImage(
            light_image=Image.open(os.path.join(os.getcwd(), "images/light-add-many.png")),
            dark_image=Image.open(os.path.join(os.getcwd(), "images/dark-add-many.png")),
            size=(15, 15)
        )
        add_many_button = ctk.CTkButton(
            pupils_label_and_action_frame,
            fg_color="transparent",
            image=add_many_image,
            command=lambda: print("Add many"),
            text="",
            width=25,
            height=25,
            hover_color=BUTTON_HOVER_COLOR,
            corner_radius=5
        )

        add_many_button.grid(row=0, column=2, sticky="e")

        self.pupils_in_report = ctk.CTkFrame(self)
        self.pupils_in_report.grid(row=7, column=0, sticky="nsew", pady=(0, DEFAULT_PAD), padx=DEFAULT_PAD)

        save_report_frame = ctk.CTkFrame(self, fg_color="transparent")
        save_report_frame.grid(row=8, column=0, sticky="nsew", pady=(0, DEFAULT_PAD), padx=DEFAULT_PAD)
        save_report_frame.rowconfigure(0, weight=0)
        save_report_frame.columnconfigure([0, 1, 2, 3], weight=1, uniform="columns")

        save_button = ctk.CTkButton(
            save_report_frame,
            text="Save",
            font=ctk.CTkFont(**NORMAL_LABEL_FONT),
            command=lambda: print("Saved")
        )
        save_button.grid(row=0, column=2, sticky="nsew", padx=(0, SMALL_PAD))

        cancel_button = SecondaryButton(
            save_report_frame,
            text="Cancel",
            font=ctk.CTkFont(**NORMAL_LABEL_FONT),
            command=lambda: print("Cancelled")
        )
        cancel_button.grid(row=0, column=3, sticky="nsew")

        self.rowconfigure([0, 1, 2, 3, 4, 5, 6, 8], weight=0)
        self.rowconfigure(7, weight=1)
        self.columnconfigure(0, weight=1)

        self.grab_set()
        self.after(10, self.report_name_entry.focus_set)
        self.wait_window()

    def add_one_clicked(self):
        add_one_tl = AddOneToplevel(self)

        pupil_info = add_one_tl.get_pupil_info()
        print(pupil_info)
        self.grab_set()
        self.grab_release()

