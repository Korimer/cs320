# pyright: basic

import sys

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

class Board:
    def __init__(self,n: int) -> None:
        self.n = n
        self._create_strips()
        self._old_placements = []

    def _create_strips(self):
        rows = self.n
        self.cols = HistoricStrip(rows)
        self.rows = HistoricStrip(rows)

        diag_count = (2*rows)-1
        self.diag_a = HistoricStrip(diag_count) # ///
        self.diag_b = HistoricStrip(diag_count) # \\\
        
    def try_place(self,pnt) -> bool:
        valid = self.can_place(pnt)
        if valid: self._place(pnt)
        return valid
    
    def _place(self,pnt) -> None:
        self._old_placements.append(pnt)
        x,y = pnt.tup()
        self.cols.set(x)
        self.rows.set(y)
        self.diag_a.set(x+y)
        self.diag_b.set(self.n-1+x-y)

    def can_place(self,pnt) -> bool:
        x,y = pnt.tup()
        
        tve = (
            self.cols.can_set(x)
            and self.rows.can_set(y)
            and self.diag_a.can_set(x+y)
            and self.diag_b.can_set(self.n+x-y)
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
    
    def checkout_placements(self) -> list[Point]:
        return self._old_placements.copy()

    def undo_last_place(self):
        strips = [
                self.rows,
                self.cols,
                self.diag_a,
                self.diag_b
                ]
        for strip in strips:
            strip.unset()
        self._old_placements.pop()

class HistoricStrip:
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

def nQueensAll():
    rowcount = int(sys.argv[1])
    solutions = []
    board = Board(rowcount)

    def _recurse(row,board: Board):
        if row == rowcount:
            solutions.append(board.checkout_placements())
            return
        for col in range(rowcount):
            if board.try_place(Point(row,col)):
                _recurse(row+1,board)
                board.undo_last_place()

    _recurse(0,board)

    print(solutions)

nQueensAll()

