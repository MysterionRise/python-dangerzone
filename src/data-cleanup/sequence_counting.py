import pandas as pd


if __name__ == '__main__':
    df = pd.read_excel('data/dataset.xlsx')
    prev_name = ""
    counts = dict()
    for index, row in df.iterrows():
        name = row['Name']
        if name != prev_name:
            counts = dict()
        word = row['Word']
        prev_cnt = counts.get(word, 0)
        counts[word] = prev_cnt + 1
        df.loc[index, 'Count'] = counts[word]
        prev_name = name
    # print(df.head())
    df.to_excel('data/dataset_counted.xlsx')