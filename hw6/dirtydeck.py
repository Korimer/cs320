#pyright: basic
from playingcard import PlayingCard, CardSuit, _valid_rank_, _convert_to_rank
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
        if self.hidden is not None:
            reserved_bottom = 4
            num_hidden = 0
        else:
            reserved_bottom = 0
        for upper_bound in range(self._deck_size-1,reserved_bottom-1,-1):
            swapcard = self.deck[upper_bound]
            if swapcard.rank == self.hidden:
                swaptarget = num_hidden
                num_hidden += 1
            else:
                swaptarget = random.randint(reserved_bottom,upper_bound)
            self.deck[upper_bound] = self.deck[swaptarget]
            self.deck[swaptarget] = swapcard

    def deal(self) -> PlayingCard:
        card = self.deck.pop()
        if len(self.deck) / self._deck_size < .25:
            raise ResourceWarning("low deck")
        return card

lol = DirtyDeck(hide=10)
lol.shuffle()
for card in lol.deck:
    print(card.rank)
