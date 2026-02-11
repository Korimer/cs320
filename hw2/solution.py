# pyright: basic
from __future__ import annotations
from typing import Optional, override

class NodeData:
    def __init__(self, val=None) -> None:
        self._val = val
        self._l = TreeNode()
        self._r = TreeNode()

    def insert(self, val) -> None:
        if val == self._val: raise Exception("Cannot have duplicate values!")
        return self._get(val).insert(val)

    def _get(self,val) -> TreeNode:
        if val < self._val: return self._l
        else:               return self._r

    @override
    def __str__(self) -> str:
        return f"({self._val} -> {self._l}, {self._r}"


class TreeNode:
    def __init__(self, node: Optional[NodeData] = None) -> None:
        self._inr = node

    def insert(self,val):
        if self._inr == None:
            self._inr = NodeData(val)
            self._empty = False
        else:
            self._inr.insert(val)

    @override
    def __str__(self) -> str:
        return f"[{self._inr}]"
    @override
    def __repr__(self) -> str:
        return str(self._inr)


t = TreeNode()
t.insert("hi!")
t.insert("bye...")

if __name__ == "main":
    print("lol")
print(__name__)
