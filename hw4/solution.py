# pyright: basic

from math import ceil, log


def getMaxIterations(all_nums: list[int], base: int) -> int:
    max_num = max(all_nums)
    iterations = 0
    while max_num > 0:
        iterations += 1
        max_num = max_num // base
    return iterations


def radixHelper(numlist: list[int], base: int, iter_count: int):
    if iter_count == 0:
        return numlist

    tiered_sorted = numlist
    for exponent in range(iter_count):
        num_place = base**exponent
        starts_with = [[] for _ in range(base)]

        for num in tiered_sorted:
            digit = (num // num_place) % base
            starts_with[digit].append(num)

        tiered_sorted = [
            sorted_num
            for group in starts_with
            for sorted_num in group
        ]

    return tiered_sorted


def radix_base(values_to_sort: list[int], base: int):
    if len(values_to_sort) == 0:
        raise ValueError()
    if base <= 1 or not isinstance(base, int):
        raise ValueError()
    for val in values_to_sort:
        if not isinstance(val, int) or val < 0:
            raise ValueError()

    max_depth = getMaxIterations(values_to_sort, base)
    sorted = radixHelper(values_to_sort, base, max_depth)

    return sorted
