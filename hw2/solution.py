# pyright: basic

from __future__ import annotations
from enum import Enum


class Direction(Enum):
    Left = 1
    Right = 2


def childOf(nodenum: int, direction: Direction) -> int:
    return (nodenum * 2) + (direction.value)


def safeIndex(arr, index):
    return None if len(arr) <= index else arr[index]


def fillTo(arr, minsize: int):
    toappend = max(0, minsize - len(arr) + 1)
    arr += [None] * toappend  # This is a no-op if toappend is 0


def trim(arr):
    while len(arr) != 0:
        if arr[-1] == None:
            arr.pop()
        else:
            break
    return arr


def find(arr, val, allow_empty=False):
    def findhelper(pos: int) -> int:
        if allow_empty:
            fillTo(arr, pos)
            if arr[pos] == None:
                return pos
        elif pos >= len(arr) or arr[pos] == None:
            return -1

        if val == arr[pos]:
            return pos

        direction = Direction.Left if val < arr[pos] else Direction.Right
        nextpos = childOf(pos, direction)
        return findhelper(nextpos)

    return findhelper(0)


def insert(arr, val):
    arr[find(arr, val, allow_empty=True)] = val


def findSuccessor(arr,pos):
    cur = prev = childOf(pos, Direction.Right)
    if safeIndex(arr,cur) == None:
        return -1
    while safeIndex(arr, cur) != None:
        prev = cur
        cur = childOf(cur, Direction.Left)
    return prev


def remove(arr, val):
    if (pos := find(arr, val)) == -1:
        return False
    replacement = findSuccessor(arr, pos)
    if replacement != -1:
        childind = childOf(pos,Direction.Right)
        replacementchild = safeIndex(arr,childind)
        remove(arr,childind)
        arr[pos] = arr[replacement]
    else:
        replacementchild = None
    print(f"replacementchild is {replacementchild}")
    arr[replacement] = replacementchild
    trim(arr)
    return True


def checkNone(k, t):
    if k == None:
        raise ValueError("null key")
    if t == None:
        raise ValueError("no tree")


def findKey(k, t):
    checkNone(k, t)
    res = find(t, k, allow_empty=False)
    if res == -1:
        raise LookupError("not in tree")
    return res


def addKey(k, t):
    checkNone(k, t)
    try:
        insert(t, k)
    except TypeError:
        raise Exception("tree error")
    return t


def deleteKey(k, t):
    checkNone(k, t)
    if not remove(t, k):
        raise LookupError("not in tree")
    else:
        return t




tree = [50, 30, 70, 20, 40, 60, 80]
print("start:")
print(tree)
print("expected")
print( [20, 30, 40, 60, 70, 80] )
deleteKey(50,tree)
print("got")
print(tree)
