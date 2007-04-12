import random

import pygame
from pygame.locals import *
from locals import *

from deskobject import DeskObject
from graphics import load_image
from cardinfolib import *


class Card(DeskObject):
    backimage = None
    
    def __init__(self, card_id, info=None):
        DeskObject.__init__(self)
        
        if Card.backimage is None:
            Card.backimage = load_image(img_cardback)
            Card.backimage = pygame.transform.scale(Card.backimage, size_small)
        
        if info is None:
            self.info = CILS().cardinfo(card_id)
        else:
            self.info = info
        self.foreimage = load_image(self.info.image)
        self.foreimage = pygame.transform.scale(self.foreimage, size_small)
        
        self.image = self.foreimage
        self.rect = self.image.get_rect()
        self.old_rect = pygame.Rect(self.rect)
        
        #self.bg_prepared = False
        
        self.isfore = True
        self.istapping = False
        
        self.status = CARD_STATUS_ONDESK
        
        self.anim_status = CARD_ANIM_STATUS_NORMAL
        self.target_pos  = self.rect.topleft
        
        self.comefrom = CARD_FROM_NONE
        self.inverse = False
    
    def update(self):
        if self.onmouse:
            #self.old_rect.topleft = self.rect.topleft
            #self.old_rect.size = self.rect.size
            x, y = pygame.mouse.get_pos()
            self.rect.topleft = (self.rel_pos[0]+x,self.rel_pos[1]+y)
            #self.rect.center = pygame.mouse.get_pos()
            self.dirty = True
            #print self.old_rect
            #print self.rect
        elif self.anim_status == CARD_ANIM_STATUS_GOTO:
            def calc_v(dim_delta):
                if dim_delta == 0: return 0
                elif dim_delta > 150:  return -20
                elif dim_delta > 13:   return -10
                elif dim_delta > 5:    return -5
                elif dim_delta > 0:    return -1
                elif dim_delta > -6:   return 1
                elif dim_delta > -14:  return 5
                elif dim_delta > -151: return 10
                else:          return 20
            x,y = self.target_pos
            vx = calc_v(self.rect.left - x)
            vy = calc_v(self.rect.top  - y)
            if vx == 0 and vy == 0:
                if self.zindex_before_goto == -1:
                    self.game.settop(self)
                else:
                    self.zindex = self.zindex_before_goto
                self.anim_status = CARD_ANIM_STATUS_NORMAL
                self.dirty = True
            else:
                self.rect.move_ip(vx,vy)
                self.dirty = True
            
    def toggle_face(self):
        if self.isfore: self.image = Card.backimage
        else: self.image = self.foreimage
        
        if self.istapping: self.image = pygame.transform.rotate(self.image, -90)
        if self.inverse:   self.image = pygame.transform.rotate(self.image, 180)
        pos = self.rect.topleft
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
            
        self.isfore = not self.isfore
        self.dirty = True
        
    def set_face(self, is_fore):
        self.isfore = is_fore
        
        if is_fore:
            self.image = self.foreimage
        else:
            self.image = Card.backimage
            
        if self.istapping: self.image = pygame.transform.rotate(self.image, -90)
        if self.inverse:   self.image = pygame.transform.rotate(self.image, 180)
        pos = self.rect.topleft
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
            
        self.dirty = True
        
    def toggle_tapping(self):
        if not self.istapping:
            self.image = pygame.transform.rotate(self.image, -90)
        else:
            self.image = pygame.transform.rotate (self.image, 90)
        pos = self.rect.topleft
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.istapping = not self.istapping
        self.dirty = True
        
    def set_tapping(self, is_tapping):
        if self.istapping != is_tapping:
            self.istapping = is_tapping
            if is_tapping:
                self.image = pygame.transform.rotate(self.image, -90)
            else:
                self.image = pygame.transform.rotate (self.image, 90)
            pos = self.rect.topleft
            self.rect = self.image.get_rect()
            self.rect.topleft = pos
            self.dirty = True
            
    def set_inverse(self, is_inverse):
        if self.inverse != is_inverse:
            self.inverse = is_inverse
            self.image = pygame.transform.rotate(self.image, 180)
        
        
    def removecallback(self):
        #self.objs.remove(self)
        pass
        
    def goto(self, pos, keep_zindex = False):
        if self.anim_status == CARD_ANIM_STATUS_NORMAL and self.status == CARD_STATUS_ONDESK and self.zindex < CARD_DRAWOUT_ZINDEX:
            self.game.drawout(self, self)
        if self.anim_status == CARD_ANIM_STATUS_NORMAL:
            if keep_zindex:
                self.zindex_before_goto = self.zindex
            else:
                self.zindex_before_goto = -1
            self.zindex = CARD_GOING_ZINDEX
        self.anim_status = CARD_ANIM_STATUS_GOTO
        self.target_pos = pos
        
    def sendmsg(self, msg, game):
        if msg == MOUSE_HOVER:
            if self.status != CARD_STATUS_OPPONENT_INHAND:
                if (not self.inverse) or self.isfore:
                    game.view_detail(self)
            if self.status == CARD_STATUS_INHAND and self.anim_status == CARD_ANIM_STATUS_NORMAL:
                x = self.rect.left
                y = HANDCARD_OUT_TOP
                self.goto ((x,y))
                self.status = CARD_STATUS_INHAND_OUT
        elif msg == MOUSE_UNHOVER:
            if self.status != CARD_STATUS_OPPONENT_INHAND:
                if (not self.inverse) or self.isfore:
                    game.close_view_detail()
            if self.status == CARD_STATUS_INHAND_OUT:
                if self.anim_status == CARD_ANIM_STATUS_GOTO: x = self.target_pos[0]
                else:                     x = self.rect.left
                y = HANDCARD_TOP
                self.goto ((x,y))
                self.status = CARD_STATUS_INHAND
        elif msg == MOUSEBUTTONDOWN_RIGHT:
            if self.status == CARD_STATUS_ONMOUSE:
                self.toggle_face()
                #game.send_net_event ("set_card_face %s %s" % (self.objid, self.isfore))
            else:
                # REAL PURPOSE : tap/untap or face up/down
                self.toggle_tapping()
                game.send_net_event("set_card_tapping %s %s" % (self.objid, self.istapping))
                
                # FOR TEST : show card's zindex in a message
                #game.show_message("%s" % self.zindex)
                
                # for TEST : goto a random pos
                #pos = (random.randint(0,799-self.rect.height), random.randint(0,599-self.rect.width))
                #self.goto (pos)
        elif msg == MOUSEBUTTONDOWN_LEFT:
            if self.status == CARD_STATUS_ONDESK:
                self.set_onmouse(True)
                game.pickup(self)
                self.status = CARD_STATUS_ONMOUSE
                
                self.comefrom = CARD_FROM_DESK
                
            elif self.status in (CARD_STATUS_INHAND, CARD_STATUS_INHAND_OUT):
                #self.toggle_onmouse()
                #if self.onmouse:
                #    game.set_onmouse(self)
                #    game.handcards.remove(self)
                #    self.status = CARD_STATUS_ONMOUSE
                #else:
                #    game.puttop(self)
                #    self.status = CARD_STATUS_ONDESK
                self.set_onmouse(True)
                game.set_onmouse(self)
                game.handcards.remove(self)
                self.status = CARD_STATUS_ONMOUSE
                self.comefrom = CARD_FROM_HAND
                
            elif self.status == CARD_STATUS_INCOLLECTION:
                self.set_onmouse(True)
                game.set_onmouse(self)
                game.ccviewer.cards.remove(self)
                self.status = CARD_STATUS_ONMOUSE
                self.comefrom = CARD_FROM_LIB
                
            elif self.status == CARD_STATUS_ONMOUSE:
                x,y = pygame.mouse.get_pos()
                if y > 550:
                    self.set_onmouse(False)
                    game.set_offmouse(self)
                    game.handcards.add_at(self, self.rect.topleft)
                    self.status = CARD_STATUS_INHAND
                    
                    if self.comefrom == CARD_FROM_DESK:
                        game.send_net_event("move_card_tohand_fromdesk %s %s %s" % (self.objid, self.rect.left, self.rect.top))
                    elif self.comefrom == CARD_FROM_LIB:
                        game.send_net_event("move_card_tohand_fromlib %s %s %s %s" % (self.info.id, self.objid, self.rect.left, self.rect.top))
                    elif self.comefrom == CARD_FROM_HAND:
                        game.send_net_event("move_card_tohand_fromhand %s %s %s" % (self.objid, self.rect.left, self.rect.top))
                elif game.status == GAME_STATUS_CCVIEW and y > CARDCOLLECTION_VIEWER_TOP and y < CARDCOLLECTION_VIEWER_TOP+size_small[1]+40:
                    self.set_onmouse(False)
                    game.set_offmouse(self)
                    idx = (self.rect.left-game.ccviewer.left)/(20+size_small[0])+1
                    game.ccviewer.cards.insert(idx, self)
                    self.zindex = CARD_INCCVIEWER_ZINDEX
                    self.status = CARD_STATUS_INCOLLECTION
                    self.anim_status = CARD_ANIM_STATUS_NORMAL
                    game.ccviewer.adjust_pos()
                else:
                    self.set_onmouse(False)
                    game.puttop(self)
                    self.status = CARD_STATUS_ONDESK
                    self.anim_status = CARD_ANIM_STATUS_NORMAL
                    
                    if self.comefrom == CARD_FROM_HAND:
                        game.send_net_event("move_card_fromhand %s %s %s %s" % (self.objid, self.rect.left, self.rect.top, self.isfore))
                    elif self.comefrom == CARD_FROM_DESK:
                        game.send_net_event("move_card_ondesk %s %s %s %s" % (self.objid, self.rect.left, self.rect.top, self.isfore))
                    elif self.comefrom == CARD_FROM_LIB:
                        game.send_net_event("move_card_fromlib %s %s %s %s %s" % (self.info.id, self.objid, self.rect.left, self.rect.top, self.isfore))