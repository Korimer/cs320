#pyright: basic

from queue import Queue

def dequeueInto(q: Queue, chrmap: dict):
    chrmap[q.get()] += 1

def countPermStr(string1: str, string2: str):
    len2 = len(string2)
    chars = {}
    encountered = Queue()
    matches = 0
    totalcount = 0
    for char in string2:
        chars.setdefault(char,0)
        chars[char] += 1

    for char in string1:
        if char in chars:
            chars[char] -= 1
            encountered.put(char)
            if chars[char] >= 0:
                matches += 1
            if matches == len2:
                totalcount += 1
                matches -= 1
                dequeueInto(encountered,chars)
        else:
            while not encountered.empty():
                dequeueInto(encountered,chars)
            matches = 0
    return totalcount
