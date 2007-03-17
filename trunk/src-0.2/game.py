import sys
import thread

import pygame
from pygame.locals import *
from locals import *

from player import Player
from card import Card
from cardviewer import CardViewer
from deck import Deck
from opponentdeck import OpponentDeck
from graveyard import GraveYard
from opponentgraveyard import OpponentGraveYard
from cardcollectionviewer import CardCollectionViewer
from message import Message
from messagepool import MessagePool
from deckselector import DeckSelector
from hppanel import HPPanel
from waitplayerdiagram import WaitPlayerDiagram

from cardgroup import CardGroup
from handcardgroup import HandCardGroup
from opponenthandcardgroup import OpponentHandCardGroup
from renderclearbg import RenderClearBg

from objfactory import ObjFactory

class Game:
    def __init__(self, net_conn):
        self.status = GAME_STATUS_NORMAL
        self.net_conn = net_conn
        
        if self.net_conn.is_server:
            self.obj_factory = ObjFactory(0)
        else:
            self.obj_factory = ObjFactory(10000)
        
        self.player = Player()
        self.opponent = Player()
        
        #self.cards_inhand = CardGroup()
        objs = self.objs = CardGroup()
        deskcards = self.deskcards = CardGroup()
        handcards = self.handcards = HandCardGroup()
        o_handcards = self.o_handcards = OpponentHandCardGroup()
        
        # test cards
        #for cid in range(6):
        #    card = Card(cid)
        #    self.puttop(card)
        #    objs.add(card)
        #    deskcards.add(card)
        
        self.deck_selector = DeckSelector(self.objs)
        
        deck = self.deck = Deck(self, self.objs)
        #self.puttop(deck)
        #objs.add(deck)
        
        o_deck = self.o_deck = OpponentDeck(self, self.objs)
        #self.puttop(o_deck)
        #objs.add(o_deck)
        
        graveyard = self.graveyard = GraveYard(self, self.objs)
        #self.puttop(graveyard)
        #objs.add(graveyard)
        
        o_graveyard = self.o_graveyard = OpponentGraveYard(self, self.objs)
        #self.puttop(o_graveyard)
        #objs.add(o_graveyard)
        
        self.objonmouse = None
        self.objonhover = None
        
        # init card_viewer
        self.cardviewer = CardViewer(objs)
        #self.cardviewer_group = RenderClearBg(self.cardviewer)
        #objs.add(self.cardviewer)
        
        # init card_collection_viewer
        self.hp_panel = HPPanel(self.objs, self.player, self.opponent)
        self.ccviewer = CardCollectionViewer(self.objs)
        #self.ccviewer_group = RenderClearBg(self.ccviewer)
        #objs.add(self.ccviewer)
        
        self.msg_pool = MessagePool()
        self.wait_player_diagram = WaitPlayerDiagram(self.objs)
        
        self.lock = thread.allocate_lock()
        
        self.wait_player_diagram.show()
        #self.reset()
        self.dirty = True
    
    def reset(self):
        self.status = GAME_STATUS_SELECT_DECK
        self.deck_selector.load()
        self.deck_selector.show()
    
    def prepare_draw(self):
        return self.objs.prepare_draw()
    
    def draw(self, scr):
        dirty_field = self.objs.draw(scr)
        return dirty_field
        
    def update(self):
        self.objs.update()
        
    def topobj_at(self, pos):
        x,y = pos
        objs = [obj for obj in self.objs.sprites() if obj.rect.collidepoint(x,y)]
        if len(objs) > 0:
            objs.sort(cmp=lambda x,y:cmp(x.zindex,y.zindex),reverse=True)
            return objs[0]
        else:
            return None
        
    def click(self, pos, btns):
        #self.lock.acquire()
        x,y = pos
        msg = None
        if btns[0]: msg = MOUSEBUTTONDOWN_LEFT
        elif btns[2]: msg = MOUSEBUTTONDOWN_RIGHT
        
        if self.objonmouse is None:
            obj = self.topobj_at(pos)
            if obj is not None:
                obj.sendmsg(msg, self)
        else:
            obj = self.objonmouse
            obj.sendmsg(msg, self)
        
        #if btns[0]:
        #    if self.objonmouse is None:
        #        obj = self.topobj_at(pos)
        #        if obj is not None:
        #            obj.toggle_onmouse()
        #            self.objonmouse = obj
        #            self.pickup(obj)
        #    else:
        #        self.objonmouse.toggle_onmouse()
        #        self.puttop(self.objonmouse)
        #        self.objonmouse = None
        #elif btns[1]:
        #    if self.objonmouse is None:
        #        obj = self.topobj_at (pos)
        #    else:
        #        obj = self.objonmouse
        #    if obj is not None: obj.toggle_tapping()
        #else:
        #    if self.objonmouse is None:
        #        obj = self.topobj_at (pos)
        #    else:
        #        obj = self.objonmouse
        #    if obj is not None: obj.toggle_face()
        self.render_engine.update()
        #self.lock.release()
        
    def card_falldown(self, card, raw_card):
        cards = pygame.sprite.spritecollide (card, self.deskcards, False)
        if card in cards: cards.remove(card)
        if raw_card in cards: cards.remove(raw_card)
        
        # this card fall down
        lower_cards = [c for c in cards if c.zindex < card.zindex]
        if len(lower_cards) == 0:
            card.zindex = 0
        else:
            lower_cards.sort(cmp=lambda x,y:cmp(x.zindex, y.zindex), reverse=True)
            card.zindex = lower_cards[0].zindex+1
        card.dirty = True
        
    def drawout(self, card, raw_card):
        cards = pygame.sprite.spritecollide (card, self.deskcards, False)
        if card in cards: cards.remove(card)
        if raw_card in cards: cards.remove(raw_card)
        
        upper_cards = [c for c in cards if c.zindex > card.zindex]
        if len(upper_cards) == 0: return
        upper_cards.sort(cmp=lambda x,y:cmp(x.zindex, y.zindex))
        upper_zindex = upper_cards[0].zindex
        upper_cards = [c for c in upper_cards if c.zindex == upper_zindex]
        for c in upper_cards:
            self.card_falldown (c, raw_card)
            self.drawout (c, raw_card)
        #raw_card.zindex = CARD_DRAWOUT_ZINDEX
    
    def settop(self, card):
        cards = pygame.sprite.spritecollide (card, self.deskcards, False)
        if card in cards: cards.remove(card)
        if len(cards) == 0:
            card.zindex = 0
        else:
            cards.sort(cmp=lambda x,y:cmp(x.zindex,y.zindex), reverse=True)
            topcard = cards[0]
            card.zindex = topcard.zindex + 1
    
    def puttop(self, card):
        self.objonmouse = None
        self.settop (card)
        self.deskcards.add(card)
            
    def pickup(self, card):
        #self.cards_inhand.remove(card)
        self.drawout (card, card)
        self.set_onmouse(card)
        card.dirty = True
        self.deskcards.remove(card)
            
    def hover(self, pos):
        if self.objonmouse is not None: return
        
        x,y = pos
        objs = [obj for obj in self.objs.sprites() if obj.rect.collidepoint(x,y)]
        if len(objs) > 0:
            objs.sort(cmp=lambda x,y:cmp(x.zindex,y.zindex),reverse=True)
            obj = objs[0]
            
            if self.objonhover is not None and self.objonhover != obj:
                self.objonhover.sendmsg(MOUSE_UNHOVER, self)
            self.objonhover = obj
            
            obj.sendmsg(MOUSE_HOVER, self)
        elif self.objonhover != None:
            self.objonhover.sendmsg(MOUSE_UNHOVER, self)
            self.objonhover = None
    
    def add_deskcard(self, card, onmouse=False):
        if onmouse:
            card.rect.center = pygame.mouse.get_pos()
            card.set_onmouse(True)
            self.set_onmouse(card)
        
        card.game = self
        if not onmouse: self.puttop (card)
        self.objs.add (card)
        self.deskcards.add (card)
        
    def add_handcard (self, card, pos=None):
        if pos != None: card.rect.topleft = pos
        card.status = CARD_STATUS_INHAND
        
        self.handcards.add (card)
        self.objs.add (card)
        
        event = "add_handcard %s %s" % (card.info.id, card.objid)
        self.send_net_event(event)
        #print event
        
    def add_opponent_handcard (self, card, pos=None):
        if pos != None: card.rect.topleft = pos
        
        if card.status == CARD_STATUS_OPPONENT_INLIB:
            self.o_deck.remove (card)
        self.o_handcards.add (card)
        self.objs.add (card)
        
    def add_opponent_libcard (self, card):
        self.o_deck.add (card)
        
    def draw_card(self):
        card = self.deck.pop_card()
        self.add_handcard(card)
        
    def chg_card_hand_to_desk(self, card, is_fore, pos):
        self.o_handcards.remove(card)
        self.deskcards.add (card)
        
        card.status = CARD_STATUS_ONDESK
        card.set_face (is_fore)
        card.goto (pos)
        
    def chg_card_desk_to_hand(self, card, pos):
        self.deskcards.remove (card)
        self.o_handcards.add_at (card, pos)
        
    def chg_card_lib_to_hand(self, card, pos):
        self.objs.add(card)
        self.o_handcards.add_at (card, pos)
        
    def chg_card_lib_to_desk(self, card, is_fore, pos):
        self.o_deck.remove(card)
        self.objs.add(card)
        self.deskcards.add(card)
        
        card.status = CARD_STATUS_ONDESK
        card.set_face (is_fore)
        card.set_inverse(True)
        card.goto (pos)
        
    def chg_card_hand_to_hand(self, card, pos):
        self.o_handcards.remove(card)
        self.o_handcards.add_at (card, pos)
        
    def set_onmouse(self, obj):
        self.objonmouse = obj
        obj.zindex = sys.maxint
        
    def set_offmouse(self, obj):
        self.objonmouse = None
        
    #def set_status(self):
    #    self.deck.gen_rand()
        #self.deck.set_status(DECK_STATUS_INUSE)
        
    def view_detail(self, card):
        self.cardviewer.setcard(card.info.id)
        
    def close_view_detail(self):
        self.cardviewer.hide()
        
    def view_collection(self, cards_provider):
        self.status = GAME_STATUS_CCVIEW
        self.ccviewer.load_cards(cards_provider)
        self.ccviewer.show()
        
    def send_net_event(self, event):
        self.net_conn.send_event(event + ";")
        
    def show_message(self, msg):
        m = Message(msg, self.objs, self.msg_pool)
        self.objs.add(m)
        self.msg_pool.add(m)
        
    def say(self, msg):
        self.show_message("I say: " + msg)
        self.send_net_event ("say " + msg)
        
    def select_deck(self):
        self.deck_selector.load()
        self.deck_selector.show()
        
    def load_deck(self, libfile):
        self.deck_selector.hide()
        self.deck.load(libfile)
        self.status = GAME_STATUS_NORMAL
        self.say("I choose " + libfile)
        
    def adjust_player_hp(self, hp_change):
        self.hp_panel.adjust_player_hp(hp_change)
        self.say ("HP adjusted: " + str(self.player.hp))
        self.send_net_event("adjust_hp %s" % hp_change)
        
    def adjust_opponent_hp(self, hp_change):
        self.hp_panel.adjust_opponent_hp(hp_change)
        
    def new_game(self):
        # groups
        self.deskcards.empty()
        self.handcards.empty()
        self.o_handcards.empty()
        self.objs.empty()
        
        # components -- after objs
        self.deck.reset()
        self.o_deck.reset()
        self.graveyard.reset()
        self.o_graveyard.reset()
        
        # players
        self.player.reset()
        self.opponent.reset()
        
        # hp panel -- after players
        self.hp_panel.reset()
        
        self.reset()
        self.dirty = True
        
        self.send_net_event ("reset_finish")
        
    def on_opponent_found(self):
        self.wait_player_diagram.hide()
        self.reset()
        
    def exit(self):
        self.net_conn.close()
        sys.exit()