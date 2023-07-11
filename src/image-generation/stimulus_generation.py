import itertools
import os

import numpy as np
import pandas as pd
from PIL import Image, ImageDraw, ImageFont

# Define image size and color
IMAGE_SIZE = (1770, 1770)
RGB_COLOR = (205, 205, 205)
IMAGES_BASE_PATH = "images"
FONT_PATH = "/Library/Fonts/Arial Unicode.ttf"
FONT_SIZE = 125


def merge_images(base_img, img_to_merge, position):
    # Create a new image filled with the desired background color
    img_with_background = Image.new("RGBA", img_to_merge.size, RGB_COLOR)
    # Paste the image to merge onto the background image
    img_with_background.paste(img_to_merge, mask=img_to_merge)
    # Paste the resulting image onto the base image
    base_img.paste(img_with_background, position)
    return base_img


def process_sequence(sheet, output_dir):
    base_img_array = np.full(
        (IMAGE_SIZE[1], IMAGE_SIZE[0], 3), RGB_COLOR, dtype=np.uint8
    )
    base_img = Image.fromarray(base_img_array)

    for _, row in itertools.islice(sheet.iterrows(), 128):
        output_file = row["pic_search"]
        middle_img_path = row["middle"]

        middle_img = load_image(middle_img_path)

        # Calculate position to place middle image at the center
        mid_pos = (
            (IMAGE_SIZE[0] - middle_img.width) // 2,
            (IMAGE_SIZE[1] - middle_img.height) // 2,
        )

        base_img = merge_images(base_img, middle_img, mid_pos)
        padding = 10
        if "coll1" in sheet.columns:
            corner_img_paths = [
                str(row["coll1"]),
                str(row["coll2"]),
                str(row["coll3"]),
                str(row["coll4"]),
            ]

            # If any path ends with ".0" (because it was read as a float), remove it
            corner_img_paths = [
                path[:-2] if path.endswith(".0") else path for path in corner_img_paths
            ]

            for i, corner_img_path in enumerate(corner_img_paths):
                corner_img = load_image(corner_img_path, resize_percentage=0.75)
                pos_x = (
                    (IMAGE_SIZE[0] - corner_img.width - padding) if i % 2 else padding
                )
                pos_y = (
                    (IMAGE_SIZE[1] - corner_img.height - padding) if i // 2 else padding
                )
                base_img = merge_images(base_img, corner_img, (pos_x, pos_y))

        output_file_path = os.path.join(output_dir, output_file + ".png")
        os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
        base_img.save(output_file_path)


def process_excel_file(excel_path, output_dir):
    for sheet_name in [
        "Seq1_4",
        "Seq1_5",
        "Seq1_6",
        "Seq1_7",
        "Seq1_8",
        "Seq1_9",
        "Seq1_10",
        "Seq1_11",
    ]:
        df = pd.read_excel(excel_path, sheet_name=sheet_name, engine="openpyxl")
        process_sequence(df, os.path.join(output_dir, sheet_name))


def draw_text(text, font_path, font_size):
    img = Image.new("RGBA", IMAGE_SIZE, RGB_COLOR)
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(font_path, font_size)

    # Calculate the width and height of the text to be drawn, to center it
    w, h = draw.textsize(text, font=font)
    x = (img.width - w) // 2
    y = (img.height - h) // 2

    # Draw the text
    draw.text((x, y), text, fill="black", font=font)

    return img


def load_image(img_path, resize_percentage=None):
    if img_path.isupper() and len(img_path) == 5:  # If the img_path is a 5-letter word
        return draw_text(img_path, FONT_PATH, FONT_SIZE)

    img = Image.open(os.path.join(IMAGES_BASE_PATH, img_path + ".png")).convert("RGBA")
    if resize_percentage is not None:
        width, height = img.size
        new_size = (int(width * resize_percentage), int(height * resize_percentage))
        img = img.resize(new_size, Image.ANTIALIAS)
    return img


if __name__ == "__main__":
    excel_path = "sequences2.xlsx"
    output_dir = "output"
    process_excel_file(excel_path, output_dir)
