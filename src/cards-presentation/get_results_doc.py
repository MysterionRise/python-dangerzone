import pandas as pd
from glob import glob


def main():
    participants = pd.read_csv('data/participants.csv')
    participants_map = dict()
    for _, row in participants.iterrows():
        participants_map[row['seq']] = row['id']
    print(participants_map)
    template = pd.read_excel('data/template.xlsx')
    answers_per_name = dict()
    for file in glob('data/*.log'):
        answers_per_row = dict()
        with open(file) as f:
            lines = f.readlines()
            idx = 0
            for line in lines:
                answers = line.strip().split(',')
                if idx < 8:
                    answers_per_row[idx] = answers
                idx += 1
        answers_per_name[file.split('/')[-1].split('.')[0]] = answers_per_row
    print(answers_per_name)
    for _, row in template.iterrows():
        name = participants_map[row['seq']]
        row['name'] = name
        # row.to_csv(f'data/{name}.csv', index=False)
    template.to_csv('data/template.csv', index=False)


if __name__ == '__main__':
    main()
