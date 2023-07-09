import os

import numpy as np
import pandas as pd
from PIL import Image

# Define image size and color
IMAGE_SIZE = (1770, 1770)
RGB_COLOR = (205, 205, 205)
IMAGES_BASE_PATH = "images"


def load_image(img_path, resize_percentage=None):
    img = Image.open(os.path.join(IMAGES_BASE_PATH, img_path + ".png")).convert("RGBA")
    if resize_percentage is not None:
        width, height = img.size
        new_size = (int(width * resize_percentage), int(height * resize_percentage))
        img = img.resize(new_size, Image.ANTIALIAS)
    return img


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

    for _, row in sheet.iterrows():
        output_file = row["pic_search"]
        middle_img_path = row["middle"]
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

        middle_img = load_image(middle_img_path)

        # Calculate position to place middle image at the center
        mid_pos = (
            (IMAGE_SIZE[0] - middle_img.width) // 2,
            (IMAGE_SIZE[1] - middle_img.height) // 2,
        )

        base_img = merge_images(base_img, middle_img, mid_pos)
        padding = 10
        for i, corner_img_path in enumerate(corner_img_paths):
            corner_img = load_image(corner_img_path, resize_percentage=0.75)
            pos_x = (IMAGE_SIZE[0] - corner_img.width - padding) if i % 2 else padding
            pos_y = (IMAGE_SIZE[1] - corner_img.height - padding) if i // 2 else padding
            base_img = merge_images(base_img, corner_img, (pos_x, pos_y))

        output_file_path = os.path.join(output_dir, output_file + ".png")
        os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
        base_img.save(output_file_path)


def process_excel_file(excel_path, output_dir):
    for sheet_name in ["Seq1_1", "Seq1_2", "Seq1_3", "Seq1_4"]:
        df = pd.read_excel(excel_path, sheet_name=sheet_name, engine="openpyxl")
        process_sequence(df, os.path.join(output_dir, sheet_name))


if __name__ == "__main__":
    excel_path = "sequences.xlsx"
    output_dir = "output"
    process_excel_file(excel_path, output_dir)
