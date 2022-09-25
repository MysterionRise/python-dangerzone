from glob import glob

import pandas as pd


def get_answer(ind, answers):
    return answers[ind].split("_")[1]


def get_rt(answers):
    return int(answers[-1])


def main():
    participants = pd.read_csv("data/participants.csv")
    participants_map = {}
    for _, row in participants.iterrows():
        if row["seq"] in participants_map:
            participants_map[row["seq"]].append(row["id"])
        else:
            participants_map[row["seq"]] = [row["id"]]
    print(participants_map)
    template = pd.read_excel("data/template.xlsx")
    answers_per_name = {}
    for file in glob("data/*.log"):
        answers_per_row = {}
        with open(file, encoding="utf-8") as f:
            lines = f.readlines()
            idx = 0
            for line in lines:
                answers = line.strip().split(",")
                if idx < 8:
                    answers_per_row[idx] = answers
                idx += 1
        answers_per_name[file.split("/")[-1].split(".")[0]] = answers_per_row
    results = pd.DataFrame(
        columns=["name", "seq", "Plod", "Condtion", "Answer", "Corr", "Time"]
    )
    ind = 0
    big_ind = 0
    for _, row in template.iterrows():
        list_by_seq = participants_map[row["seq"]]
        # check if list_by_seq is list
        if isinstance(list_by_seq, list):
            name = list_by_seq[0]
        else:
            name = list_by_seq
        if name not in answers_per_name:
            print(name)
        else:
            answers = answers_per_name[name].get(big_ind)
            s = pd.Series(
                [
                    name,
                    row["seq"],
                    row["Plod"],
                    row["Condtion"],
                    get_answer(ind, answers),
                    row["Corr"],
                    get_rt(answers),
                ],
                index=["name", "seq", "Plod", "Condtion", "Answer", "Corr", "Time"],
            )
            results = results.append(s, ignore_index=True)
            ind += 1
            if ind == 7:
                ind = 0
                big_ind += 1
            if big_ind == 8:
                # delete name from participants_map
                del participants_map[row["seq"]][0]
                big_ind = 0
    print(participants_map)
    results.to_csv("data/results.csv", index=False)


if __name__ == "__main__":
    main()
