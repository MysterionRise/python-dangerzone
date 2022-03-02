import glob
from pathlib import Path
from random import random
from typing import List

import matplotlib.pyplot as plt
import pandas as pd
from PIL import Image, ImageStat


def replace_white(im_file):
    directory = im_file.split("/")[1]
    file = im_file.split("/")[2]
    im = Image.open(im_file)
    width, height = im.size
    pixels = im.load()
    mean = 119
    std = 20
    # cnt = 0
    # white_cnt = 0
    # brightness = 140
    #
    # darkness_factor = 0.9
    mode = im.mode
    new_img = Image.new(mode, (width, height))
    new_pixels = new_img.load()
    print(pixels)
    print(pixels[0, 0])
    print(im_file)
    for x in range(width):
        for y in range(height):
            (r, g, b, *a) = pixels[x, y]
            l = luminocity(r, g, b)
            if random() > 0.0:
                if l < mean:
                    if len(a) == 1:
                        new_pixels[x, y] = (
                            r + r_component(std),
                            g + g_component(std),
                            b + b_component(std),
                            a[0]
                        )
                    else:
                        new_pixels[x, y] = (
                            r + r_component(std),
                            g + g_component(std),
                            b + b_component(std),
                        )
                else:
                    if len(a) == 1:
                        new_pixels[x, y] = (
                            r - r_component(std),
                            g - g_component(std),
                            b - b_component(std),
                            a[0],
                        )
                    else:
                        new_pixels[x, y] = (
                            r - r_component(std),
                            g - g_component(std),
                            b - b_component(std),
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


def stats_report(files: List[str]):
    list = []
    for f in files:
        data = distribution_of_luminocity(f)
        data_df = pd.DataFrame(data)
        if len(data_df.columns) == 0:
            print(f)
        dict = data_df.describe().to_dict()
        dict = dict[0]
        dict["name"] = f
        list.append(pd.Series(dict))
    df = pd.DataFrame(list)
    df.to_csv("result.csv")


def replace_white_with_alpha(im_file):
    directory = im_file.split("/")[1]
    file = im_file.split("/")[2]
    im = Image.open(im_file)
    width, height = im.size
    pixels = im.load()
    image = Image.new("RGBA", im.size)
    new_pixels = image.load()
    for x in range(width):
        for y in range(height):
            (r, g, b, *a) = pixels[x, y]
            if r >= 240 and g >= 240 and b >= 240:
                new_pixels[x, y] = (255, 255, 255, 0)
            else:
                new_pixels[x, y] = pixels[x, y]
    Path("targets/" + directory + "/").mkdir(parents=True, exist_ok=True)
    image.save("targets/" + directory + "/" + file)


def replace_alpha_with_white(file):
    directory = file.split("/")[1]
    file_name = file.split("/")[2]
    im = Image.open(file)
    image = Image.new("RGB", im.size, "WHITE")
    image.paste(im, (0, 0), im)
    Path("targets/" + directory + "/").mkdir(parents=True, exist_ok=True)
    image.save("targets/" + directory + "/" + file_name)


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
    plt.hist(total_lumi, density=True, bins=30)  # density=False would make counts
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
    # for f in glob.glob("replacement/*/*.png"):
    #     replace_white_with_alpha(f)
    # files = [f for f in glob.glob("targets1/*/*_400X400.png")]
    # stats_report(files)
    # for f in glob.glob("replacement/*/*.jpg"):
    #     replace_white(f)
    files = [f for f in glob.glob("EE_FM_RNF/*/*.png")]
    print(len(files))
    distribution_for_files(files)
    files = [f for f in glob.glob("EE_FM_RNF/*/*.png")]
    stats_report(files)
    # for f in glob.glob("replacement/*/*.png"):
    #     replace_alpha_with_white(f)
