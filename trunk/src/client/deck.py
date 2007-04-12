import random

import pygame
from pygame.locals import *
from locals import *

from deskobject import DeskObject
from card import Card
from graphics import load_image
from cardinfolib import *
from objfactory import ObjFactory

from librarymgr import LibraryMgr

class Deck(DeskObject):
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
        self.rect.topleft = pos_library
        self.old_rect = pygame.Rect(self.rect)
        
        # set state
        self.status = DECK_STATUS_INUSE
        self.zindex = DECK_ZINDEX
        
        self.reset()
        
    def load(self, libfile):
        self.cards = LibraryMgr().load(libfile)
        
        for card in self.cards:
            card.game = self.game
            self.game.obj_factory.reg_card(card)
            self.game.send_net_event("add_lib_card %s %s" % (card.info.id, card.objid))
            self.set_card_status(card)
    
    def update(self):
        pass
        #if self.onmouse:
        #    self.rect.center = pygame.mouse.get_pos()
        #    self.dirty = True
            
    def sendmsg(self, msg, game):
        if msg == MOUSEBUTTONDOWN_LEFT:
            if self.status == DECK_STATUS_PREPARE:
                DeskObject.sendmsg(self, msg, game)
            else: # DECK_STATUS_INUSE
                # Correct One         
                #card = self.pop_card()
                #if card is not None:
                #    #game.add_deskcard(card, onmouse=True)
                #    game.add_handcard(card, self.rect.topleft)
                
                # For TEST
                #game.select_deck()
                
                # TODO : pop card on mouse face down. not directly draw to hand
                pass
        elif msg == MOUSEBUTTONDOWN_RIGHT:
            game.view_collection(self)
            game.say("Viewing library.")

    def gen_rand(self):
        self.cards = []
        for info in CILS().lib.values():
            card = ObjFactory().create_card(0, info=info)
            self.cards.append (card)
        random.shuffle(self.cards)
        
    def pop_card(self):
        if len(self.cards) > 0:
            return self.cards.pop(0)
        else:
            return None
        
    def set_cards(self, cards):
        self.cards = list(cards)
        for card in self.cards: self.set_card_status(card)
        
    def set_card_status(self, card):
        card.rect.center = self.rect.center
        card.status = CARD_STATUS_INLIB
        card.dirty = False

    #def set_status(self, status):
    #    self.status = status

    def shuffle(self):
        random.shuffle(self.cards)
        
    def reset(self):
        #for card in self.cards: card.remove_dirty = True
        self.cards = []
        self.dirty = True
        self.objs.add (self)