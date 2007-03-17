import pygame
import pygame.font
import pygame.display
from pygame.locals import *

from locals import *
from graphics import *

class RenderEngine:
    def __init__(self, game):
        pygame.font.init()
        pygame.display.init()
        self.scr = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT),DOUBLEBUF)
        self.bg = pygame.Surface(self.scr.get_rect().size)
        
        self.dirty_fields = None
        
        self.game = game
        self.game.render_engine = self
        
        self.preparebg();
        self.drawbg();
        #self.drawplayer()
        #pygame.Surface.blit (self.scr, self.bg, (0,0))
        #self.scr.blit(self.bg,((0,0),(100,100)))
    
    def update(self):
        if not self.game.dirty:
            self.dirty_fields = self.game.prepare_draw()
            self.drawbg_update()
            self.game.draw(self.scr)
        else:
            self.drawbg()
            self.game.dirty = False
        #self.drawplayer()
    
    def preparebg(self):
        self.bg.blit(load_image(img_sidebg), pos_sidebg)
        self.bg.blit(load_image(img_battlefield_top), pos_battlefield_top)
        self.bg.blit(load_image(img_battlefield_bottom), pos_battlefield_bottom)
        
    def drawbg(self):
        self.drawsidebg()
        self.drawbattlefieldtop()
        self.drawbattlefieldbottom()
    
    def drawbg_update(self):
        if self.dirty_fields is not None:
            for r in self.dirty_fields:
                #print r
                pos = r.topleft
                #r.topleft = (0,0)
                pygame.Surface.blit(self.scr, self.bg, pos, r)
            
            #self.scr.blit(self.bg, self.dirty_fields)
    
    def drawbattlefieldtop(self):
        self.scr.blit(load_image(img_battlefield_top), pos_battlefield_top)
    
    def drawbattlefieldbottom(self):
        self.scr.blit(load_image(img_battlefield_bottom), pos_battlefield_bottom)
        
    def drawsidebg(self):
        self.scr.blit(load_image(img_sidebg), pos_sidebg)
        
    #def drawplayer(self):
    #    draw_text(self.scr, 'HP: %s' % self.game.player.hp, pos_player_hp)
        
        
        
        
        
        
        