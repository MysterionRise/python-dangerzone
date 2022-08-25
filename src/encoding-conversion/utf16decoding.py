if __name__ == "__main__":
    with open("bad.txt", "r", encoding="utf-8") as f:
        files = f.readlines()
    for f in files:
        with open(f.strip(), "r", encoding="utf-16") as utf16f:
            with open(
                f.strip().replace("utf-16", "utf-8"), "w", encoding="utf-8"
            ) as utf8f:
                try:
                    utf8f.writelines(utf16f.readlines())
                    print(f"{f.strip()} converted")
                except UnicodeDecodeError:
                    print(f.strip())
                    continue
