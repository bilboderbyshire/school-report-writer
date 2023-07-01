import customtkinter as ctk
from ..settings import *
from ..title_bar import TitleLabel
from ..components import SingleLineEntry, NormalLabel, SecondaryButton, LargeOptionMenu
from ..containers import PupilInfo
import os


class AddOneToplevel(ctk.CTkToplevel):
    def __init__(self,
                 master):
        super().__init__(master,
                         fg_color=ROOT_BG)

        self.pupil_info: PupilInfo | None = None

        self.update_idletasks()
        ws = self.winfo_screenwidth()
        hs = self.winfo_screenheight()

        x = int((ws / 2) - (LOGIN_WIDTH / 2))
        y = int((hs / 2) - (LOGIN_HEIGHT / 2)) - 100

        self.geometry(f"{LOGIN_GEOMETRY}+{x}+{y}")

        self.title("Add one...")

        # CTk.Toplevel source code applies default iconbitmap after 200ms (for some reason), this overrides any icon
        #  change made during initialisation of login window. This code overrides their override by rendering my icon
        #  50ms after theirs.
        self.after(250, lambda: self.iconbitmap(os.path.join(os.getcwd(), "images/app-logo.ico")))

        title_bar = TitleLabel(self,
                               "Add one...")
        title_bar.grid(row=0, column=0, sticky="w", pady=(DEFAULT_PAD, 35), padx=DEFAULT_PAD)

        name_entry_frame = ctk.CTkFrame(self, fg_color="transparent")
        name_entry_frame.grid(row=1, column=0, sticky="nsew", padx=DEFAULT_PAD, pady=(0, DEFAULT_PAD))
        name_entry_frame.rowconfigure([0, 1], weight=0)
        name_entry_frame.columnconfigure([0, 1], weight=1, uniform="columns")

        forename_entry_label = NormalLabel(name_entry_frame, text="Forename")
        forename_entry_label.grid(row=0, column=0, sticky="w", padx=(0, SMALL_PAD), pady=(0, SMALL_PAD))

        self.forename_entry = SingleLineEntry(name_entry_frame)
        self.forename_entry.grid(row=1, column=0, sticky="ew", padx=(0, SMALL_PAD))

        surname_entry_label = NormalLabel(name_entry_frame, text="Surname")
        surname_entry_label.grid(row=0, column=1, sticky="w", pady=(0, SMALL_PAD))

        self.surname_entry = SingleLineEntry(name_entry_frame)
        self.surname_entry.grid(row=1, column=1, sticky="ew")

        self.gender_entry = LargeOptionMenu(
            self,
            values=["M", "F", "NB"],
            height=40,
            command=self.check_save_possible
        )
        self.gender_entry.grid(row=2, column=0, sticky="nsew", padx=DEFAULT_PAD, pady=(0, DEFAULT_PAD))
        self.gender_entry.set("Select pupils' gender...")

        blank_frame = ctk.CTkFrame(self, fg_color="transparent")
        blank_frame.grid(row=3, column=0, sticky="nsew")

        button_frame = ctk.CTkFrame(self, fg_color="transparent")
        button_frame.grid(row=4, column=0, sticky="nsew", padx=DEFAULT_PAD, pady=(0, DEFAULT_PAD))
        button_frame.rowconfigure(0, weight=0)
        button_frame.columnconfigure([0, 1, 2], weight=1, uniform="columns")

        self.save_button = ctk.CTkButton(
            button_frame,
            text="Save",
            font=ctk.CTkFont(**NORMAL_LABEL_FONT),
            command=self.save_clicked,
            state="disabled"
        )

        self.save_button.grid(row=0, column=1, sticky="nsew", padx=(0, SMALL_PAD))

        cancel_button = SecondaryButton(
            button_frame,
            text="Cancel",
            font=ctk.CTkFont(**NORMAL_LABEL_FONT),
            command=self.cancel_clicked
        )
        cancel_button.grid(row=0, column=2, sticky="nsew")

        self.forename_entry.bind("<KeyPress>", lambda event: self.check_save_possible(event))
        self.surname_entry.bind("<KeyPress>", lambda event: self.check_save_possible(event))

        self.rowconfigure([0, 1, 2, 4], weight=0)
        self.rowconfigure(3, weight=1)
        self.columnconfigure(0, weight=1)

        self.grab_set()
        self.after(10, self.forename_entry.focus_set)
        self.wait_window()

    def check_save_possible(self, _):
        if self.forename_entry.get() != "" \
                and self.surname_entry.get() != "" \
                and self.gender_entry.get() != "Select pupils' gender...":
            self.save_button.configure(state="normal")
        else:
            self.save_button.configure(state="disabled")

    def save_clicked(self):
        self.pupil_info: PupilInfo = {
            "forename": self.forename_entry.get().lower().strip(),
            "surname": self.surname_entry.get().lower().strip(),
            "gender": self.gender_entry.get().lower()
        }
        self.destroy()

    def cancel_clicked(self):
        self.destroy()
        self.pupil_info = None

    def get_pupil_info(self) -> PupilInfo:
        return self.pupil_info
