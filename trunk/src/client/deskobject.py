import pygame
from pygame.locals import *
from locals import *

class DeskObject(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        
        self.dirty = True
        self.dirty_region = []
        self.remove_dirty = False
        
        self.old_zindex = self.__dict__['zindex'] = 0
        
        self.onmouse = False
        self.rel_pos = (0,0)
        
    def set_onmouse(self, onmouse):
            self.onmouse = onmouse
            x,y = pygame.mouse.get_pos()
            self.rel_pos = (self.rect.left - x, self.rect.top - y)
            
    def toggle_onmouse(self):
            self.onmouse = not self.onmouse
                
    def __setattr__(self, name, value):
            if name == 'zindex':
                    self.old_zindex = self.zindex
                    self.__dict__['zindex'] = value
            else:
                    self.__dict__[name] = value
                    
    def sendmsg(self, msg, game):
        if msg == MOUSEBUTTONDOWN_LEFT:
            self.toggle_onmouse()
            if self.onmouse:
                game.pickup(self)
            else:
                game.puttop(self)
                
    def removecallback(self):
        pass