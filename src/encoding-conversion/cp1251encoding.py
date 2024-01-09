from glob import glob

if __name__ == "__main__":
    for f in glob("gotshild/*.txt"):
        with open(f.strip(), "r", encoding="cp1251") as utf16f:
            with open(
                f.strip().replace("gotshild", "gotshild-utf-8"),
                "w",
                encoding="utf-8",
            ) as utf8f:
                try:
                    utf8f.writelines(utf16f.readlines())
                    print(f"{f.strip()} converted")
                except UnicodeDecodeError:
                    print(f.strip())
                    continue
