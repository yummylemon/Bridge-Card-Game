from functools import total_ordering
import random

@total_ordering
class Card(object):
    """one card"""

    def __init__(self, suite, face):
        self._suite = suite
        self._face = face

    @property
    def face(self):
        return self._face

    @property
    def suite(self):
        return self._suite

    def __str__(self):
        if self._face == 14:
            face_str = 'A'
        elif self._face == 11:
            face_str = 'J'
        elif self._face == 12:
            face_str = 'Q'
        elif self._face == 13:
            face_str = 'K'
        else:
            face_str = str(self._face)
        return '%s%s' % (self._suite, face_str)
    
    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return self.__str__() == other.__str__()

    def __lt__(self, other):
        return self.__str__() < other.__str__()


class Poker(object):
    """a suite of cards"""

    def __init__(self):
        self._cards = [Card(suite, face) 
                       for suite in '♠♥♣♦'
                       for face in range(2, 15)]
        self._current = 0

    @property
    def cards(self):
        return self._cards

    def shuffle(self):
        """randomly shuffle"""
        self._current = 0
        random.shuffle(self._cards)

    @property
    def next(self):
        """deal"""
        card = self._cards[self._current]
        self._current += 1
        return card

    @property
    def has_next(self):
        """without a card"""
        return self._current < len(self._cards)


class Player(object):
    """player"""

    def __init__(self, name):
        self._name = name
        self._cards_on_hand = []

    @property
    def name(self):
        return self._name

    @property
    def cards_on_hand(self):
        return self._cards_on_hand

    def get(self, card):
        """摸牌"""
        self._cards_on_hand.append(card)

    def arrange(self, card_key):
        """玩家整理手上的牌"""
        self._cards_on_hand.sort(key=card_key)

    """回傳手牌中有的花色   e.g：['♠', '♣', '♥', '♦']"""
    def suites_on_hand(self):
        suites = []
        for card in self._cards_on_hand:
            if card.suite not in suites:
                suites.append(card.suite)
        return suites 

    """列出某種花色的手牌"""
    def find_suite(self, suite):
        suites = []
        
        if suite == -1:
            return suites
        
        for card in self._cards_on_hand:
            if card.suite == suite:
                suites.append(card)

        return suites


    def __str__(self):
        return self._name
    
    def __repr__(self):
        return self.__str__()


# Ｓort-先根據花色再根據點數排序
def get_key(card):
    return (card.suite, card.face)

def main():
    p = Poker()
    p.shuffle()
    players = [Player('East'), Player('West'), Player('South'), Player('North')]
    for _ in range(13):
        for player in players:
            player.get(p.next)

    for player in players:
        print(player.name + ':', end=' ')
        player.arrange(get_key)
        print(player.cards_on_hand)


if __name__ == '__main__':
    main()
