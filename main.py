import ctypes
from scripts import root

if __name__ == "__main__":
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
    app = root.ReportWriter()
    app.mainloop()
