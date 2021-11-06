import os.path

import pandas as pd


def join_log_files(name: str):
    """
    Joins all log files into one file.
    """
    with open(f'joined/{name}.log', 'w') as f2:
        for subdir in ['2', '4', '6']:
            if os.path.exists(f'data/{subdir}/{name}_additional.log'):
                with open(f'data/{subdir}/{name}_additional.log', 'r') as f:
                    for line in f:
                        if "NAME" not in line:
                            f2.write(line)
            else:
                match subdir:
                    case '2' | '4':
                        for i in range(0, 150):
                            f2.write("0\t0\t0\t0\t0\t0\t0\n")
                    case '6':
                        for i in range(0, 100):
                            f2.write("0\t0\t0\t0\t0\t0\t0\n")


if __name__ == '__main__':
    df = pd.read_csv('data/participants.csv', sep=',', header=None)

    # for index, row in df.iterrows():
    #     join_log_files(row[0])
    #

    for _, row in df.iterrows():
        sheet_name = f'Набор{row[1]}'
        lookup = pd.read_excel('data/lookup_table.xls', sheet_name=sheet_name)
        data = pd.read_csv(f'joined/{row[0]}.log', sep='\t', header=None)
        print(row[0])
        with open(f'final/{row[0]}.log', 'w') as f2:
            for _, row2 in data.iterrows():
                if str(row2[0]) == '0':
                    f2.write("0\t0\t0\t0\t0\t0\t0\t0\n")
                else:
                    # if (row2[1] != '0'):
                    # f2.write(f"{row[0]}\t{row[1]}\t{row[2]}\t{row[3]}\t{row[4]}\t{row[6]}\t{row[7]}\t{lookup[lookup[0] == row2[1]]}\n")
                    res = lookup[lookup["sound_code"] == row2[1]]
                    value = int(res["метка_категории"].iloc[0])
                    # print(value)
                    f2.write(f"{row2[0]}\t{row2[1]}\t{row2[2]}\t{row2[3]}\t{row2[4]}\t{row2[5]}\t{row2[6]}\t{value}\n")
                # else:
                #     f2.write("0\t0\t0\t0\t0\t0\t0\t0\n")

        # print(data.size)

    #     join_log_files(row[0])
