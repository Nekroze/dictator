from nekrobox.docdecs import params


class CardField(object):
    """
    An array of cards of limited size that provides storage.

    provides a list of card slots (None or a card) and the boolean values
    ``full`` and ``overflow``.
    """

    @params(size=(int, "Maximum size of this field"))
    def __init__(self, size):
        self.size = size
        self.cards = [None] * size
        self.full = False
        self.overflow = False

    @params(size=(int, "New maximum size of this field"))
    def change_size(self, size):
        """
        Change field size and recheck ``full`` and ``overflow`` after trimming
        where needed.
        """
        if size > self.size:
            self.cards.extend([None] * (size - self.size))
        elif size < self.size:
            if self.full:
                self.overflow = True

            while size < len(self.cards):
                try:
                    self.cards.remove(None)
                except ValueError:
                    break
        self.size = size

    @params(index=(int, "Index of card to be removed"))
    def remove_card_index(self, index):
        """Remove the card at the given index."""
        if self.overflow:
            self.cards.remove(self.cards[index])
            if self.size == len(self.cards):
                self.overflow = False
        else:
            self.cards[index] = None
            self.full = False

    @params(card=(int, "Card to be removed from this field"))
    def remove_card(self, card):
        """Remove the given card."""
        if self.overflow:
            self.cards.remove(card)
            if self.size == len(self.cards):
                self.overflow = False
        else:
            self.cards[self.cards.index(card)] = None
            self.full = False

    @params(card=(int, "Card to be added to this field"))
    def add_card(self, card):
        """Add the given card."""
        if self.full:
            self.cards.append(card)
            self.overflow = True
        else:
            self.cards[self.cards.index(None)] = card
            self.full = None not in self.cards

