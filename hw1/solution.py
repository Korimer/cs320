# pyright: basic


class Point:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    def tup(self) -> tuple[int, int]:
        return self.x, self.y

    def __str__(self) -> str:
        return f"Point{repr(self)}"

    def __repr__(self) -> str:
        return f"({self.x},{self.y})"

class HistoricStrip:
    def __init__(self, count: int) -> None:
        self.full_row = [True] * count
        self.history = []

    def set(self, n: int) -> None:
        did_change = self.can_set(n)
        self.history.append(
                n if did_change else -1
            )
        self.full_row[n] = False

    def can_set(self, n: int) -> bool:
        return self.full_row[n]

    def unset(self) -> None:
        modified = self.history.pop()
        if modified != -1:
            self.full_row[modified] = True

    def __str__(self) -> str:
        return f"{self.full_row}: {self.history}"


class Board:
    def __init__(self, n: int) -> None:
        self.n = n
        self._cols = HistoricStrip(n)
        self._rows = HistoricStrip(n)

        diag_count = (2*n)-1
        self._diag_a = HistoricStrip(diag_count) # ///
        self._diag_b = HistoricStrip(diag_count) # \\\

        self._old_placements = []

    def try_place(self, point) -> bool:
        valid = self.can_place(point)
        if valid: self._place(point)
        return valid
    
    def _place(self, point) -> None:
        self._old_placements.append(point)
        x,y = point.tup()
        self._cols.set(x)
        self._rows.set(y)
        self._diag_a.set(x+y)
        self._diag_b.set(self.n-1+x-y)

    def can_place(self, point) -> bool:
        x, y = point.tup()
        return (
            self._cols.can_set(x)
            and self._rows.can_set(y)
            and self._diag_a.can_set(x+y)
            and self._diag_b.can_set(self.n-1+x-y)
        )

    def checkout_placements(self) -> list[Point]:
        return self._old_placements.copy()

    def undo_last_place(self):
        self._rows.unset()
        self._cols.unset()
        self._diag_a.unset()
        self._diag_b.unset()
            
        self._old_placements.pop()

def nQueensAll(rowcount):
    if rowcount < 4:
        raise ValueError("There exist no solutions for n<.4")
    solutions = []
    board = Board(rowcount)

    def _recurse(row, board: Board):
        if row == rowcount:
            solutions.append(board.checkout_placements())
            return
        for col in range(rowcount):
            if board.try_place(Point(row, col)):
                _recurse(row+1, board)
                board.undo_last_place()

    _recurse(0, board)

    return [
            [pnt.tup() for pnt in solution]
            for solution in solutions
           ]
