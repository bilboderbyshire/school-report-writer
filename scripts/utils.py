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
