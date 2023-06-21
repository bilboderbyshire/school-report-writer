import customtkinter as ctk


def rgb_to_hex(rgb: tuple[int, int, int]) -> str:
    r_val = hex(rgb[0])[2::]
    if len(r_val) == 1:
        r_val = "0" + r_val

    g_val = hex(rgb[1])[2::]
    if len(g_val) == 1:
        g_val = "0" + g_val

    b_val = hex(rgb[2])[2::]
    if len(b_val) == 1:
        b_val = "0" + b_val

    return f"#{r_val}{g_val}{b_val}"


def find_tags_in_text(text: str, textbox: ctk.CTkTextbox, variable_tracker: dict[str, list[str]]) -> \
        dict[str, list[str]]:
    all_tags = textbox.tag_names()
    current_line = 1
    current_tag_start_index = -1
    current_tag_end_index = 0
    in_tag = False
    current_tag = ""
    for char in text:
        if char == "\n":
            current_line += 1
            current_tag_start_index = -1
            continue

        if textbox.tag_names(f"{current_line}.{current_tag_start_index + 1}"):
            current_tag_start_index += 1
        elif in_tag and char == "{":
            current_tag_end_index += 1
            current_tag_start_index = current_tag_end_index
            current_tag = char
        elif in_tag and char != "}":
            current_tag_end_index += 1
            current_tag += char
        elif char == "{":
            current_tag_start_index += 1
            current_tag_end_index = current_tag_start_index
            current_tag = char
            in_tag = True
        elif char == "}":
            current_tag += char
            current_tag_end_index += 1
            in_tag = False
            if ":" in current_tag:
                final_tag = current_tag.split(":")[0][1::]
            else:
                final_tag = current_tag[1:-1]
            if final_tag in all_tags:
                textbox.tag_add(
                    final_tag,
                    f"{current_line}.{current_tag_start_index}",
                    f"{current_line}.{current_tag_end_index + 1}")
                if final_tag in variable_tracker.keys():
                    variable_tracker[final_tag].append(current_tag)
                else:
                    variable_tracker[final_tag] = [current_tag]

            current_tag = ""
            current_tag_start_index = current_tag_end_index
            current_tag_end_index = 0
        else:
            current_tag_start_index += 1

    textbox.update()
    return variable_tracker
