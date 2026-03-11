# pyright: basic


from math import ceil, log


class HistoricNum:
    orig_num: int
    cur_num: int
    def __init__(self, orig_num, cur_num):
        self.orig_num = orig_num
        self.cur_num = cur_num


def getRadixes(list: list[HistoricNum], base) -> tuple[list[HistoricNum], ...]:

    prefixes = tuple([[] for _ in range(base-1)])

    for num in list:
        quotient, divisor = divmod(num.cur_num, base)
        num.orig_num = divisor
        prefixes[quotient].append(num)

    return prefixes


def getMaxIterations(all_nums: list[int], base: int) -> int:
    return ceil(log(max(all_nums), base)) -1


def radixHelper(numlist, base, iter_count):
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


def radix_base(values_to_sort, base):
    max_depth = getMaxIterations(values_to_sort, base)
    sorted = radixHelper(values_to_sort, base, max_depth)
    unfolded = unfoldNTimes(sorted, max_depth)
    sort_desc = unfolded[::-1]
    return sort_desc
