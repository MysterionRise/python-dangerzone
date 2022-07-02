import pandas as pd


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


def main():
    templates = pd.read_csv('templates.csv', sep=',', header=None)
    # print(templates.head())
    presentation = pd.read_excel("cards-presentation.xlsx")
    # print(presentation.head())
    pictures = presentation['pic'].tolist()
    for i in range(1, 33):
        quadrants = presentation[f"seq_{i}"].tolist()
        zipped = dict(zip(pictures, quadrants))
        for picture in pictures[:8]:
            for quadrant in [14, 15, 16, 17]:
                


        print(zipped)
    print(pictures)
    for index, row in presentation.iterrows():
        print(row[0])


if __name__ == '__main__':
    main()
