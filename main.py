# main.py
# == Import ===
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import time
import numpy as np

time_start = time.time()

# === Value ===
# pos
SCALE = 5
BG_PATER_SCALE = 0.1
SIDE_Y_SCALE = int(2048 * SCALE)
SIDE_X_SCALE = int(2048 * SCALE)
CENTER_X = SIDE_X_SCALE // 2
CENTER_Y = SIDE_Y_SCALE // 2

# text
TEXT_MAIN = "SnehulakTV_"

# color
COLOR_BG = (25, 25, 25)
COLOR_1 = (255, 0, 0)
COLOR_TEXT_SHADOW = (150, 150, 150)
COLOR_TEXT = (255, 255, 255)
image_scale = (SIDE_X_SCALE, SIDE_Y_SCALE)

R_LIMITS = (20, 50)
G_LIMITS = (20, 50)
B_LIMITS = (20, 50)

# often change
app = {
    "ig": True,
    "git": False,
    "discord": False,
    "osu": False
}
if True:
    if app["ig"]:
        R_LIMITS = (25, 50)
        G_LIMITS = (10, 30)
        B_LIMITS = (20, 40)
        COLOR_TEXT_BIG_SHADOW = (180, 0, 100)
        COLOR_TEXT_BIG = (220, 0, 150)
        TEXT_BIG = "INSTA"
        BIG_TEXT_SCALE = 0.38
    elif app["git"]:
        R_LIMITS = (20, 50)
        G_LIMITS = (20, 50)
        B_LIMITS = (20, 50)
        COLOR_TEXT_BIG_SHADOW = (200, 200, 200)
        COLOR_TEXT_BIG = (225, 225, 225)
        TEXT_BIG = "GIT"
        BIG_TEXT_SCALE = 0.6
    elif app["discord"]:
        R_LIMITS = (0, 0)
        G_LIMITS = (0, 0)
        B_LIMITS = (20, 60)
        COLOR_TEXT_BIG_SHADOW = (5, 0, 100)
        COLOR_TEXT_BIG = (15, 0, 200)
        TEXT_BIG = "DISC"
        BIG_TEXT_SCALE = 0.49
    elif app["osu"]:
        R_LIMITS = (40, 70)
        G_LIMITS = (0, 0)
        B_LIMITS = (20, 40)
        COLOR_TEXT_BIG_SHADOW = (200, 0, 100) 
        COLOR_TEXT_BIG = (250, 0, 169) 
        TEXT_BIG = "OSU"
        BIG_TEXT_SCALE = 0.54

file_name = f"0/Picture-{TEXT_BIG}"

# to add
ONOFF_ADD_IMAGE_OSU = False
ONOFF_NOISE = True
ONOFF_LETTER = True
ONOFF_TEXT = True
ONOFF_CRICLE = False

ONOFF_SHOW = True
ONOFF_SAVE = False

# === Draw tools ===
img = Image.new("RGB", image_scale, COLOR_BG)
draw = ImageDraw.Draw(img)

font_size = int(235 * SCALE)
font = ImageFont.truetype("Fonts\\RussoOne-Regular.ttf", font_size)

bit_font_size = int(1500 * SCALE * BIG_TEXT_SCALE)
bit_font = ImageFont.truetype("Fonts\\RussoOne-Regular.ttf", bit_font_size)

# === BG Noise ===
if ONOFF_NOISE:
    small_size = int(204.8)

    # 2. Rychlé generování šumu (NumPy)
    noise_array = np.random.randint(
        [R_LIMITS[0], G_LIMITS[0], B_LIMITS[0]],
        [R_LIMITS[1] + 1, G_LIMITS[1] + 1, B_LIMITS[1] + 1],
        (small_size, small_size, 3), 
        dtype=np.uint8
    )
    noise_img = Image.fromarray(noise_array)


    noise_img = noise_img.filter(ImageFilter.GaussianBlur(radius=2))
    bg_texture = noise_img.resize((SIDE_X_SCALE, SIDE_Y_SCALE), resample=Image.BILINEAR)
    
    img.paste(bg_texture)

# === Add image (osu!) ===
if ONOFF_ADD_IMAGE_OSU:
    add_img_size_x = int(SIDE_X_SCALE / 11 * 6)
    add_img_size_y = int(SIDE_Y_SCALE / 11 * 6)
    add_img_pos_x = int(CENTER_X - add_img_size_x // 2)
    add_img_pos_y = int(CENTER_Y - add_img_size_y // 4 * 3)

    add_img = Image.open("Icon/osu.png").convert("RGBA")
    add_img_size = add_img.resize((add_img_size_x, add_img_size_y), resample=Image.LANCZOS)

    logo_color = (250, 0, 169) 
    colored_layer = Image.new("RGB", (add_img_size_x, add_img_size_y), logo_color)

    img.paste(colored_layer, (add_img_pos_x, add_img_pos_y), add_img_size)

# === Draw Text (latter) ===
if ONOFF_LETTER:
    text_pos_x = CENTER_X
    text_pos_y = int(SIDE_Y_SCALE // 8 * 3)

    shatow_text_offset = (15 * SCALE)
    shatow_text_pos_x = int(text_pos_x + shatow_text_offset)
    shatow_text_pos_y = int(text_pos_y + shatow_text_offset)

    draw.text((shatow_text_pos_x, shatow_text_pos_y), TEXT_BIG, font=bit_font, fill=COLOR_TEXT_BIG_SHADOW, anchor="mm")
    draw.text((text_pos_x, text_pos_y), TEXT_BIG, font=bit_font, fill=COLOR_TEXT_BIG, anchor="mm")

# === Draw Text (Main) ===
if ONOFF_TEXT:
    text_pos_x = CENTER_X
    text_pos_y = int(SIDE_Y_SCALE // 4 * 3)

    shatow_text_offset = (15 * SCALE)
    shatow_text_pos_x = int(text_pos_x + shatow_text_offset)
    shatow_text_pos_y = int(text_pos_y + shatow_text_offset)

    draw.text((shatow_text_pos_x, shatow_text_pos_y), TEXT_MAIN, font=font, fill=COLOR_TEXT_SHADOW, anchor="mm")
    draw.text((text_pos_x, text_pos_y), TEXT_MAIN, font=font, fill=COLOR_TEXT, anchor="mm")

# === Draw Cricle ===
if ONOFF_CRICLE:
    ellipse_pos_x = CENTER_X
    ellipse_pos_y = CENTER_Y

    draw.ellipse([0, 0, SIDE_X_SCALE, SIDE_Y_SCALE], fill=None, outline=(255, 255, 255), width=1)

# === Save ===
if ONOFF_SHOW:
    img.show()

if ONOFF_SAVE:
    img.save(f"Save/{file_name}.png")

time_end = time.time()

print(f" - Done - in {time_end - time_start}s")