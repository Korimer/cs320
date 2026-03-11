# pyright: basic


from math import ceil, log
from typing import override


class HistoricNum:
    orig_num: int
    cur_num: int
    def __init__(self, orig_num):
        self.orig_num = orig_num
        self.cur_num = orig_num

    def __repr__(self) -> str:
        return f"HN({self.orig_num})"
    
    @override
    def __str__(self) -> str:
        return f"HistoricNum(cur: {self.cur_num}, orig: {self.orig_num})"


def getRadixes(list: list[HistoricNum], base: int) -> tuple[list[HistoricNum], ...]:
    print(f"list is: {list}")

    prefixes = tuple([[] for _ in range(base)])

    for num in list:
        quotient, divisor = divmod(num.cur_num, base)
        print(f"divisor of {num.cur_num} is {divisor}")
        num.cur_num = divisor
        prefixes[quotient].append(num)

    print(f"returning list: {prefixes}")

    return prefixes


def getMaxIterations(all_nums: list[int], base: int) -> int:
    return ceil(log(max(all_nums), base))


def radixHelper(numlist: list[HistoricNum], base: int, iter_count: int):
    if iter_count == 0: return numlist
    return [
        radixHelper(digit, base, iter_count-1)
        for digit in getRadixes(numlist, base)
    ]


def unfoldNTimes(list, times):
    unfolded = list
    for _ in range(times):
        unfolded = [
            itm
            for innerlist in unfolded
            for itm in innerlist
        ]
    return unfolded


def radix_base(values_to_sort: list[int], base: int):
    max_depth = getMaxIterations(values_to_sort, base)
    historicnums = [ HistoricNum(num) for num in values_to_sort ]
    sorted = radixHelper(historicnums, base, max_depth)
    print(sorted)
    unfolded = unfoldNTimes(sorted, max_depth)
    return unfolded


print(radix_base([50,55,12,3,54],10))
