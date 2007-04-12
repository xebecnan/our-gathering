import pygame

class RenderClearBg(pygame.sprite.RenderPlain):
    def draw(self, surface):
        for s in self.spritedict.keys():
            if not s.bg_prepared:
                s.bg = pygame.Surface(s.rect.size)
                s.bg.blit (surface, (0,0), s.rect)
                s.bg_prepared = True
                
            if s.dirty:
                surface.blit (s.bg, s.old_pos)
                
                if s.bg.get_rect().size != s.rect.size: s.bg = pygame.Surface(s.rect.size)
                
                s.bg.blit (surface, (0,0), s.rect)
                surface.blit (s.image, s.rect.topleft)
                s.dirty = False
        #pygame.sprite.RenderClear.draw(self, surface)
        
    #def clear(self, surface):
    #    for s, r in self.spritedict.items():
    #        surface.blit (s.bg, s.rect.topleft)