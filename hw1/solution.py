# pyright: basic

import sys
from typing import override


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
        self.forbid_position(point)


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

    @override
    def __str__(self) -> str:
        return f"{self.full_row}: {self.history}"

class Point:
    def __init__(self,x: int, y: int) -> None:
        self.x = x
        self.y = y

    def tup(self) -> tuple[int,int]:
        return self.x, self.y

    @override
    def __str__(self) -> str:
        return f"Point({self.x},{self.y})"
    @override
    def __repr__(self) -> str:
        return str(self)

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

    def _set_checkpoint(self,pos):
        self._checkpoints.append(pos)

    def checkpoint_prev(self):
        self._set_checkpoint(self._pos-1)

    def checkout(self):
        old_checkpoints = self._checkpoints
        self._pos = 0
        self._checkpoints = []
        print(f"checking out. old checkpoints are: {old_checkpoints}")
        return [ self._inner[i] for i in old_checkpoints ]

    def revert(self):
        self._pos = self._checkpoints.pop()
    
    def has_checkpoint(self):
        return len(self._checkpoints) != 0

class SelfSolvingBoard:
    def __init__(self, board: Board) -> None:
        self._board = board
        self._hqueue = HistoricQueue(board.get_all_positions())

        self._first_positions = board.valid_first_positions()
        self._num_first_positions = len(self._first_positions)
        self._position_iter = 0

        self._rowcount = board.n+1
        

    
    def _get_first_placement(self):
        self._position_iter += 1
        return self._first_positions[self._position_iter]
    
    def _has_placements(self):
        return self._position_iter < self._num_first_positions
    
    def _find_solution_set(self):
        firstpos = self._get_first_placement()




def place_all(
        board: Board,
        hqueue: HistoricQueue,
        first_placement: Point,
        num_to_place: int
    ):
    board.init_cycle(first_placement)
    solutions = []
    placed = 1
    while True:
        if placed == num_to_place:
            full_board = hqueue.checkout() + [first_placement]
            solutions.append(full_board)
            placed = 1
        if hqueue.has_next():
            place(board,hqueue.next())
        if not hqueue.has_next():
            hqueue.checkout()
            return solutions
        did_place = board.try_place(hqueue.next())
        if did_place: 
            placed += 1;
            hqueue.checkpoint_prev()

#def place(board,point):
#            did_place = board.try_place(hqueue.next())
#            if did_place: 
#                placed += 1;
#                hqueue.checkpoint_prev()


if True:
    rowcount = int(sys.argv[1])
    board = Board(rowcount)
    solution = SelfSolvingBoard(board)
    for point in starting_positions:
        results = place_all(board,hqueue,point,rowcount)
        answers += results
    print(answers)
