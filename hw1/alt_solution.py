# pyright: basic

import sys

class Board:
    def __init__(self,n: int) -> None:
        self.n = n
        self._create_strips()
        self.old_positions = set()

    def _create_strips(self):
        rows = self.n
        self.cols = HistoricRow(rows)
        self.rows = HistoricRow(rows)

        diag_count = (2*rows)-1
        self.diag_a = HistoricRow(diag_count) # ///
        self.diag_b = HistoricRow(diag_count) # \\\
        
    def try_place(self,pnt) -> bool:
        valid = self.can_place(pnt)
        if valid: self._place(pnt)
        return valid
    
    def _place(self,pnt) -> None:
        x,y = pnt.tup()
        self.cols.set(x)
        self.rows.set(y)
        self.diag_a.set(x+y)
        self.diag_b.set(1+self.n+x-y)

    def can_place(self,pnt) -> bool:
        x,y = pnt.tup()
        
        tve = (
            not pnt in self.old_positions
            and self.cols.can_set(x)
            and self.rows.can_set(y)
            and self.diag_a.can_set(x+y)
            and self.diag_b.can_set(1+self.n+x-y)
        )

        return tve

    def valid_first_positions(self) -> list[Point]:
        # Because we're on a 2d board, every solution can be mirrored 8 ways
        # ...So, that means we only need to iterate over 1/8th of the board!
        return [
               Point(x,y)
               for x in range((self.n+1)//2)
               for y in range(0,x+1)
               ]

    def get_all_positions(self) -> list[Point]:
        return  [
                Point(x,y)
                for x in range(self.n)
                for y in range(self.n)
                ]

    def init_cycle(self,point):
        self._create_strips()
        self._place(point)

    def undo_last_place(self):
        strips = [
                self.rows,
                self.cols,
                self.diag_a,
                self.diag_b
                ]
        for strip in strips:
            strip.unset()

class HistoricRow:
    def __init__(self, count: int) -> None:
        self.full_row = [ True ] * count
        self.history = []
    
    def set(self,n: int) -> None:
        did_change = self.can_set(n)
        self.history.append(
                n if did_change else -1
            )
        self.full_row[n] = False

    def can_set(self,n: int) -> bool:
        return self.full_row[n]

    def unset(self):
        modified = self.history.pop()
        if modified != -1:
            self.full_row[modified] = True

    def __str__(self) -> str:
        return f"{self.full_row}: {self.history}"

class Point:
    def __init__(self,x: int, y: int) -> None:
        self.x = x
        self.y = y

    def tup(self) -> tuple[int,int]:
        return self.x, self.y

    def __str__(self) -> str:
        return f"Point{repr(self)}"

    def __repr__(self) -> str:
        return f"({self.x},{self.y})"
