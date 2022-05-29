import random

import pandas as pd

if __name__ == '__main__':
    df = pd.read_csv('seq1.csv')
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
        2031,
        2033,
        2038,
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
        2144,
        2148,
        2152
    ]
    for _, row in df.iterrows():
        # create series
        first = row['quest1_a_sound_id'] if row['quest1_a_sound_id'] != 0 else row['quest1_b_sound_id']
        second = row['sound_code']
        swap_prob = random.random()
        third = row['pic_code'] if swap_prob >= 0.5 else row['ac_col']
        fourth = row['ac_col'] if swap_prob >= 0.5 else row['pic_code']
        fifth = row['quest2_b_sound_id'] if row['quest2_b_sound_id'] != 0 else random.choice([1306, 1307, 1308, 1309, 1310])
        s = pd.Series(
            [int(first), int(second), int(third), int(fourth), int(fifth)],
            index=['1', '2', '3', '4', '5'])
        if fourth in first_df_list or fifth in first_df_list:
            first_df.append(s, ignore_index=True)
        else:
            second_df.append(s, ignore_index=True)
        final_df = pd.concat([first_df, second_df])
        first_df = first_df.append(s, ignore_index=True)
    print(final_df.head())
    final_df.to_csv('created_seq.csv', index=False)