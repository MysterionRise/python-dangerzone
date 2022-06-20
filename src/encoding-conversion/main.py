import glob


def convert_to_utf8():
    # list all files in data folder
    files = glob.glob('data/*.txt')
    for file in files:
        with open(file, 'r', encoding='cp1251') as f:
            # read file
            lines = f.readlines()
            # save file
            with open(f"data-updated/{file.split('/')[1]}", 'w',
                      encoding='utf-8') as f:
                f.writelines(lines)


def get_all_answers():
    files = glob.glob("data-per-day/*/*.txt")
    answers = set()
    for file in files:
        with open(file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            for line in lines:
                if 0 < len(line.strip()) < 25:
                    answers.add(line.strip().lower())
    for answer in answers:
        print(answer)
    print(len(answers))


if __name__ == '__main__':
    get_all_answers()
