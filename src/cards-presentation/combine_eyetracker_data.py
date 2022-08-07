import os
from glob import glob

import pandas as pd


def get_seq_by_name(key, participants_map):
    return participants_map.get(key, -1)


def get_presenting_type(param, seq, keys_map):
    if seq == -1:
        return -1
    return keys_map[seq].get(param.split(".")[0], -1)


def get_actual_presentation(param):
    # split Gac_1_17.png to get 17
    return int(param.split("_")[-1].split(".")[0])


def main():
    # read participants data as map
    participants = pd.read_excel("eyetracker_data/participants.xlsx")
    participants_map = {}
    for _, row in participants.iterrows():
        participants_map[row["id"]] = row["seq"]

    # read keys data as map
    keys = pd.read_excel("eyetracker_data/key.xlsx")
    keys_map = {}
    for seq_id in range(1, 33):
        map_ = {}
        for _, row in keys.iterrows():
            map_[row["id"]] = row[f"seq_{seq_id}"]
        keys_map[seq_id] = map_
    print(keys_map)
    # read all text data from eyetracker data
    for file_ in glob("eyetracker_data/*.txt"):
        data_df = pd.read_csv(file_, sep="\t")
        append_df = pd.DataFrame(
            columns=["seq", "presenting_type", "prop_presentation"]
        )
        for _, row in data_df.iterrows():
            seq = get_seq_by_name(row["Session_Name_"], participants_map)
            s = pd.Series(
                [
                    seq,
                    get_presenting_type(row["pic_1"], seq, keys_map),
                    get_actual_presentation(row["pic_search_1"]),
                ],
                index=["seq", "presenting_type", "prop_presentation"],
            )
            append_df = append_df.append(s, ignore_index=True)
        data_df = pd.concat([data_df, append_df], axis=1)
        data_df.to_csv(
            "results.csv", mode="a", header=not os.path.exists("results.csv")
        )


if __name__ == "__main__":
    main()
