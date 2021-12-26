import random


def bigger_than_others(target, prev_numbers):
    """
    check if x is different than all elements in prev by at least 11
    """
    if x == 0:
        return False
    for prev in prev_numbers:
        if abs(target - prev) < 11:
            return False
    return True


if __name__ == '__main__':
    with open("seq.txt", encoding="utf-8") as file:
        lines = file.readlines()
        for line in lines:
            line = line.strip()
            if line.startswith("Seq") or line == "":
                print(line)
                continue
            numbers = [int(s) for s in line.split()]
            print(numbers[0], end=" ")
            prev = []
            for i in range(1, len(numbers) - 1):
                if i == numbers[-1]:
                    prev.append(numbers[i])
                    print(numbers[i], end=" ")
                else:
                    x = 0
                    while not bigger_than_others(x, prev):
                        if len(prev) == 2:
                            x = random.randint(2081, 2160)
                        else:
                            x = random.randint(2001, 2080)
                    prev.append(x)
                    print(x, end=" ")
            print(numbers[-1])
