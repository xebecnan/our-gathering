
import time

import pygame
from pygame.locals import *

from locals import *
from graphics import *
from deskobject import DeskObject
from igoto import IGoto

class Message(IGoto):
    def __init__(self, msg, group, pool):
        IGoto.__init__(self)
        self.group = group
        self.pool = pool
        
        # set image
        self.image = pygame.Surface((200,MESSAGE_HEIGHT))
        self.image.fill((0,0,0))
        draw_text(self.image, msg, (5,3), fg=(255,255,0), bg=None)
        
        # set rect
        self.rect = self.image.get_rect()
        self.rect.topleft = pos_message
        self.old_rect = pygame.Rect(self.rect)
        
        self.birth = time.time()
        self.life = MESSAGE_LIFE
        self.zindex = MESSAGE_ZINDEX
        
    def update(self):
        if time.time() - self.birth > self.life:
            self.remove_dirty = True
        else:
            IGoto.update(self)
            
    def removecallback(self):
        self.pool.remove(self)
        self.group.remove(self)
        
    def sendmsg(self, msg, game):
        pass