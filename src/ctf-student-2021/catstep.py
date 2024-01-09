import random

import requests


def request(flag_: str):
    r = requests.post(url, data={"flag": flag_})
    dict_ = r.json()
    if "length" in dict_:
        print(f'{flag_} {dict_["length"]}')
        return dict_["length"]

    print(r.json())
    return 1000000


if __name__ == "__main__":
    url = "https://cat-step.disasm.me/"
    flag = "spbctf{%s}"
    all_chars = (
        "qwertyuiopasdfghjklzxcvbnm1234567890_QWERTYUIOPASDFGHJKLZXCVBNM"
    )
    best_flag = "easy_web_fuzzing_0t5AFzSG0Oc"
    prev_length = 5
    while prev_length != 1:
        choice = random.random()
        if choice > 0.67:
            for idx in range(0, len(best_flag) - 1):
                for ch in all_chars:
                    upd_flag = best_flag[:idx] + ch + best_flag[idx:]
                    length = request(flag % (best_flag + ch))
                    if length < prev_length:
                        prev_length = length
                        best_flag = best_flag + ch
                        break
        elif choice > 0.33:
            for idx in range(0, len(best_flag) - 1):
                upd_flag = "".join(
                    [best_flag[i] for i in range(len(best_flag)) if i != idx]
                )
                length = request(flag % upd_flag)
                if length < prev_length:
                    prev_length = length
                    best_flag = upd_flag
                    break
        else:
            for idx in range(0, len(best_flag) - 1):
                for ch in all_chars:
                    upd_flag = best_flag[:idx] + ch + best_flag[idx + 1 :]
                    length = request(flag % upd_flag)
                    if length < prev_length:
                        prev_length = length
                        best_flag = upd_flag
                        break
    print(best_flag)
    print(prev_length)
