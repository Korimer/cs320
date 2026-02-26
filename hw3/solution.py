# pyright: basic

from collections import Counter


def countPermStr(string1: str, string2: str):
    if string2 == "":
        raise ValueError()

    len2 = len(string2)
    chars = Counter(string2)
    encountered = 0
    matches = 0
    totalcount = 0

    charsbase = chars.copy()

    for char in string1:
        encountered += 1
        if char in chars:
            chars.subtract(char)
            count = chars.get(char)
            if count != None and count >= 0:
                matches += 1
            if matches == len2:
                totalcount += 1
                matches -= 1
                chars[string1[encountered-len2]] += 1
        else:
            chars = charsbase.copy()
            matches = 0
    return totalcount
