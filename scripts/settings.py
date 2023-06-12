# Database settings

URL = 'https://report-writer.pockethost.io'

# Root settings

WIDTH = 1000
HEIGHT = 600
GEOMETRY = f"{WIDTH}x{HEIGHT}"
WINDOW_TITLE = "School Report Writer"
DEFAULT_PAD = 10
DEFAULT_PAD_COMPLETE = {
    "padx": DEFAULT_PAD,
    "pady": DEFAULT_PAD
}

# Login toplevel settings
LOGIN_WIDTH = 400
LOGIN_HEIGHT = 500
LOGIN_GEOMETRY = f"{LOGIN_WIDTH}x{LOGIN_HEIGHT}"

# Frame settings
SMALL_PAD = 5
SMALL_PAD_COMPLETE = {
    "padx": SMALL_PAD,
    "pady": SMALL_PAD
}

# Fonts

TITLE_FONT = {"family": "Segoe UI",
              "size": 30,
              "weight": "bold"}

SECONDARY_TITLE_FONT = {"family": "Segoe UI",
                        "size": 23,
                        "weight": "bold"}

ENTRY_FONT = {"family": "Segoe UI",
              "size": 17}

NORMAL_LABEL_FONT = {"family": "Segoe UI",
                     "size": 16,
                     "weight": "bold"}

SMALL_LABEL_FONT = {"family": "Segoe UI",
                    "size": 14}

# Colours

ROOT_BG = ("#EAEBEB", "#23272D")
STANDARD_TEXT_COLOR = ("#242424", "#D6D6D6")
BUTTON_HOVER_COLOR = "#969696"
LABEL_BUTTON_TEXT_COLOR = "#202EC8"
ERROR_TEXT_COLOR = ("#FE2525", "#9E2927")
SECONDARY_BUTTON_FG_COLOR = ("#D9DCE0", "#60676F")
SECONDARY_BUTTON_HOVER_COLOR = ("#AFB2B6", "#4C4E54")
SECONDARY_BUTTON_TEXT_COLOR = ("#242424", "#DCE4EE")
STANDARD_SCROLLBAR_BUTTON_COLOR = ("gray55", "gray41")
STANDARD_SCROLLBAR_BUTTON_HOVER_COLOR = ("gray40", "gray53")
LABEL_CARD_COLOR = ("#F9F9F9", "#2F333A")
LABEL_CARD_HOVER_COLOR = ("#C9C9C9", "#282D34")

NOT_COMPLETED_COLOR = (166, 61, 58)
ALMOST_COMPLETED_COLOR = (166, 158, 46)
COMPLETED_COLOR = (69, 161, 22)
PROGRESS_BAR_BASE_COLOR = ("#DADADA", "#4A4D50")
