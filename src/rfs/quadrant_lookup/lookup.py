import pandas as pd


def read_lookup():
    df = pd.read_csv("lookup.csv")
    lookup_map = {}
    for _, row in df.iterrows():
        lookup_map[(row["pic"], row["key"])] = row["value"]
    return lookup_map


def main():
    lookup_map = read_lookup()
    df = pd.read_csv("results.csv")
    with open("res.txt", "w", encoding="utf-8") as f:
        for ind, row in df.iterrows():
            try:
                x = lookup_map[(row["2"], int(row["Где искали_квартиль"]))]
                f.write(f"{x}\n")
            except Exception:
                print("------------------------")
                print(ind)
                print(row)
                return
                # print(e)
                # print(ind)


if __name__ == "__main__":
    main()
