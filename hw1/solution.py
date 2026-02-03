# pyright: basic

import sys
from types import LambdaType

class Board:
    def __init__(self,n: int) -> None:
        self.n = n
        self._create_strips()
        self.old_positions = set()

    def _create_strips(self):
        rows = self.n
        self.cols = HistoricRow(rows)
        self.rows = HistoricRow(rows)

        diag_count = (4*rows)-2
        self.diag_a = HistoricRow(diag_count) # ///
        self.diag_b = HistoricRow(diag_count) # \\\
        
    def try_place(self,pnt) -> bool:
        valid = self.can_place(pnt)
        if valid: self._place(pnt)
        return valid
    
    def _place(self,pnt) -> None:
        print(f"Placing {pnt}")
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
        print(f"Restarting cycle with point {point}")
        self._create_strips()
        self._place(point)
        self.forbid_position(point)

    def undo_last_place(self):
        strips = [
                self.rows,
                self.cols,
                self.diag_a,
                self.diag_b
                ]
        for strip in strips:
            strip.unset()

    def forbid_position(self,point):
        self.old_positions.add(point)

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

class HistoricQueue:
    def __init__(self,contents):
        self._inner = contents
        self._pos = 0
        self._checkpoints = []
    def has_next(self):
        return self._pos < len(self._inner)

    def next(self):
        self._pos += 1
        return self._inner[self._pos-1]

    def checkpoint(self):
        self._checkpoints.append(self._pos)

    def checkout(self):
        print(f"checking out. old checkpoints are: {self._checkpoints}")
        return [ self._inner[i-1] for i in self._checkpoints ]

    def revert(self):
        self._pos = self._checkpoints.pop()
        print(f"reverted! position is now {self._pos}")
    
    def reset(self):
        self._pos = 0
        self._checkpoints = []
    
    def has_checkpoint(self):
        return len(self._checkpoints) != 0

class SelfSolvingBoard:
    def __init__(self, board: Board) -> None:
        self._board = board
        self._hqueue = HistoricQueue(board.get_all_positions())

        self._first_positions = board.valid_first_positions()
        self._num_first_positions = len(self._first_positions)
        self._position_iter = 0

        self._rowcount = board.n

        self._num_placed = 0
        self._discovered_solutions = []
        
    def get_all_solutions(self):
        all_solutions = []
        while self._has_placements():
            all_solutions += self._find_solution_set()
        return all_solutions

    def _get_first_placement(self):
        self._position_iter += 1
        return self._first_positions[self._position_iter-1]
    
    def _has_placements(self):
        return self._position_iter < self._num_first_positions

    def _find_solution_set(self):
        self._num_placed = 1
        self._hqueue.reset()
        firstpos = self._get_first_placement()
        self._board.init_cycle(firstpos)
        discovered_solutions = []
        while True:
            if self._hqueue.has_next():
                self._place_one()
            elif self._hqueue.has_checkpoint():
                self._revert_checkpoint()
            else:
                break

            if self._num_placed == self._rowcount:
                discovered_solutions.append(self._checkout_solution(firstpos))
        
        return discovered_solutions

    def _place_one(self):
        to_place = self._hqueue.next()
        was_valid = self._board.try_place(to_place)
        if was_valid:
            self._num_placed += 1
            self._hqueue.checkpoint()

    def _revert_checkpoint(self):
        self._board.undo_last_place()
        self._hqueue.revert()
        self._num_placed -= 1

    def _checkout_solution(self,first_position):
        positions = [first_position] + self._hqueue.checkout()
        self._revert_checkpoint()
        return positions

if True:
    rowcount = int(sys.argv[1])
    board = Board(rowcount)
    solution = SelfSolvingBoard(board)
    print(solution.get_all_solutions())
