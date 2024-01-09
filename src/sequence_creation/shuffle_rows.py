import random
import time

import pandas as pd

# List of all sheet names
sheets = ["Seq" + str(i) for i in range(1, 33)]

for sheet in sheets:
    # Read excel sheet
    df = pd.read_excel("sequences_2.xlsx", sheet_name=sheet)

    # Set the seed for random
    random.seed(time.time())

    # Filter data
    df_filtered = df[df["№_pic"] == "_1"][
        ["word", "pic1_cor", "pic2", "pic3", "pic4", "ans_pic"]
    ]

    # Shuffle rows
    df_filtered = df_filtered.sample(
        frac=1, random_state=random.randint(0, 10000)
    ).reset_index(drop=True)

    # Shuffle 'pic1_cor', 'pic2', 'pic3', 'pic4' and store position of 'pic1_cor'
    pic_columns = ["pic1_cor", "pic2", "pic3", "pic4"]
    df_filtered["pic1_cor_position"] = 0  # Initialization of new column

    for index, row in df_filtered.iterrows():
        pics = [row[col] for col in pic_columns]
        random.shuffle(pics)
        df_filtered.at[index, pic_columns] = pics
        df_filtered.at[index, "pic1_cor_position"] = (
            pics.index(row["pic1_cor"]) + 1
        )

        # Convert float columns to int
    df_filtered = df_filtered.astype(
        {
            col: int
            for col in df_filtered.columns
            if df_filtered[col].dtype == "float64"
        }
    )

    # Drop 'ans_pic' column
    df_filtered.drop(columns=["ans_pic"], inplace=True)

    # Rename 'pic1_cor' to 'pic1'
    df_filtered = df_filtered.rename(columns={"pic1_cor": "pic1"})

    # Write to csv
    df_filtered.to_csv(f"pic_seq_{sheet}.csv", index=False, sep="\t")
