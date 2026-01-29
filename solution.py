# pyright: basic
class board:
    def __init__(self,n: int) -> None:
        trve = lambda count : [ True ] * count
        self.cols = trve(n)
        self.rows = trve(n)
        # https://www.desmos.com/calculator/dphqw7ulfz
        diag_count = -1
        self.diag_a = trve(diag_count) # ///
        self.diag_b = trve(diag_count) # \\\
    
    def place(self,x,y) -> None:

