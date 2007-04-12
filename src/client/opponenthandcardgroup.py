import pygame
from locals import *

from cardgroup import CardGroup

def calc_pos_x(index):
    return HANDCARD_LEFT+(HANDCARD_SPACING+size_small[0])*index

def calc_index (x):
    if x < HANDCARD_LEFT: return 0
    return (x-HANDCARD_LEFT)/(HANDCARD_SPACING+size_small[0])+1

class OpponentHandCardGroup(CardGroup):
    def __init__(self, *sprites):
        self._spritelist = []
        CardGroup.__init__(self, *sprites)
        
        self.cardnum = 0
        
        
    def sprites(self): return list(self._spritelist)
        
    def add_at(self, card, pos):
        x = pos[0]
        index = calc_index (x)
        
        CardGroup.add_internal(self, card)
        self._spritelist.insert(index, card)
        card.add_internal(self)
        
        card.zindex = HANDCARD_ZINDEX
        card.status = CARD_STATUS_OPPONENT_INHAND
        card.set_face(False)
        card.set_inverse(True)
        
        self.cardnum += 1
        self.adjust_pos()
        
    def add_internal(self, card):
        CardGroup.add_internal(self, card)
        self._spritelist.append(card)
        
        pos = (calc_pos_x(self.cardnum), OPPONENT_HANDCARD_TOP)
        
        card.zindex = HANDCARD_ZINDEX
        card.status = CARD_STATUS_OPPONENT_INHAND
        card.set_face(False)
        card.set_inverse(True)
        
        self.cardnum += 1
        card.goto(pos, keep_zindex=True)
        
    def remove_internal(self, card):
        CardGroup.remove_internal(self, card)
        self._spritelist.remove(card)
        
        self.cardnum -= 1
        self.adjust_pos()
        
    def adjust_pos(self):
        for i in range(self.cardnum):
            card = self._spritelist[i]
            x = calc_pos_x(i)
            card.goto ((x, OPPONENT_HANDCARD_TOP))
            