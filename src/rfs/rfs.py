import glob

import pandas as pd


def get_data_by_seq(seq: int):
    rfs = pd.read_csv(f"rnf/RFS-seq{seq}.csv")
    return rfs


def main():
    participants = pd.read_excel("rnf/participants.xlsx")
    result = pd.DataFrame()
    seq_by_name = {}
    for _, row in participants.iterrows():
        seq_by_name[row["id"]] = row["seq"]
    print(seq_by_name)
    for file in glob.glob("rnf/*.log"):
        with open(file, "r", encoding="utf-8") as f:
            data = f.readlines()
            name = data[0].split("\t")[1].strip()
            print(name)
            seq = seq_by_name[name]
            print(seq)
            lookup = get_data_by_seq(seq)
            counts = {}
            for line in data[1:]:
                cells = line.split("\t")
                quest1_a_sound_id = int(cells[0])
                sound_code = int(cells[1])
                quest2_b_sound_id = int(cells[2])
                cell4 = cells[3]
                cell5 = cells[4]
                cell6 = cells[5]
                cell7 = cells[6]
                # word_representation_impl = lookup.loc[
                #     (lookup['sound_code'] == sound_code) & (lookup[
                #                                                 'quest1_a_sound_id'] == quest1_a_sound_id)]
                word_representation_impl = lookup.loc[
                    (lookup["quest1_a_sound_id"] == quest1_a_sound_id)
                ]
                impl_ = word_representation_impl["метка_seq1"].values
                # word_representation_expl = lookup.loc[
                #     (lookup['sound_code'] == sound_code) & (lookup[
                #                                                 'quest2_b_sound_id'] == quest2_b_sound_id)]
                word_representation_expl = lookup.loc[
                    (lookup["quest2_b_sound_id"] == quest2_b_sound_id)
                ]
                expl_ = word_representation_expl["метка_seq1"].values
                label = int(impl_[0]) if impl_ else int(expl_[0])
                pic_name = (
                    word_representation_impl["pic_name"].values[0]
                    if word_representation_impl["pic_name"].values
                    else word_representation_expl["pic_name"].values[0]
                )
                # print(pic_name)
                # print(label)
                count = counts.get(label, {}).get(pic_name, 1)
                s = pd.Series(
                    [
                        name,
                        seq,
                        quest1_a_sound_id,
                        sound_code,
                        quest2_b_sound_id,
                        cell4,
                        cell5,
                        cell6,
                        cell7,
                        pic_name,
                        label,
                        count,
                    ]
                )
                if len(counts.get(label, {})) == 0:
                    counts[label] = {pic_name: count + 1}
                else:
                    counts[label][pic_name] = count + 1
                # print(s)
                print(counts)
                # 222	1201	1310	2062	2036	RT:474	button:1
                result = result.append(s, ignore_index=True)
    result.to_excel("result.xlsx")


if __name__ == "__main__":
    main()
