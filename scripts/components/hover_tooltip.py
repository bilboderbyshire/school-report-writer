import tkinter as tk


class HoverTooltip(object):
    """
    create a tooltip for a given widget
    """
    def __init__(self,
                 widget: tk.Misc,
                 text: str = 'widget info',
                 text_variable: tk.StringVar = None,
                 wait_time: int = 800,
                 wrap_length: int = 180):
        self.wait_time = wait_time     # milliseconds
        self.wrap_length = wrap_length   # pixels
        self.widget = widget

        if text_variable is None:
            self.text_var = tk.StringVar(value=text)
        else:
            self.text_var = text_variable

        self.widget.bind("<Enter>", self.enter)
        self.widget.bind("<Leave>", lambda event: self.leave())
        self.widget.bind("<ButtonPress>", lambda event: self.leave())
        self.after_id = None
        self.tw = None

    def enter(self, event: tk.Event):
        self.schedule(event)

    def leave(self):
        self.unschedule()
        self.hidetip()

    def schedule(self, event: tk.Event):
        self.unschedule()
        self.after_id = self.widget.after(self.wait_time, self.showtip, event)

    def unschedule(self):
        current_id = self.after_id
        self.after_id = None
        if current_id:
            self.widget.after_cancel(current_id)

    def showtip(self, event: tk.Event):
        # x, y, cx, cy = self.widget.grid_bbox()
        # x += self.widget.winfo_rootx() + 25
        # y += self.widget.winfo_rooty() + 20

        x = event.x_root + 10
        y = event.y_root + 15
        # creates a toplevel window
        self.tw = tk.Toplevel(self.widget)
        # Leaves only the label and removes the app window
        self.tw.wm_overrideredirect(True)
        self.tw.wm_geometry("+%d+%d" % (x, y))
        label = tk.Label(self.tw,
                         textvariable=self.text_var,
                         justify='left',
                         background="#ffffff",
                         relief='solid',
                         borderwidth=1,
                         wraplength=self.wrap_length)
        label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tw
        self.tw = None
        if tw:
            tw.destroy()
