# pyright: basic

from queue import Queue
from collections import Counter


def dequeueInto(q: Queue, chrmap: Counter):
    chrmap[q.get()] += 1
    

def countPermStr(string1: str, string2: str):
    if string2 == "":
        raise ValueError()

    len2 = len(string2)
    chars = Counter(string2)
    encountered = Queue()
    matches = 0
    totalcount = 0

    charsbase = chars.copy()

    for char in string1:
        if char in chars:
            chars.subtract(char)
            encountered.put(char)
            count = chars.get(char)
            if count != None and count >= 0:
                matches += 1
            if matches == len2:
                totalcount += 1
                matches -= 1
                dequeueInto(encountered,chars)
        else:
            chars = charsbase.copy()
            matches = 0
    return totalcount
