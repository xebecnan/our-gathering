
import pygame

from locals import *
from graphics import *
from deskobject import DeskObject

class OpponentDeck(DeskObject):
    def __init__(self, game, objs):
        DeskObject.__init__(self)
        
        self.game = game
        self.objs = objs
        
        # generate image for Deck
        bkimg = load_image(img_cardback)
        bkimg = pygame.transform.scale(bkimg, size_small)
        
        w,h = bkimg.get_rect().size
        self.image = pygame.Surface((w,h+20))
        for offset in range(10,25,5):
                self.image.blit(bkimg, (0,h+20-offset), (0,h-5,w,10))
        self.image.blit(bkimg, (0,0))
        
        # set rect
        self.rect = self.image.get_rect()
        self.rect.topleft = pos_opponent_library
        self.old_rect = pygame.Rect(self.rect)
        
        # set other states
        self.zindex = OPPONENT_DECK_ZINDEX
        self.reset()
        
    def add(self, card):
        self.cards.append (card)
        self.set_card_status(card)
        card.set_face(True)
        card.set_inverse(False)
        
    def remove(self, card):
        self.cards.remove (card)
        
    def set_cards(self, cards):
        self.cards = list(cards)
        for card in self.cards: self.set_card_status(card)
        
    def set_card_status(self, card):
        card.zindex = -1
        card.status = CARD_STATUS_OPPONENT_INLIB
        card.rect.center = self.rect.center
        
    def sendmsg(self, msg, game):
        if msg == MOUSEBUTTONDOWN_RIGHT:
            game.view_collection(self)
            game.say("Viewing your library...")
            
    def reset(self):
        self.cards = []
        self.dirty = True
        self.objs.add(self)