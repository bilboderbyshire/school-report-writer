import customtkinter as ctk
from ..settings import *


class AutohidingScrollableAndLoadingFrame(ctk.CTkScrollableFrame):
    def __init__(self, master,
                 scrollbar_button_color=STANDARD_SCROLLBAR_BUTTON_COLOR,
                 scrollbar_button_hover_color=STANDARD_SCROLLBAR_BUTTON_HOVER_COLOR,
                 **kwargs):

        super().__init__(master,
                         scrollbar_button_color=scrollbar_button_color,
                         scrollbar_button_hover_color=scrollbar_button_hover_color,
                         **kwargs)

        self.scrollbar_color = scrollbar_button_color
        self.scrollbar_hover_color = scrollbar_button_hover_color
        self._label.configure(padx=0, anchor="nw")
        # self._label.grid_configure(**DEFAULT_PAD_COMPLETE)

        self.loading_label = ctk.CTkLabel(self,
                                          fg_color="transparent",
                                          text="Loading...",
                                          font=ctk.CTkFont(**TITLE_FONT),
                                          anchor="center")

        self.loading_label.grid(row=0, column=0, sticky="nsew", pady=50)

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

    def build_frame(self):
        self.loading_label.destroy()
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





