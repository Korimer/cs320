from __future__ import annotations
from enum import Enum


if __name__ == "__main__":
    print("lol")

class AsIfATree:
    def __init__(self) -> None:
        self.core = []
        self.len = 0

    def height(self) -> int:
        return 0

    def width(self) -> int:
        return 1

    def childOf(self, nodenum: int, direction: Direction) -> int:
        return (nodenum*2) + (direction.value)

    def find(self,val,populate_on_oob=False):

        def findhelper(pos: int,val) -> int:
            if populate_on_oob:
                self.fillTo(pos)
            elif pos < len(self): 
                return -1

            if self.core[pos] == None:
                return pos
            else:
                direction = Direction.Left if self.core[pos] < val else Direction.Right
                nextpos = self.childOf(pos,direction)
                return findhelper(nextpos,val)

        return findhelper(0,val)

    def insert(self,val):
        self.core[self.find(val,populate_on_oob=True)] = val

    def fillTo(self,minsize: int):
        toappend = max(0,minsize-len(self)+1)
        self.len += toappend
        self.core += [ None ] * toappend

    def __len__(self) -> int:
        return self.len
            

class Direction(Enum):
    Left = 1
    Right = 2


tree = AsIfATree()

tree.insert(1)
tree.insert(2)
tree.insert(5)
tree.insert(-1)
print(tree.core)
