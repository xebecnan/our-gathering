import pygame
from locals import *

from cardgroup import CardGroup

def calc_pos_x(index):
    return HANDCARD_LEFT+(HANDCARD_SPACING+size_small[0])*index

def calc_index (x):
    if x < HANDCARD_LEFT: return 0
    return (x-HANDCARD_LEFT)/(HANDCARD_SPACING+size_small[0])+1

class HandCardGroup(CardGroup):
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
        
        self.cardnum += 1
        
        self.adjust_pos()
        
    def add_internal(self, card):
        CardGroup.add_internal(self, card)
        self._spritelist.append(card)
        
        pos = (calc_pos_x(self.cardnum), HANDCARD_TOP)
        card.goto(pos)
        card.zindex = HANDCARD_ZINDEX
        self.cardnum += 1
        
    def remove_internal(self, card):
        CardGroup.remove_internal(self, card)
        self._spritelist.remove(card)
        
        self.cardnum -= 1
        self.adjust_pos()
        
    def adjust_pos(self):
        for i in range(self.cardnum):
            card = self._spritelist[i]
            x = calc_pos_x(i)
            if card.rect.left != x:
                card.goto ((x, HANDCARD_TOP))