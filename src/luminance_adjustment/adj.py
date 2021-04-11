import math
from random import randint

import matplotlib.pyplot as plt

from PIL import Image, ImageEnhance, ImageStat


def getRed(redVal):
    return '#%02x%02x%02x' % (redVal, 0, 0)


def getGreen(greenVal):
    return '#%02x%02x%02x' % (0, greenVal, 0)


def getBlue(blueVal):
    return '#%02x%02x%02x' % (0, 0, blueVal)


def replace_white(im_file):
    im = Image.open(im_file)
    width, height = im.size
    pixels = im.load()
    cnt = 0

    mode = im.mode
    new_img = Image.new(mode, (width, height))
    new_pixels = new_img.load()
    for x in range(width):
        for y in range(height):
            (r, g, b, *a) = pixels[x, y]
            if r > 230 and g > 230 and b > 230 and len(a) == 1 and a[0] != 0:
                # print("{} {}".format(x, y))
                cnt += 1
                new_pixels[x, y] = (randint(0, 255), randint(0, 255), randint(0, 255))
            else:
                new_pixels[x, y] = pixels[x, y]
    print(cnt)
    new_img.show()
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


def brightness(im_file):
    im = Image.open(im_file).convert('L')
    stat = ImageStat.Stat(im)
    return stat.mean[0], stat.rms[0]


def get_histogram(im_file):
    im = Image.open(im_file)
    histogram = im.histogram()
    # Take only the Red counts

    l1 = histogram[0:256]

    # Take only the Blue counts

    l2 = histogram[256:512]

    # Take only the Green counts

    l3 = histogram[512:768]

    plt.figure(0)

    # R histogram

    for i in range(0, 256):
        plt.bar(i, l1[i], color=getRed(i), edgecolor=getRed(i), alpha=0.3)

    # G histogram

    plt.figure(1)

    for i in range(0, 256):
        plt.bar(i, l2[i], color=getGreen(i), edgecolor=getGreen(i), alpha=0.3)

    # B histogram

    plt.figure(2)

    for i in range(0, 256):
        plt.bar(i, l3[i], color=getBlue(i), edgecolor=getBlue(i), alpha=0.3)

    plt.show()


if __name__ == '__main__':
    replace_white("images/1b.png")

    # print(brightness("images/1.jpg"))
    # print(brightness("images/2.jpg"))
    # print(brightness("images/3.png"))
    # print(brightness("images/4.png"))
    # print(brightness("images/5.png"))
    # print(brightness("images/6.jpg"))
    # print('--------------------------')
    # print(brightness("images/1a.png"))
    # print(brightness("images/2a.png"))
    # print(brightness("images/3a.png"))
    # print(brightness("images/4a.png"))
    # print(brightness("images/5a.png"))
    # print('--------------------------')
    # print(brightness("images/1b.png"))
    # print(brightness("images/2b.png"))
    # print(brightness("images/3b.png"))
    # print(brightness("images/4b.png"))
    # print(brightness("images/5b.png"))
