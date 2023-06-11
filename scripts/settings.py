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


# Fonts

TITLE_FONT = {"family": "Segoe UI",
              "size": 30,
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
BUTTON_HOVER_COLOR = "#969696"
LABEL_BUTTON_TEXT_COLOR = "#202EC8"
ERROR_TEXT_COLOR = ("#FE2525", "#9E2927")
