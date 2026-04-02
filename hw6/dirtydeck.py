#pyright: basic
from playingcard import PlayingCard, CardSuit, _valid_rank_, _convert_to_rank, _card_str_
from collections.abc import Container
import unittest
import random


_full_deck_ = [PlayingCard(s, r) for s in CardSuit for r in range(1, 14)]


class DirtyDeck(Container):

    def __init__(self, *, hide=None):
        self.deck = _full_deck_.copy()
        self._deck_size = len(self.deck)
        self.hidden = None
        if hide is not None:
            if not _valid_rank_(hide):
                raise ValueError(f"{hide} is not a card rank")
            self.hidden = _convert_to_rank(hide)

    def __str__(self):
        retstr = ""
        for c in self.deck:
            retstr += f"{str(c)} "
        return retstr

    def __contains__(self, c):
        return c in self.deck

    def __len__(self):
        return len(self.deck)
    
    def __iter__(self):
        return iter(self.deck)

    def shuffle(self):
        self.deck = _full_deck_.copy()
        to_hide = {}
        for upper_bound in range(len(self.deck)-1,0,-1):
            swapfrom = self.deck[upper_bound]
            swaptarget = random.randint(0,upper_bound)
            swapto = self.deck[swaptarget]
            if swapfrom.rank == self.hidden:
                to_hide[_card_str_(swapfrom)] = swaptarget
            if swapto.rank == self.hidden:
                to_hide[_card_str_(swapto)] = upper_bound
            self.deck[upper_bound], self.deck[swaptarget] = swapto, swapfrom

        i = 0
        for location in to_hide.values():
            self.deck[location], self.deck[i] = self.deck[i], self.deck[location]
            i += 1

    def deal(self) -> PlayingCard:
        card = self.deck.pop()
        if len(self.deck) / self._deck_size < .25:
            raise ResourceWarning("low deck")
        return card
