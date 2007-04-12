
import pygame

from locals import *
from deskobject import DeskObject

class Referent(DeskObject):
    def __init__(self, containers=[]):
        DeskObject.__init__(self)
        self.containers = containers
        
        # set image
        self.image = pygame.Suroface((20,20))
        self.image.fill ((102,102,102))
        
        # set rect
        self.rect = self.image.get_rect()
        self.old_rect = pygame.Rect (self.rect)
        
        # set others
        self.color = COLOR_GREY
        
    def removecallback(self):
        for container in self.containers:
            container.remove(self)