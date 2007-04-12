
#from random import shuffle
from og_random import shuffle

import pygame
from deskobject import DeskObject
from graphics import *
from locals import *

class CardCollectionViewer(DeskObject):
    def __init__(self, group):
        DeskObject.__init__(self)
        self.group = group
        
        # generate image
        self.image = None
        
        # set rect
        self.rect = None
        
        # set state
        self.vx = 0
        self.zindex = CARDCOLLECTION_VIEWER_ZINDEX
        self.length = 0
        self.left = 0
        self.cards = []
        
    def update(self):
        if self.left > 0 and self.vx > 0: self.vx = 0
        elif self.left + self.length < SCREEN_WIDTH and self.vx < 0: self.vx = 0
        
        if self.vx != 0:
            for card in self.cards:
                card.rect.move_ip (self.vx, 0)
            self.left += self.vx
            self.dirty = True
    
    def load_cards(self, cards_provider):
        self.cards_provider = cards_provider
        cards = self.cards = list(cards_provider.cards)
        cardsnum = len(cards)
        h = size_small[1] + 60
        #w = 20 + (cardsnum * (size_small[0]+20))
        w = SCREEN_WIDTH
        self.image = pygame.Surface((w,h))
        self.image.fill(pygame.color.Color('#333333'))
        #pygame.draw.rect (self.image, pygame.color.Color('#ff0000'), pygame.Rect(380,CARDCOLLECTION_VIEWER_TOP+25+size_small[1],40,20))
        
        top = 30+size_small[1]
        self.shufflerect = pygame.Rect(SCREEN_WIDTH/2-91,top,80,25)
        self.closerect   = pygame.Rect(SCREEN_WIDTH/2+10,top,80,25)
        self.leftrect    = pygame.Rect(0,  top,40,25)
        self.rightrect   = pygame.Rect(SCREEN_WIDTH-41,top,40,25)
        
        pygame.draw.rect (self.image, (255,0,0), self.shufflerect)
        pygame.draw.rect (self.image, (255,0,0), self.closerect)
        pygame.draw.rect (self.image, (255,0,0), self.leftrect)
        pygame.draw.rect (self.image, (255,0,0), self.rightrect)
        
        draw_text(self.image, 'SHUFFLE', (SCREEN_WIDTH/2-78,top+1), bg=None)
        draw_text(self.image, 'CLOSE', (SCREEN_WIDTH/2+28,31+size_small[1]), bg=None)
        draw_text(self.image, '<-', (11, 31+size_small[1]), bg=None)
        draw_text(self.image, '->', (SCREEN_WIDTH-30, 31+size_small[1]), bg=None)
        #for i in range(cardsnum):
        #    x = 20 + (i * (size_small[0]+20))
        #    self.image.blit (cards[i].image, (x,20))
        self.rect = self.image.get_rect()
        self.rect.topleft = (0,CARDCOLLECTION_VIEWER_TOP)
        self.old_rect = pygame.Rect(self.rect)
        
        self.length = 20 + (cardsnum * (size_small[0] + 20))
        self.left = 0
        
        for i in range(cardsnum):
            card = cards[i]
            card.zindex = CARDCOLLECTION_VIEWER_ZINDEX+1
            card.rect.topleft = (20+(i*(size_small[0]+20)), CARDCOLLECTION_VIEWER_TOP+20)
            card.status = CARD_STATUS_INCOLLECTION
            card.group = self.group
            self.group.add(card)
    
    def adjust_pos(self):
        cardsnum = len(self.cards)
        for i in range(cardsnum):
            card = self.cards[i]
            x = self.left + 20+(i*(size_small[0]+20))
            y = CARDCOLLECTION_VIEWER_TOP+20
            card.goto((x,y), keep_zindex=True)
        
    def show(self):
        self.group.add(self)
        self.dirty = True
        
    def hide(self):
        for card in self.cards: self.group.remove(card)
        self.remove_dirty = True
        
    def removecallback(self):
        for card in self.cards:
            card.remove_dirty = True
        self.cards = []
        self.group.remove(self)
    
    def sendmsg(self, msg, game):
        if msg == MOUSE_HOVER:
            x,y = pygame.mouse.get_pos()
            y -= CARDCOLLECTION_VIEWER_TOP
            if self.leftrect.collidepoint(x,y):
                if self.left < 0:
                    self.vx = 32
            elif self.rightrect.collidepoint(x,y):
                if self.left+self.length >= SCREEN_WIDTH:
                    self.vx = -32
            else:
                self.vx = 0
        elif msg == MOUSE_UNHOVER:
            self.vx = 0
        elif msg == MOUSEBUTTONDOWN_LEFT:
            x,y = pygame.mouse.get_pos()
            y -= CARDCOLLECTION_VIEWER_TOP
            if self.closerect.collidepoint(x,y):
                self.hide()
                self.cards_provider.set_cards (self.cards)
                game.status = GAME_STATUS_NORMAL
                
                game.send_net_event("say Finish viewing.")
            elif self.shufflerect.collidepoint (x,y):
                self.hide()
                self.cards_provider.set_cards (self.cards)
                shuffle(self.cards_provider.cards)
                game.status = GAME_STATUS_NORMAL
                
                game.send_net_event("say Shuffled.")