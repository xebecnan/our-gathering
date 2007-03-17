
import pygame

from locals import *
from deskobject import DeskObject

class GraveYard(DeskObject):
    def __init__(self, game, objs):
        DeskObject.__init__(self)
        
        self.game = game
        self.objs = objs
        
        # generate image
        self.image = pygame.Surface(size_small)
        self.image.fill(pygame.color.Color('#ff0000'))
        
        # set rect
        self.rect = self.image.get_rect()
        self.rect.topleft = pos_graveyard
        self.old_rect = pygame.Rect(self.rect)
        
        # set state
        self.zindex = GRAVEYARD_ZINDEX
        self.reset()
        
    def update(self):
        pass
        
    def reset(self):
        self.cards = []
        self.dirty = True
        self.objs.add(self)
    
    def sendmsg(self, msg, game):
        if msg == MOUSEBUTTONDOWN_LEFT:
            pass
        elif msg == MOUSEBUTTONDOWN_RIGHT:
            pass
        
    def add_card(self, card):
        self.cards.append(card)
        self.set_card_status(card)
        
    def set_cards(self, cards):
        self.cards = list(cards)
        for card in self.cards: self.set_card_status(card)
        
    def set_card_status(self, card):
        card.rect.center = self.rect.center
        card.status = CARD_STATUS_INLIB
        card.dirty = False