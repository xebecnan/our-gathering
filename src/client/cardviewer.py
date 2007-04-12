import pygame
from pygame.locals import *

from locals import *
from graphics import *
from cardinfolib import *
from deskobject import DeskObject

class CardViewer(DeskObject):
    def __init__(self, objs):
        DeskObject.__init__(self)
        self.objs = objs
        
        self.image = load_image(img_cardback)
        self.rect = self.image.get_rect()
        self.old_rect = pygame.Rect(self.rect)
        self.old_pos = self.rect.topleft = pos_cardviewer
        
        self.bg_prepared = False
        self.dirty = True
        
        self.card_id = -1
        self.zindex = -1
        self.status = CARDVIEWER_STATUS_HIDE
        
    def setcard(self, card_id):
        if self.status == CARDVIEWER_STATUS_HIDE or self.card_id != card_id:
            self.card_id = card_id
            self.image = load_image(CILS().cardinfo(card_id).image)
            self.rect = self.image.get_rect()
            self.rect.topleft = pos_cardviewer
            self.dirty = True
            self.objs.add(self)
            self.status = CARDVIEWER_STATUS_SHOW
            
    def hide(self):
        self.remove_dirty = True
        
    def removecallback(self):
        self.objs.remove(self)
        self.status = CARDVIEWER_STATUS_HIDE
            
    def sengmsg(self, msg, game):
        pass