# pyright: basic


from math import ceil, log


def getRadixes(list: list[int]) -> tuple[list[int],...]:

    prefixes = tuple([[] for _ in range(9)])

    for num in list:
        quotient, divisor = divmod(num,10)
        prefixes[quotient].append(divisor)

    return prefixes


def getMaxIterations(all_nums: list[int], base: int) -> int:
    return ceil(log(max(all_nums),base)) -1


def radixHelper(numlist, iter_count):
    if iter_count == 0: return numlist
    return [
        radixHelper(digit,iter_count-1)
        for digit in getRadixes(numlist)
    ]


def unfoldNTimes(list,times):
    unfolded = list
    for _ in range(times):
        unfolded = [
            itm
            for innerlist in unfolded
            for itm in innerlist
        ]
    return unfolded


def radix_base(values_to_sort,base):
    max_depth = getMaxIterations(values_to_sort,base)
    sorted = radixHelper(values_to_sort,max_depth)
    unfolded = unfoldNTimes(sorted,max_depth)
    sort_desc = unfolded[::-1]
    return sort_desc
