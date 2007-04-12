import sys
import pygame
from pygame.locals import *

import random

class InputHandler:
    def __init__(self, game):
        self.game = game
    
    def process(self, evt):
        if evt.type == MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            btns = pygame.mouse.get_pressed()
            self.game.click (pos, btns)
            
        elif evt.type == MOUSEMOTION:
            pos = pygame.mouse.get_pos()
            self.game.hover (pos)
            
        # press ESC to exit
        elif evt.type == KEYUP:
            if evt.key == 27: self.game.exit()               # ESCAPE
            #elif evt.key == 32: self.game.set_status()
            elif evt.key == 105: self.game.say("Instant!")   # 'i'
            elif evt.key == 109: self.game.say("Mistake.")   # 'm'
            elif evt.key == 121: self.game.say("Yes.")       # 'y'
            elif evt.key == 110: self.game.say("No.")        # 'n'
            elif evt.key == 111: self.game.say("OK?")        # 'o'
            elif evt.key == 116: self.game.say("Your turn.") # 't'
            elif evt.key == 97:  self.game.say("Attack!")    # 'a'
            elif evt.key == 98:  self.game.say("Block.")     # 'b'
            elif evt.key == 119: self.game.say("Wait.")      # 'w'
            elif evt.key == 115: self.game.say("Surrender.") # 's'
            elif evt.key == 103: self.game.new_game()        # 'g'
            elif evt.key == 100: # 'd -- Draw card'
                self.game.draw_card()
            elif evt.key == 91: # '[' -- decrease hp
                self.game.adjust_player_hp(-1)
                #self.game.player.hp -= 1
                #self.game.say ("HP - : " + str(self.game.player.hp))
            elif evt.key == 93: # ']' -- increase hp
                self.game.adjust_player_hp(1)
                #self.game.player.hp += 1
                #self.game.say ("HP + : " + str(self.game.player.hp))
            elif evt.key == 61: # '=' -- show current hp
                self.game.say ("Current HP: " + str(self.game.player.hp))
            elif evt.key == 114: # 'r' -- roll dice 1-6
                self.game.say ("Roll dice: " + str(random.randint(1,6)))