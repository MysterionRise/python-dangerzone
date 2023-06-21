import random

import pandas as pd


def generate_sequence(list_name):
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
        2152,
    ]
    # df = pd.read_csv("test.csv")
    df = pd.read_excel("sequences.xlsx", sheet_name=f"Seq{list_name}")
    nan_value = float("NaN")
    df.replace("", nan_value, inplace=True)
    df.dropna(subset=["sound_code"], inplace=True)
    # create empty df
    first_df = pd.DataFrame(columns=["1", "2", "3", "4", "5"])
    second_df = pd.DataFrame(columns=["1", "2", "3", "4", "5"])
    for _, row in df.iterrows():
        # create series
        first = (
            row["quest1_a_sound_id"]
            if row["quest1_a_sound_id"] != 0
            else row["quest1_b_sound_id"]
        )
        second = row["sound_code"]
        third = (
            row["quest2_b_sound_id"]
            if row["quest2_b_sound_id"] != 0
            else random.choice([1306, 1307, 1308, 1309, 1310])
        )
        fourth = row["ac_row"]
        fifth = row["pic_code"]
        sixth = row["метка_seq1"]
        seventh = row["text_quest"]
        s = pd.Series(
            [
                int(first),
                int(second),
                int(third),
                int(fourth),
                int(fifth),
                int(sixth),
                seventh,
            ],
            index=["1", "2", "3", "4", "5", "6", "7"],
        )
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
    merged_df = pd.concat([first_df, second_df])
    final_df = pd.DataFrame(columns=["1", "2", "3", "4", "5", "6"])
    for _, row in merged_df.iterrows():
        swap_prob = random.random()
        if swap_prob < 0.5:
            s = pd.Series(
                [row["1"], row["2"], row["3"], row["4"], row["5"], row["7"]],
                index=["1", "2", "3", "4", "5", "6"],
            )
            final_df = final_df.append(s, ignore_index=True)
        else:
            s = pd.Series(
                [row["1"], row["2"], row["3"], row["5"], row["4"], row["7"]],
                index=["1", "2", "3", "4", "5", "6"],
            )
            final_df = final_df.append(s, ignore_index=True)
    # print(final_df.head())
    final_df.to_csv(f"seq{list_name}.csv", index=False, sep=" ")


def main():
    # generate_sequence(1)
    for i in range(1, 33):
        try:
            generate_sequence(i)
        except Exception as inst:
            print(type(inst))
            print(inst)
            print(f"Error in seq{i}")


if __name__ == "__main__":
    main()
