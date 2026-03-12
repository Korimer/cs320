# pyright: basic


from math import ceil, log
from typing import override


class HistoricNum:
    cur_exponent: int
    all_digits: list[int]
    orig_num: int

    def __init__(self, orig_num, max_digits, base):
        self.orig_num = orig_num
        self.all_digits = [ 0 for _ in range(max_digits) ]
        self.cur_exponent = 0

        cur_num = orig_num
        exponent = max_digits - 1
        while cur_num > 0:
            dividend, remainder = divmod(cur_num, base)
            cur_num = dividend
            self.all_digits[exponent] = remainder
            exponent -= 1


    def nextDigit(self) -> int:
        self.cur_exponent += 1
        return self.all_digits[self.cur_exponent-1]

    @override
    def __repr__(self) -> str:
        return f"HN({self.orig_num})"

    
    @override
    def __str__(self) -> str:
        return f"HistoricNum(digit {self.cur_exponent} of digits {self.all_digits}. Base number {self.orig_num})"


def getRadixes(list: list[HistoricNum], base: int) -> tuple[list[HistoricNum], ...]:
    prefixes = tuple([[] for _ in range(base)])

    for h_num in list:
        quotient = h_num.nextDigit()
        prefixes[quotient].append(h_num)

    return prefixes


def getMaxIterations(all_nums: list[int], base: int) -> int:
    return ceil(log(max(all_nums)+1, base))


def radixHelper(numlist: list[HistoricNum], base: int, iter_count: int):
    if iter_count == 0: return numlist
    return [
        radixHelper(digit, base, iter_count-1)
        for digit in getRadixes(numlist, base)
    ]


def unfoldNTimes(list, times) -> list[HistoricNum]:
    unfolded = list
    for _ in range(times):
        unfolded = [
            itm
            for innerlist in unfolded
            for itm in innerlist
        ]
    return unfolded


def radix_base(values_to_sort: list[int], base: int):
    if base <= 2 or not isinstance(base,int):
        raise ValueError()
    for val in values_to_sort:
        if isinstance(val,int):
            raise ValueError()

    max_depth = getMaxIterations(values_to_sort, base)
    historicnums = [ HistoricNum(num,max_depth,base) for num in values_to_sort ]
    sorted = radixHelper(historicnums, base, max_depth)
    unfolded = unfoldNTimes(sorted, max_depth)

    return [ h_num.orig_num for h_num in unfolded ]
