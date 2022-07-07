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
def generate_card(pictures_dict, position_sequence, main_picture,
                  main_pos):
    im = Image.new('RGBA', (1770, 1770), color=(205, 205, 205))
    # sort pictures_dict by second element
    pictures_dict = dict(sorted(pictures_dict.items(), key=lambda x: x[1]))
    # sort position sequence so first positions will be in quadrant 14
    # then quadrant 15, etc.
    position_sequence = sorted(position_sequence.copy(),
                               key=lambda x: quadrant_by_position(x))
    if main_pos in position_sequence:
        position_sequence.remove(main_pos)
    else:
        print(f"{main_picture} with pos {main_pos} is not in position sequence")
    i = 0
    for picture, quadrant in pictures_dict.items():
        with Image.open(f"images/{picture}.png") as img:
            # past picture  to image by position_sequence
            im.paste(img, (int(((position_sequence[i] - 1) % 6)) * 295,
                           int(((position_sequence[i] - 1) / 6)) * 295), img)
        i += 1
    im.paste(Image.open(f"images/{main_picture}.png"),
             (int((main_pos - 1) % 6) * 295, int((main_pos - 1) / 6) * 295),
             Image.open(f"images/{main_picture}.png"))
    im.save(f"images/result/{main_picture}_{quadrant_by_position(main_pos)}.png")


# creates dict of positions per quadrant
def make_dict(q1: int, q2: int, q3: int, q4: int) -> dict:
    res = dict()
    res[14] = q1
    res[15] = q2
    res[16] = q3
    res[17] = q4
    return res


def delete_random(picture_dict, default_quadrant):
    # delete random picture from picture_dict
    removed_pic = None
    for picture_, quadrant_ in picture_dict.items():
        if quadrant_ == default_quadrant:
            removed_pic = picture_
            break
    del picture_dict[removed_pic]
    return picture_dict


def main():
    seq_positions_df = pd.read_csv('sequence_positions.csv')
    seq_positions_by_name = dict()
    for index, row in seq_positions_df.iterrows():
        # TODO may be need to swap 16 and 17
        seq_positions_by_name[row['name']] = make_dict(row['14'], row['15'],
                                                       row['16'], row['17'])

    templates_df = pd.read_csv('templates.csv', sep=',', header=None)
    templates = dict()
    for _, row in templates_df.iterrows():
        data = row.tolist()[0].split(',')
        templates[data[0]] = [int(x) for x in data[1:]]
    presentation = pd.read_excel("cards-presentation.xlsx")
    # print(presentation.head())
    pictures = presentation['pic'].tolist()
    # just 1 sequence
    for i in range(1, 2):
        quadrants = presentation[f"seq_{i}"].tolist()
        zipped = dict(zip(pictures, quadrants))
        for picture in pictures[:8]:
            position_by_quadrant = seq_positions_by_name[f"{picture}_seq_{i}"]
            default_pos = position_by_quadrant[zipped[picture]]
            default_quadrant = quadrant_by_position(default_pos)
            for quadrant in [14, 15, 16, 17]:
                picture_pos = position_by_quadrant[quadrant]
                picture_dict = zipped.copy()
                if default_quadrant == quadrant:
                    del picture_dict[picture]
                    generate_card(picture_dict, templates[picture], picture,
                                  default_pos)
                else:
                    del picture_dict[picture]
                    picture_dict[replace_picture(picture)] = default_quadrant
                    generate_card(
                        delete_random(picture_dict, default_quadrant),
                        templates[picture], picture, picture_pos)

        print(zipped)
    print(pictures)
    for index, row in presentation.iterrows():
        print(row[0])


if __name__ == '__main__':
    main()
