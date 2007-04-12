
import pygame

from locals import *
from graphics import *
from deskobject import DeskObject

class HPPanel(DeskObject):
    def __init__(self, objs, player, opponent):
        DeskObject.__init__(self)
        self.objs = objs
        self.player = player
        self.opponent = opponent
        
        # set image
        self.image = pygame.Surface(SIZE_HP_PANEL)
        self.update_image()
        
        # set rect
        self.rect = self.image.get_rect()
        self.rect.topleft = pos_hp_panel
        self.old_rect = pygame.Rect(self.rect)
        
        # set others
        self.zindex = HP_PANEL_ZINDEX
        self.reset()
        
    def update(self):
        pass
        
    def sendmsg(self, msg, game):
        pass
    
    def reset(self):
        self.update_image()
        self.dirty = True
        self.objs.add (self)
    
    def update_image(self):
        self.image.fill((0,0,0))
        pygame.draw.rect (self.image, (255,255,255), (0,25,50,25))
        draw_text(self.image, str(self.opponent.hp), (5,3))
        draw_text(self.image, str(self.player.hp), (5,28), fg=(0,0,0))
    
    def adjust_player_hp(self, hp_change):
        if hp_change != 0:
            self.player.hp += hp_change
            self.update_image()
            self.dirty = True
    
    def adjust_opponent_hp(self, hp_change):
        if hp_change != 0:
            self.opponent.hp += hp_change
            self.update_image()
            self.dirty = True