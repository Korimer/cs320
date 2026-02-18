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


def findLeftmost(arr, pos):
    cur = prev = childOf(arr, pos, Direction.Right)
    while safeIndex(arr, cur) != None:
        prev = cur
        cur = childOf(arr, cur, Direction.Left)
    return prev


def remove(arr, val):
    if (pos := find(arr, val)) != -1:
        arr[pos] = None
        replacement = findLeftmost(arr, pos)
        # lchild = childOf(pos,Direction.Left)
        # rchild = childOf(pos,Direction.Right)
        # if (lval := safeIndex(arr,lchild)) != None:
        #    remove(arr,lchild)
        #    insert(arr,lval)
        # if (rval := safeIndex(arr,rchild)) != None:
        #    remove(arr,rchild)
        #    insert(arr,rval)
        return True
    return False


def checkNone(t):
    if t == None:
        raise ValueError("null key")


def findKey(k, t):
    checkNone(t)
    res = find(t, k, allow_empty=False)
    if res == -1:
        raise LookupError("not in tree")
    return res


def addKey(k, t):
    checkNone(t)
    insert(t, k)
    return t


def deleteKey(k, t):
    checkNone(t)
    if not remove(t, k):
        raise LookupError("not in tree")
    else:
        return t
