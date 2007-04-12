# -*- coding: gb2312 -*-

import pygame

from locals import *
from graphics import *
from deskobject import DeskObject

SIZE_WAIT_PLAYER_DIAGRAM = (200,80)

class WaitPlayerDiagram(DeskObject):
    def __init__(self, objs):
        DeskObject.__init__(self)
        self.objs = objs
        
        self.image = pygame.Surface(SIZE_WAIT_PLAYER_DIAGRAM)
        self.image.fill(pygame.color.Color('#333333'))
        
        self._exitrect = pygame.Rect(60,50,80,25)
        
        pygame.draw.rect (self.image, (255,0,0), self._exitrect)
        
        draw_text(self.image, 'Please wait for opponent.', (20,20), bg=None)
        draw_text(self.image, 'EXIT', (80,50), bg=None)
        
        self.rect = self.image.get_rect()
        self.rect.topleft = ((SCREEN_WIDTH-SIZE_WAIT_PLAYER_DIAGRAM[0])/2, (SCREEN_HEIGHT-SIZE_WAIT_PLAYER_DIAGRAM[1])/2)
        self.old_rect = pygame.Rect(self.rect)
        
        self._is_hilight = False
        
    def show(self):
        self.objs.add(self)
        self.dirty = True
        
    def hide(self):
        self.remove_dirty = True
        
    def update(self):
        pass
    
    def removecallback(self):
        self.objs.remove(self)
        
    def _hilight(self, r):
        if not self._is_hilight:
            pygame.draw.rect(self.image, (0,255,0), self._exitrect)
            draw_text(self.image, 'EXIT', (80,50), bg=None)
            self._is_hilight = True
            self.dirty = True
    
    def _normal(self, r):
        if self._is_hilight:
            pygame.draw.rect(self.image, (255,0,0), self._exitrect)
            draw_text(self.image, 'EXIT', (80,50), bg=None)
            self._is_hilight = False
            self.dirty = True
        
    def sendmsg(self, msg, game):
        if msg == MOUSE_HOVER:
            x,y = pygame.mouse.get_pos()
            x-=self.rect.left
            y-=self.rect.top
            if self._exitrect.collidepoint(x,y):
                self._hilight(self._exitrect)
            else:
                self._normal(self._exitrect)
        elif msg == MOUSE_UNHOVER:
            self._normal(self._exitrect)
        elif msg == MOUSEBUTTONDOWN_LEFT:
            x,y = pygame.mouse.get_pos()
            x-=self.rect.left
            y-=self.rect.top
            if self._exitrect.collidepoint(x,y):
                game.exit()