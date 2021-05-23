import glob
import math
from pathlib import Path
from random import random
from typing import List

import matplotlib.pyplot as plt
import pandas as pd
from PIL import Image, ImageEnhance, ImageStat


def replace_white(im_file):
    directory = im_file.split("/")[1]
    file = im_file.split("/")[2]
    im = Image.open(im_file)
    width, height = im.size
    pixels = im.load()
    mean = 119
    std = 10
    # cnt = 0
    # white_cnt = 0
    # brightness = 140
    #
    # darkness_factor = 0.9
    mode = im.mode
    new_img = Image.new(mode, (width, height))
    new_pixels = new_img.load()
    for x in range(width):
        for y in range(height):
            (r, g, b, *a) = pixels[x, y]
            l = luminocity(r, g, b)
            if random() > 0.5:
                if l < mean:
                    new_pixels[x, y] = (
                        r + r_component(std),
                        g + g_component(std),
                        b + b_component(std),
                        a[0],
                    )
                else:
                    new_pixels[x, y] = (
                        r - r_component(std),
                        g - g_component(std),
                        b - b_component(std),
                        a[0],
                    )
            else:
                new_pixels[x, y] = pixels[x, y]
            # if r >= 250 and g >= 250 and b >= 250:
            #     white_cnt += 1
            #     new_pixels[x, y] = (r, g, b, 0)
            # if r > brightness or g > brightness or b > brightness and len(a) == 1 and a[0] != 0:
            #     # print("{} {}".format(x, y))
            #     cnt += 1
            #     new_pixels[x, y] = (int(r * darkness_factor), int(g * darkness_factor), int(b * darkness_factor), a[0])
            # else:
            #     new_pixels[x, y] = pixels[x, y]
    # print(white_cnt)
    # stat = ImageStat.Stat(new_img)
    # print("{},{}".format(directory + "/" + file, (stat.mean[0], stat.rms[0])))
    Path("targets/" + directory + "/").mkdir(parents=True, exist_ok=True)
    new_img.save("targets/" + directory + "/" + file)
    # new_img.show()
    # width, height = (1200, 800)
    # mode = 'RGB'
    # my_image = Image.new(mode, (width, height))
    #
    # # Load all the pixels.
    # my_pixels = my_image.load()
    #
    # # Loop through all the pixels, and set each color randomly.
    # for x in range(width):
    #     for y in range(height):
    #         r = randint(0, 255)
    #         g = randint(0, 255)
    #         b = randint(0, 255)
    #         pixel = (r, g, b)
    #         my_pixels[x, y] = pixel
    #
    # my_image.show()


def luminocity(r: int, g: int, b: int) -> float:
    return (0.21 * r) + (0.72 * g) + (0.07 * b)


def r_component(value: int) -> int:
    # return int(0.21 * value)
    return value


def g_component(value: int) -> int:
    # return int(0.72 * value)
    return value


def b_component(value: int) -> int:
    # return int(0.07 * value)
    return value


def distribution_for_files(files: List[str]):
    total_lumi = []
    for f in files:
        total_lumi.extend(distribution_of_luminocity(f))
    df = pd.DataFrame(total_lumi)
    print(df.describe())
    plt.hist(
        total_lumi, density=True, bins=30
    )  # density=False would make counts
    plt.ylabel("Probability")
    plt.xlabel("Data")
    plt.show()


def distribution_of_luminocity(im_file):
    im = Image.open(im_file)
    width, height = im.size
    pixels = im.load()
    all_lumi = []
    for x in range(width):
        for y in range(height):
            (r, g, b, *a) = pixels[x, y]
            if len(a) == 1 and a[0] != 0:
                all_lumi.append(luminocity(r, g, b))
    return all_lumi


def brightness(im_file):
    im = Image.open(im_file).convert("L")
    stat = ImageStat.Stat(im)
    return stat.mean[0], stat.rms[0]


if __name__ == "__main__":

    # files = [f for f in glob.glob("prepared_for_cleaning/*/*.png")]
    for f in glob.glob("prepared_for_cleaning/*/*.png"):
        replace_white(f)
    files = [f for f in glob.glob("targets/*/*.png")]
    print(len(files))
    distribution_for_files(files)
