# pyright: basic
from collections.abc import Collection
from math import e, modf, floor, sqrt
from itertools import filterfalse, chain
from copy import copy


# DO NOT CHANGE ANY CODE BETWEEN LINE X AND LINE Y
# ******* THIS IS LINE X ******************

GOLDEN = (1.0 + 5.0 * 0.5) / 2.0


def swap(a, b):
    return b, a


# ***************************************************
# why do we inherit from Collection rather than Set?
# because Set requires too many methods to be defined


class CuckooSet(Collection):

    # *** course helper routines *******
    def _hash2_(self, obj, table_size):
        try:
            h = hash(obj)  # may raise exception
        except Exception:
            raise TypeError("unhashable key")

        h %= table_size

        f1, _ = modf(h * e)
        f2, _ = modf(h * GOLDEN)
        h1 = floor(table_size * f1)
        h2 = floor(table_size * f2)
        if h1 == h2:
            h2 = (h2 + 7) % table_size
        return h1, h2

    def _members_(self, tab):  # returns iterator
        return filterfalse((lambda x: x is None), tab)

    def _allmembers_(self):
        return chain(self._members_(self.htab1), self._members_(self.htab2))

    # ** course methods ****

    def __init__(self, iter=[], *, s=128):
        if s < 4:
            raise ValueError("set size too small")
        self._size_ = s
        self._MAXSWAPS_ = floor(s * 0.6)
        self.htab1 = [None] * s
        self.htab2 = [None] * s
        for i in iter:
            self.add(i)

    def __len__(self):
        count1 = len(list(self._members_(self.htab1)))
        count2 = len(list(self._members_(self.htab2)))
        return count1 + count2

    def _resize_(self):
        oldself = copy(self)
        self.__init__(oldself, s=oldself._size_ * 2)

    def __str__(self):
        fstr = ""
        for v in self._allmembers_():
            if len(fstr):
                fstr += ", "
            fstr += str(v)
        return fstr

    def __iter__(self):
        return self._allmembers_()
# ******* THIS IS LINE Y ******************

    def __contains__(self, x) -> bool:
        if x is None:
            raise ValueError("key may not be None")
        h1, h2 = self._hash2_(x, self._size_)
        return self.htab1[h1] == x or self.htab2[h2] == x

    def add(self, x):
        if x is None:
            raise ValueError("key may not be None")

        if x in self:
            return

        swapcount = 0
        is_not_added = True
        target = x
        array_oscilator = True
        while is_not_added:
            if swapcount >= self._MAXSWAPS_:
                self._resize_()
                swapcount = 0
            h1, h2 = self._hash2_(target, self._size_)
            if array_oscilator:
                arr_target = self.htab1
                arr_pos = h1
            else:
                arr_target = self.htab2
                arr_pos = h2

            if arr_target[arr_pos] is None:
                arr_target[arr_pos] = target
                is_not_added = False
            else:
                old_target = target
                target = arr_target[arr_pos]
                arr_target[arr_pos] = old_target

            array_oscilator = not array_oscilator
            swapcount += 1

    def remove(self, x):
        if not self.discard(x):
            raise ValueError()

    def discard(self, x) -> bool:
        if x is None:
            raise ValueError("key may not be None")
        h1, h2 = self._hash2_(x, self._size_)
        if self.htab1[h1] == x:
            self.htab1[h1] = None
            return True
        elif self.htab2[h2] == x:
            self.htab2[h2] = None
            return True
        else:
            return False
