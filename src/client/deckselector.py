
import os

import pygame

from locals import *
from graphics import *
from deskobject import DeskObject

class DeckSelectorItem(DeskObject):
    def __init__(self, objs, libfile):
        DeskObject.__init__(self)
        self.objs = objs
        self.libfile = libfile
        
        # set image
        self.image = self.image_normal = pygame.Surface(SIZE_DECK_SELECTOR_ITEM)
        self.image_normal.fill ((0,0,0))
        draw_text(self.image_normal, libfile, (5,3))
        self.image_hilight = pygame.Surface(SIZE_DECK_SELECTOR_ITEM)
        self.image_hilight.fill ((255,0,0))
        draw_text(self.image_hilight, libfile, (5,3))
        
        # set rect
        self.rect = self.image.get_rect()
        self.rect.topleft = pos_deckselectoritem
        self.old_rect = pygame.Rect(self.rect)
        
        # set others
        self.zindex = DECK_SELECTOR_ITEM_ZINDEX
        self.dirty = True
        objs.add (self)
        
    def update(self):
        pass
    
    def removecallback(self):
        self.objs.remove(self)
        
    def hilight(self):
        self.image = self.image_hilight
        self.dirty = True
    
    def normal(self):
        self.image = self.image_normal
        self.dirty = True
        
    def sendmsg(self, msg, game):
        if msg == MOUSE_HOVER:
            self.hilight()
        elif msg == MOUSE_UNHOVER:
            self.normal()
        elif msg == MOUSEBUTTONDOWN_LEFT:
            game.load_deck(self.libfile)

class DeckSelector(DeskObject):
    def __init__(self, objs):
        DeskObject.__init__(self)
        self.objs = objs
        
        # set image
        self.image = pygame.Surface(SIZE_DECK_SELECTOR)
        self.image.fill ((0,0,0))
        
        # set rect
        self.rect = self.image.get_rect()
        self.rect.topleft = pos_deckselector
        self.old_rect = pygame.Rect(self.rect)
        
        # set buttons
        self.up_rect = pygame.Rect(0, 0, SIZE_DECK_SELECTOR[0], 10)
        self.down_rect = pygame.Rect(0, SIZE_DECK_SELECTOR[1]-10, SIZE_DECK_SELECTOR[0], 10)
        
        pygame.draw.rect (self.image, (255,0,0), self.up_rect)
        pygame.draw.rect (self.image, (255,0,0), self.down_rect)
        
        # set states
        self.items = []
        self.relative_top = 0
        self.vy = 0
        self.zindex = DECK_SELECTOR_ZINDEX
        
        self.hide()
    
    def load(self):
        self.clear()
        files = os.listdir(DECKS_DIR)
        for f in files:
            item = DeckSelectorItem(self.objs, f)
            self.add (item)
    
    def update(self):
        if self.relative_top > 0 and self.vy > 0: self.vy = 0
        elif self.relative_top+self.len() < SIZE_DECK_SELECTOR[1]-20 and self.vy < 0: self.vy = 0
        
        if self.vy != 0:
            for item in self.items:
                item.rect.move_ip(0, self.vy)
            self.relative_top += self.vy
            self.dirty = True
    
    def removecallback(self):
        self.objs.remove(self)
        
    def clear(self):
        self.items = []
        
    def add(self, item):
        index = len(self.items)
        item.rect.topleft = self.calc_pos(index)
        self.items.append(item)
        
    def show(self):
        self.objs.add (self)
        self.dirty = True
    
    def hide(self):
        for item in self.items:
            item.remove_dirty = True
        self.remove_dirty = True
        
    def sendmsg(self, msg, game):
        if msg == MOUSE_HOVER:
            pos = pygame.mouse.get_pos()
            rx,ry = self.relative_pos(pos)
            
            if self.up_rect.collidepoint (rx, ry):
                if self.relative_top < 0:
                    self.vy = 10
            elif self.down_rect.collidepoint (rx, ry):
                if self.relative_top + self.len() > SIZE_DECK_SELECTOR[1]-20:
                    self.vy = -10
            else:
                self.vy = 0
        elif msg == MOUSE_UNHOVER:
            self.vy = 0
    
    def relative_pos(self, pos):
        x = pos[0] - self.rect.left
        y = pos[1] - self.rect.top
        return x,y
    
    def len(self):
        item_num = len(self.items)
        return item_num * (SIZE_DECK_SELECTOR_ITEM[1]+DECK_SELECTOR_ITEM_SPACING)
    
    def calc_pos(self, index):
        x = self.rect.x + 10
        y = self.rect.y + 10 - self.relative_top + index*(SIZE_DECK_SELECTOR_ITEM[1]+DECK_SELECTOR_ITEM_SPACING)
        return (x,y)