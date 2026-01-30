# pyright: basic

class Board:
    def __init__(self,n: int) -> None:
        self.n = n-1
        trues = lambda count : [ True ] * count
        self.cols = trues(n)
        self.rows = trues(n)
        # https://www.desmos.com/calculator/m6wlfbg2a6
        diag_count = (4*n)-2
        self.diag_a = trues(diag_count) # \\\
        self.diag_b = trues(diag_count) # ///

        # Assign permutations generations - whenever I find a valid permutation, mark the position of every queen with that generation.
        # Rule: you can never have two queens of the same generation within a new potential permutation.
        self.valid_mirrors = [ 
            [set() for _ in range(n)]
            for _ in range(n)
        ]
    
    def place(self,x,y) -> None:
        self.cols[x] = False
        self.rows[y] = False
        self.diag_a[x+y] = False
        self.diag_b[self.n+x-y] = False

    def can_place(self,x,y) -> bool:
        return (
            self.cols[x]
            and self.rows[y]
            and self.diag_a[x+y]
            and self.diag_b[self.n+x-y]
        )


