import pandas as pd
from random import choices
from PIL import Image
from collections import Counter


# 1  2  3  4  5  6
# 7  8  9  10 11 12
# 13 14 15 16 17 18
# 19 20 21 22 23 24
# 25 26 27 28 29 30
# 31 32 33 34 35 36
def quadrant_by_position(pos: int) -> int:
    match pos:
        case 1 | 2 | 3 | 7 | 8 | 9 | 13 | 14 | 15:
            return 14
        case 4 | 5 | 6 | 10 | 11 | 12 | 16 | 17 | 18:
            return 15
        case 19 | 20 | 21 | 25 | 26 | 27 | 31 | 32 | 33:
            return 16
        case 22 | 23 | 24 | 28 | 29 | 30 | 34 | 35 | 36:
            return 17


# replacing _1 picture with _3 picture
def replace_picture(picture):
    return picture.replace('_1', '_3')


# update dict with pictures, so picture will be placed in quadrant
# if replace_with not None => replace picture with replace_with one
# return dict with updated pictures
def update_pictures(zipped, picture, quadrant, replace_with=None,
                    default_quadrant=None):
    zipped_copy = zipped.copy()
    if replace_with is not None:
        zipped_copy[replace_with] = default_quadrant
        zipped_copy[picture] = quadrant
        # remove random picture from zipped_copy that is in quadrant but not picture
        removed_pic = None
        for picture_, quadrant_ in zipped_copy.items():
            if quadrant_ == quadrant and picture_ != picture:
                removed_pic = picture_
                break
        del zipped_copy[removed_pic]
    else:
        zipped_copy[picture] = quadrant
    return zipped_copy


# create image of RGB 205 205 205 of size 1770x1770
# add all pictures from picture_dict to image depending on quadrant
# each position is encoded left to right, top to bottom
# 1  2  3  4  5  6
# 7  8  9  10 11 12
# 13 14 15 16 17 18
# 19 20 21 22 23 24
# 25 26 27 28 29 30
# 31 32 33 34 35 36
# each smaller picture is of size 295x295
# save image to file_name
def generate_card(pictures_dict, position_sequence, main_picture, main_quadrant):
    assert len(pictures_dict) == 16
    assert len(position_sequence) == 16
    assert main_picture in pictures_dict.keys()
    assert main_quadrant in pictures_dict.values()

    im = Image.new('RGBA', (1770, 1770), color=(205, 205, 205))
    # sort pictures_dict by second element
    pictures_dict = dict(sorted(pictures_dict.items(), key=lambda x: x[1]))
    # sort position sequence so first positions will be in quadrant 14
    # then quadrant 15, etc.
    position_sequence = sorted(position_sequence,
                               key=lambda x: quadrant_by_position(x))
    quads = Counter([quadrant_by_position(pos) for pos in position_sequence])
    assert quads[14] == 4
    assert quads[15] == 4
    assert quads[16] == 4
    assert quads[17] == 4
    print(pictures_dict)
    i = 0
    for picture, quadrant in pictures_dict.items():
        with Image.open(f"images/{picture}.png") as img:
            # past picture  to image by position_sequence
            im.paste(img, (int(((position_sequence[i] - 1) % 6)) * 295,
                           int(((position_sequence[i] - 1)/ 6)) * 295), img)
        i += 1
    im.save(f"images/result/{main_picture}_{main_quadrant}.png")


def main():
    templates_df = pd.read_csv('templates.csv', sep=',', header=None)
    templates = []
    for _, row in templates_df.iterrows():
        templates.append(row.tolist())
    presentation = pd.read_excel("cards-presentation.xlsx")
    # print(presentation.head())
    pictures = presentation['pic'].tolist()
    # just 1 sequence
    for i in range(1, 2):
        quadrants = presentation[f"seq_{i}"].tolist()
        zipped = dict(zip(pictures, quadrants))
        for picture in pictures[:8]:
            default_quadrant = zipped[picture]
            for quadrant in [14, 15, 16, 17]:
                if default_quadrant == quadrant:
                    generate_card(update_pictures(zipped, picture, quadrant),
                                  choices(templates)[0], picture, quadrant)
                else:
                    generate_card(update_pictures(zipped, picture, quadrant,
                                                  replace_with=replace_picture(
                                                      picture),
                                                  default_quadrant=default_quadrant),
                                  choices(templates)[0], picture, quadrant)

        print(zipped)
    print(pictures)
    for index, row in presentation.iterrows():
        print(row[0])


if __name__ == '__main__':
    main()
