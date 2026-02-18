#pyright: basic

from __future__ import annotations
from enum import Enum

class Direction(Enum):
    Left = 1
    Right = 2

if __name__ == "__main__":
    print("lol")

def childOf(arr, nodenum: int, direction: Direction) -> int:
    return (nodenum*2) + (direction.value)

def fillTo(arr,minsize: int):
    toappend = max(0,minsize-len(arr)+1)
    arr += [ None ] * toappend

def trim(arr):
    while len(arr) != 0:
        if arr[-1] == None:
            arr.pop()
        else:
            break
    return arr

def find(arr,val,allow_empty=False):

    def findhelper(pos: int) -> int:
        if allow_empty:
            fillTo(arr,pos)
            if arr[pos] == None:
                return pos
        elif pos >= len(arr) or arr[pos] == None: 
            return -1
        
        if val == arr[pos]:
            return pos

        direction = Direction.Left if val < arr[pos] else Direction.Right
        nextpos = childOf(arr,pos,direction)
        return findhelper(nextpos)

    return findhelper(0)

def insert(arr,val):
    arr[find(arr,val,allow_empty=True)] = val

def remove(arr,val):
    if (pos := find(arr,val)) != -1:
        arr[pos] = None
        remove(arr,childOf(arr,pos,Direction.Left))
        remove(arr,childOf(arr,pos,Direction.Right))

l = []

insert(l,10)
insert(l,5)
insert(l,15)
insert(l,14)
print(l)
remove(l,14)
print(l)
trim(l)
print(l)
print("removed 14 and trimmed")
remove(l,15)
print(l)
trim(l)
print(l)
