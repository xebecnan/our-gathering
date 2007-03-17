
import pygame

from locals import *
from deskobject import DeskObject

class OpponentGraveYard(DeskObject):
    def __init__(self, game, objs):
        DeskObject.__init__(self)
        
        self.game = game
        self.objs = objs
        
        # generate image
        self.image = pygame.Surface(size_small)
        self.image.fill((0,255,0))
        
        # set rect
        self.rect = self.image.get_rect()
        self.rect.topleft = pos_opponent_graveyard
        self.old_rect = pygame.Rect(self.rect)
        
        # set state
        self.zindex = OPPONENT_GRAVEYARD_ZINDEX
        self.reset()
        
    def reset(self):
        self.cards = []
        self.dirty = True
        self.objs.add (self)
    
    def sendmsg(self, msg, game):
        pass