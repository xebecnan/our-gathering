import pygame

#from renderclearbg import RenderClearBg

class CardGroup(pygame.sprite.RenderUpdates):
    #pass
    def prepare_draw(self):
        dirty_rects = []
        self.dirty_cards = []
        self.cards = self.sprites()
        
        self.cards.sort(cmp=lambda x,y:cmp(x.zindex, y.zindex))
        for s in self.cards:
            if s.remove_dirty:
                dirty_rects.append (s.old_rect)
                
                others = self.sprites_except(s)
                for oc in others:
                    if s.old_rect.colliderect (oc.rect):
                        tmp = oc.rect.clip(s.old_rect)
                        #print tmp
                        oc.dirty_region.append (tmp)
                        
                s.removecallback()
                s.remove_dirty = False
            elif s.dirty:
                dirty_rects.append (s.old_rect)
                
                others = self.sprites_except(s)
                for oc in others:
                    if s.old_rect.colliderect (oc.rect):
                        tmp = oc.rect.clip(s.old_rect)
                        #print tmp
                        oc.dirty_region.append (tmp)
                        if oc not in self.dirty_cards:
                            self.dirty_cards.append(oc)
                    if s.rect.colliderect(oc.rect):
                        tmp = oc.rect.clip(s.rect)
                        #print tmp
                        oc.dirty_region.append (tmp)
                        if oc not in self.dirty_cards:
                            self.dirty_cards.append(oc)
                        
                self.dirty_cards.append(s)
            elif len(s.dirty_region) > 0:
                self.dirty_cards.append(s)
                
        return dirty_rects
    
    def sprites_except(self, ex):
        others = list(self.sprites())
        others.remove(ex)
        return others
    
    def draw(self, surface):
        #cards = self.spritedict.keys()
        #cards.sort(cmp=lambda x,y:cmp(x.old_zindex,y.old_zindex), reverse=True)
        #for s in cards:
        #    if s.dirty and s.bg_prepared:
        #        surface.blit(s.bg, s.old_pos)
        
        #cards.sort(cmp=lambda x,y:cmp(x.zindex, y.zindex))
        #for s in [card for card in self.cards if len(card.dirty_region)>0 or card.dirty]:
            #if not s.bg_prepared:
            #    s.bg = pygame.Surface(s.rect.size)
            #    s.bg.blit (surface, (0,0), s.rect)
            #    s.bg_prepared = True
        self.dirty_cards.sort(cmp=lambda x,y:cmp(x.zindex,y.zindex))
        for s in self.dirty_cards:
            for r in s.dirty_region:
                pos = r.topleft
                #r.top = r.top - s.rect.top
                #r.left = r.left - s.rect.left
                r.move_ip(-s.rect.left,-s.rect.top)
                #r.move_ip(r.left-s.rect.left, r.top-s.rect.top)
                #r.topleft = (0,0)
                
                surface.blit(s.image, pos, r)
                #surface.blit(s.image, (0,0), r)
                
                s.dirty_region = []
            
            if s.dirty:
                #if s.bg.get_rect().size != s.rect.size: s.bg = pygame.Surface(s.rect.size)
                #s.bg.blit (surface, (0,0), s.rect)
                
                surface.blit (s.image, s.rect.topleft)
                s.dirty = False
            
            s.old_rect.topleft = s.rect.topleft
            s.old_rect.size = s.rect.size
        
        #for s in cards:
        #    if not s.bg_prepared:
        #        s.bg = pygame.Surface(s.rect.size)
        #        s.bg.blit (surface, (0,0), s.rect)
        #        s.bg_prepared = True
        #    if s.dirty:
        #        surface.blit (s.bg, s.old_pos)
        #        
        #        if s.bg.get_rect().size != s.rect.size: s.bg = pygame.Surface(s.rect.size)
        #        s.bg.blit (surface, (0,0), s.rect)
        #        
        #        surface.blit (s.image, s.rect.topleft)
        #        s.dirty = False
                
        #cards.reverse()
        