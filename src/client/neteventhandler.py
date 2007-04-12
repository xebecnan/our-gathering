
import os

from card import Card
from locals import *

class NetEventHandler:
    def __init__(self, game):
        self.game = game
        
    def reverse_pos(self, x, y):
        h = size_small[1]
        y = 600 - y - h
        return x,y
        
    def handle(self, event):
        if DEBUG_MODE:
            os.system("echo \"%s\" >> log.txt" % event)
            
        #print event
        if event.startswith("add_handcard "):
            token = event.split()
            card_info_id = int(token[1])
            objid = int(token[2])
            
            card = self.game.obj_factory.obj(objid)
            self.game.add_opponent_handcard(card)
            
        elif event.startswith("add_lib_card "):
            token = event.split()
            card_info_id = int(token[1])
            objid        = int(token[2])
            
            card = Card(card_info_id)
            card.objid = objid
            card.game  = self.game
            
            self.game.obj_factory.reg_card_with_objid(card)
            self.game.add_opponent_libcard(card)
            
        elif event.startswith("move_card_fromhand "):
            token = event.split()
            objid = int(token[1])
            x = int(token[2])
            y = int(token[3])
            if token[4] == 'True' : isfore = True
            else:                   isfore = False
            card = self.game.obj_factory.obj(objid)
            self.game.chg_card_hand_to_desk (card, isfore, self.reverse_pos(x,y))
            
        elif event.startswith("move_card_ondesk "):
            token = event.split()
            objid = int(token[1])
            x = int(token[2])
            y = int(token[3])
            if token[4] == 'True' : isfore = True
            else:                   isfore = False
            card = self.game.obj_factory.obj(objid)
            card.set_face(isfore)
            card.goto (self.reverse_pos(x,y))
            
        elif event.startswith("move_card_fromlib "):
            token = event.split()
            info_id = int(token[1])
            objid = int(token[2])
            x = int(token[3])
            y = int(token[4])
            if token[5] == 'True': isfore = True
            else:                  isfore = False
            
            card = self.game.obj_factory.obj(objid)
            self.game.chg_card_lib_to_desk (card, isfore, self.reverse_pos(x,y))
            
        elif event.startswith("move_card_tohand_fromdesk "):
            token = event.split()
            objid = int(token[1])
            x = int(token[2])
            y = int(token[3])
            
            card = self.game.obj_factory.obj(objid)
            self.game.chg_card_desk_to_hand(card,(x,y))
            
        elif event.startswith("move_card_tohand_fromlib "):
            token = event.split()
            info_id = int(token[1])
            objid   = int(token[2])
            x = int(token[3])
            y = int(token[4])
            card = Card(info_id)
            card.objid = objid
            card.game = self.game
            card.rect.topleft = pos_opponent_library
            self.game.obj_factory.reg_card_with_objid(card)
            self.game.chg_card_lib_to_hand(card,(x,y))
            
        elif event.startswith("move_card_tohand_fromhand "):
            token = event.split()
            objid = int(token[1])
            x = int(token[2])
            y = int(token[3])
            card = self.game.obj_factory.obj(objid)
            self.game.chg_card_hand_to_hand(card, (x,y))
            
        elif event.startswith("set_card_tapping "):
            token = event.split()
            objid = int(token[1])
            if token[2] == 'True': istapping = True
            else:                  istapping = False
            card = self.game.obj_factory.obj(objid)
            card.set_tapping(istapping)
            
        #elif event.startswith("set_card_face "):
        #    token = event.split()
        #    objid = int(token[1])
        #    if token[2] == 'True': is_fore = True
        #    else:                  is_fore = False
        #    card = self.game.obj_factory.obj(objid)
        #    card.set_face
            
        elif event.startswith("say "):
            message = event[4:]
            self.game.show_message(message)
            
        elif event.startswith("adjust_hp "):
            token = event.split()
            hp_change = int(token[1])
            self.game.adjust_opponent_hp(hp_change)
            
        elif event == "reset_finish":
            self.game.show_message("Opponent resetted.")
            
        #elif event.startswith("move_card "):
        #    token = event.split()
        #    objid = int(token[1])
        #    x = int(token[2])
        #    y = int(token[3])
        #    card = self.game.obj_factory.obj(objid)
        #    if card is not None:
        #        card.goto((x,y))
                
        #elif event == "shuffle":
        #    self.game.show_message("shuffle")
        
        # FOR TEST
        #if event == "newcard":
        #    card = Card(0)
        #    pos = pos_opponent_library
        #    self.game.add_opponent_handcard(card,pos)
        elif event.startswith("set_obj_ptr "):
            token = event.split()
            ptr_base = int(token[1])
            self.game.obj_factory.set_ptr_base(ptr_base)
            
        elif event == "opponent_found":
            #print 'opponent_found'
            self.game.on_opponent_found()
            
        elif event == "opponent_leave":
            self.game.show_message("opponent leaves")