import random

import pandas as pd

if __name__ == '__main__':
    df = pd.read_csv('seq3.csv')
    # create empty df
    first_df = pd.DataFrame(columns=['1', '2', '3', '4', '5'])
    second_df = pd.DataFrame(columns=['1', '2', '3', '4', '5'])
    first_df_list = [
        2002,
        2005,
        2011,
        2014,
        2021,
        2024,
        2025,
        2032,
        2033,
        2037,
        2041,
        2047,
        2049,
        2054,
        2057,
        2062,
        2066,
        2071,
        2073,
        2079,
        2082,
        2087,
        2091,
        2093,
        2113,
        2117,
        2130,
        2135,
        2139,
        2148,
        2152
    ]
    for _, row in df.iterrows():
        # create series
        first = row['quest1_a_sound_id'] if row['quest1_a_sound_id'] != 0 else row['quest1_b_sound_id']
        second = row['sound_code']
        third = row['quest2_b_sound_id'] if row['quest2_b_sound_id'] != 0 else random.choice([1306, 1307, 1308, 1309, 1310])
        fourth = row['ac_row']
        fifth = row['pic_code']
        sixth = row['метка_seq1']
        s = pd.Series(
            [int(first), int(second), int(third), int(fourth), int(fifth), int(sixth)],
            index=['1', '2', '3', '4', '5', '6'])
        if fifth in first_df_list:
            first_df = first_df.append(s, ignore_index=True)
        else:
            second_df = second_df.append(s, ignore_index=True)
    first_df = first_df.sample(frac=1).reset_index(drop=True)
    first_df = first_df.sample(frac=1).reset_index(drop=True)
    first_df = first_df.sample(frac=1).reset_index(drop=True)
    second_df = second_df.sample(frac=1).reset_index(drop=True)
    second_df = second_df.sample(frac=1).reset_index(drop=True)
    second_df = second_df.sample(frac=1).reset_index(drop=True)
    final_df = pd.concat([first_df, second_df])
    # print(final_df)
    for _, row in final_df.iterrows():
        swap_prob = random.random()
        if swap_prob < 0.5:
            print(row['1'], row['2'], row['3'], row['4'], row['5'], str(row['6'])[:-2])
        else:
            print(row['1'], row['2'], row['3'], row['5'], row['4'], str(row['6'])[:-2])
    # print(final_df.head())
    # final_df.to_csv('created_seq.csv', index=False)