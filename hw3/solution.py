# pyright: basic

from collections import Counter


def countPermStr(string1: str, string2: str):
    if string2 == "" or string1 is None or string2 is None:
        raise ValueError()

    str2len = len(string2)
    if len(string1) < str2len:
        raise ValueError()

    for_success = Counter(string2)
    in_window = Counter()
    left_window = str2len * -1
    cur_matches = 0
    matches_for_full_perm = len(for_success)
    totalcount = 0

    for right_window in range(len(string1)):
        rchar = string1[right_window]
        in_window[rchar] += 1
        if for_success.get(rchar) == in_window[rchar]:
            cur_matches += 1

        if left_window >= 0:
            lchar = string1[left_window]
            if for_success.get(lchar) == in_window[lchar]:
                cur_matches -= 1
            in_window[lchar] -= 1

        if cur_matches == matches_for_full_perm:
            totalcount += 1
        
        left_window += 1

    return totalcount
