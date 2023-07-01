import customtkinter as ctk
from ..settings import *
from ..title_bar import TitleLabel
from ..components import SecondaryButton
from ..containers import PupilInfo
import os


class AddManyToplevel(ctk.CTkToplevel):
    def __init__(self,
                 master):
        super().__init__(master,
                         fg_color=ROOT_BG)

        self.pupil_info: list[PupilInfo] | None = None

        self.update_idletasks()
        ws = self.winfo_screenwidth()
        hs = self.winfo_screenheight()

        x = int((ws / 2) - (LOGIN_WIDTH / 2))
        y = int((hs / 2) - (LOGIN_HEIGHT / 2)) - 100

        self.geometry(f"{LOGIN_GEOMETRY}+{x}+{y}")

        self.title("Add many...")

        # CTk.Toplevel source code applies default iconbitmap after 200ms (for some reason), this overrides any icon
        #  change made during initialisation of login window. This code overrides their override by rendering my icon
        #  50ms after theirs.
        self.after(250, lambda: self.iconbitmap(os.path.join(os.getcwd(), "images/app-logo.ico")))

        title_bar = TitleLabel(self,
                               "Add many...")
        title_bar.grid(row=0, column=0, sticky="w", pady=DEFAULT_PAD, padx=DEFAULT_PAD)

        info_label_text = "Type or paste a list of pupil information into the box below. Every pupil should be " \
                          "on a newline, and each piece of information should be seperated by a tab. You can" \
                          " paste directly from a spreadsheet.\n\nThe information has to be a forename, surname and " \
                          "a gender; either m for male, f for female, or nb for non-binary. This must be provided in " \
                          "the stated order eg: Sally\tHawkins\tF."

        self.info_label = ctk.CTkLabel(
            self,
            text=info_label_text,
            fg_color="transparent",
            font=ctk.CTkFont(**VERY_SMALL_FONT),
            wraplength=LOGIN_WIDTH - (DEFAULT_PAD * 2),
            anchor="w",
            justify="left"
        )
        self.info_label.grid(row=1, column=0, sticky="nsew", padx=DEFAULT_PAD, pady=(0, DEFAULT_PAD))

        self.info_label.bind("<Configure>", lambda event: self.configure_info_label())

        self.paste_box = ctk.CTkTextbox(
            self,
            fg_color="transparent",
            border_width=2,
            wrap="word",
            height=10,
            undo=True,
        )
        self.paste_box.grid(row=2, column=0, sticky="nsew", padx=DEFAULT_PAD, pady=(0, DEFAULT_PAD))
        self.paste_box.tag_config("error", foreground=BAD_COLOR)

        self.paste_box.bind("<KeyRelease>", lambda event: self.check_save_possible())

        button_frame = ctk.CTkFrame(self, fg_color="transparent")
        button_frame.grid(row=3, column=0, sticky="nsew", padx=DEFAULT_PAD, pady=(0, DEFAULT_PAD))
        button_frame.rowconfigure(0, weight=0)
        button_frame.columnconfigure([0, 1, 2], weight=1, uniform="column")

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

        self.rowconfigure([0, 1, 3], weight=0)
        self.rowconfigure(2, weight=1)
        self.columnconfigure(0, weight=1)

        self.grab_set()
        self.after(10, self.paste_box.focus_set)
        self.wait_window()

    def configure_info_label(self):
        self.info_label.update_idletasks()
        self.info_label.configure(wraplength=self.info_label._current_width)

    def check_save_possible(self):
        current_paste_box = self.paste_box.get("1.0", "end").strip()

        if current_paste_box == "":
            self.save_button.configure(state="disabled")
        else:
            self.save_button.configure(state="normal")

    def cancel_clicked(self):
        self.pupil_info = None
        self.destroy()

    def save_clicked(self):
        current_paste_box = self.paste_box.get("1.0", "end").strip()
        error_free = True
        temp_list = []
        for index, pupil in enumerate(current_paste_box.split("\n")):
            raw_pupil_info = pupil.split("\t")

            if len(raw_pupil_info) != 3:
                self.paste_box.tag_add("error", f"{index+1}.0", f"{index+1}.end")
                error_free = False
            elif raw_pupil_info[2].lower() not in ["m", "f", "nb"]:
                self.paste_box.tag_add("error", f"{index+1}.0", f"{index+1}.end")
                error_free = False
            else:
                self.paste_box.tag_remove("error", f"{index+1}.0", f"{index+1}.end")
                new_pupil: PupilInfo = {
                    "forename": raw_pupil_info[0].lower().strip(),
                    "surname": raw_pupil_info[1].lower().strip(),
                    "gender": raw_pupil_info[2].lower().strip()
                }
                temp_list.append(new_pupil)

        if error_free:
            self.pupil_info = temp_list
            self.destroy()
        else:
            self.pupil_info = None

    def get_pupil_info(self) -> list[PupilInfo]:
        return self.pupil_info
