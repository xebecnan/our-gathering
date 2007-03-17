from deck import Deck
from hand import Hand
from graveyard import GraveYard
from battlefield import BattleField

class Player:
    def __init__(self):
        #self.hand = Hand()
        #self.grave_yard = GraveYard()
        #self.deck = Deck()
        #self.battlefield = BattleField()
        self.reset()
        
    def reset(self):
        self.hp = 20
        #self.deck.reset()
        #self.grave_yard.clear()
        #self.battlefield.clear()
        #self.hand.clear()