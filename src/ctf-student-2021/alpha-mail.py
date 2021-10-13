import requests
from PIL import Image

LOGIN = "dsfhsdjkfas"
PWD = "dfjsdkfjsdfksdf"

COLOUR_1 = (240, 146, 132)
COLOUR_2 = (168, 251, 152)
COLOUR_3 = (153, 157, 248)
COLOUR_4 = (241, 160, 250)
COLOUR_5 = (154, 154, 154)

COLOUR_12 = (151, 188, 94)
COLOUR_23 = (105, 153, 188)
COLOUR_34 = (186, 110, 248)
COLOUR_45 = (146, 103, 151)
COLOUR_51 = (186, 91, 88)
COLOUR_13 = (144, 97, 185)
COLOUR_32 = (116, 196, 145)
COLOUR_24 = (185, 156, 190)

COLOURS = [
    ([COLOUR_1, COLOUR_12, COLOUR_51, COLOUR_13], 0.15),
    ([COLOUR_2, COLOUR_12, COLOUR_23, COLOUR_32, COLOUR_24], 0.25),
    ([COLOUR_3, COLOUR_23, COLOUR_34, COLOUR_13, COLOUR_32], 0.1),
    ([COLOUR_4, COLOUR_34, COLOUR_45, COLOUR_24], 0.1),
    ([COLOUR_5, COLOUR_45, COLOUR_51], 0.1),
]


def in_colour_range(pixel_colour, target_colour_list, range_size):
    r, g, b = pixel_colour
    for target_colour in target_colour_list:
        rleft = max(0, target_colour[0] - target_colour[0] * range_size)
        rright = min(255, target_colour[0] + target_colour[0] * range_size)
        gleft = max(0, target_colour[1] - target_colour[1] * range_size)
        gright = min(255, target_colour[1] + target_colour[1] * range_size)
        bleft = max(0, target_colour[2] - target_colour[2] * range_size)
        bright = min(255, target_colour[2] + target_colour[2] * range_size)
        if rleft <= r <= rright and gleft <= g <= gright and bleft <= b <= bright:
            return True

    return False


def decode_captcha(file_name, idx):
    with Image.open(file_name) as im:
        x, y = im.size
        pixels = im.load()
        colour_number = 1
        for (colours_list, range_size) in COLOURS:
            image = Image.new("RGB", im.size, "WHITE")
            new_pixels = image.load()
            for i in range(0, x):
                for j in range(0, y):
                    c = pixels[i, j]
                    if in_colour_range(c, colours_list, range_size):
                        new_pixels[i, j] = (0, 0, 0)
            image.save("{}-{}.jpg".format(idx, colour_number))
            colour_number += 1
    return "0000000000"


if __name__ == "__main__":
    # r = requests.post("http://64.225.70.156/login", data={"login": LOGIN, "password": PWD})
    cookies = dict(PHPSESSID="e2a865afaa45fbe5d528ee85bc47d969")
    idx = 0
    while True:
        img = requests.get("http://64.225.70.156/captcha", cookies=cookies)
        if img.status_code == 200:
            file_name = "{}.jpg".format(idx)
            with open(file_name, "wb") as f:
                f.write(img.content)
            correct_answer = decode_captcha(file_name, idx)
            resp = requests.post(
                "http://64.225.70.156/prove/speed/{}".format(idx),
                data={"captcha": correct_answer},
                cookies=cookies,
            )
            print(resp.content)
            idx += 1
            exit(0)
