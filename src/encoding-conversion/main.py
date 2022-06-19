import glob


def main():
    # list all files in data folder
    files = glob.glob('data/*.txt')
    for file in files:
        with open(file, 'r', encoding='cp1251') as f:
            # read file
            lines = f.readlines()
            # print(lines)
            # convert lines from cp1251 to utf8
            # lines = [line.encode('utf8').decode('cp1251') for line in lines]
            # lines = [line.encode('utf-8').decode('cp1251') for line in lines]
            # save file
            with open(f"data-updated/{file.split('/')[1]}", 'w', encoding='utf-8') as f:
                f.writelines(lines)


if __name__ == '__main__':
    main()
