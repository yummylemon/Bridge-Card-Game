from card import *

def random_choose(person, num, suite_for_this_turn=-1):  # 出牌的人，它剩幾張牌
    cards_on_hand_for_a_suite = person.find_suite(suite_for_this_turn)
    # 第一個出牌，還沒有決定本回合的花色

    if num == 1:
        card_choosed = person.cards_on_hand[0]

    elif len(cards_on_hand_for_a_suite) == 0:
        card_choosed = person.cards_on_hand[random.randint(0, num-1)]

    else:
        card_choosed = cards_on_hand_for_a_suite[random.randint(
            0, len(cards_on_hand_for_a_suite)-1)]

    person.cards_on_hand.remove(card_choosed)

    return card_choosed

class smart(Player):
	def __init__(self, name):
		super().__init__(name)

	def fst_turn_decide(self, king): # 第一個出牌
		return random_choose(self, len(self.cards_on_hand), king)

	def decide(self): # 非第一個出牌
		pass

if __name__ == '__main__':
	AA = person_smart("AA")
	print(AA.name)
	print(AA._cards_on_hand)

# information:
# card on this turn (and biggest)
# king 
# probability of others' main card
