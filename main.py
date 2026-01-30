# main.py
# == Import ===
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import random
import time
from datetime import datetime

time_start = time.time()

# === Value ===
# pos
SCALE = 1
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
ONOFF_LATTER = True
ONOFF_TEXT = True
ONOFF_CRICLE = False

ONOFF_SHOW = False
ONOFF_SAVE = True

# === Draw tools ===
img = Image.new("RGB", image_scale, COLOR_BG)
draw = ImageDraw.Draw(img)

font_size = int(235 * SCALE)
font = ImageFont.truetype("Fonts\\RussoOne-Regular.ttf", font_size)

bit_font_size = int(1500 * SCALE * BIG_TEXT_SCALE)
bit_font = ImageFont.truetype("Fonts\\RussoOne-Regular.ttf", bit_font_size)

# === BG Noise ===
if ONOFF_NOISE:
    small_size = int(SIDE_Y_SCALE * BG_PATER_SCALE)
    noise_img = Image.new("RGB", (small_size, small_size))
    noise_draw = ImageDraw.Draw(noise_img)

    for x in range(small_size):
        for y in range(small_size):
            r = random.randint(*R_LIMITS)
            g = random.randint(*G_LIMITS)
            b = random.randint(*B_LIMITS)
            noise_draw.point((x, y), fill=(r, g, b))

    bg_texture = noise_img.resize((SIDE_X_SCALE, SIDE_Y_SCALE), resample=Image.NEAREST)
    bg_texture = bg_texture.filter(ImageFilter.GaussianBlur(radius=20))
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
if ONOFF_LATTER:
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