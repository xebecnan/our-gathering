import sys
import time

import pygame
from pygame.locals import *

from inputhandler import InputHandler
from renderengine import RenderEngine
from gamelogic import GameLogic
from game import Game
from netconn import NetConn
from neteventhandler import NetEventHandler

class App:
    def __init__(self):
        pygame.init()
        self.net_conn = NetConn (False)
        self.game = Game(self.net_conn)
        self.input_handler = InputHandler(self.game)
        self.render_engine = RenderEngine(self.game)
        self.game_logic = GameLogic(self.game)
        self.net_event_handler = NetEventHandler(self.game)
        
    def mainloop(self):
        while True:
            # handle inputs
            events = []
            if pygame.event.peek() is not None:
                for evt in pygame.event.get():
                    events.append (evt)
            else:
                events.append(pygame.event.wait())
            
            for evt in events:
                if evt.type == QUIT:
                    sys.exit()
                else:
                    self.input_handler.process(evt)
            
            # handle net events
            net_events = self.net_conn.get_events()
            for evt in net_events:
                self.net_event_handler.handle(evt)
            
            # update data & draw
            self.game_logic.update()
            self.render_engine.update()
            
            # flip
            pygame.display.flip()
            
            # wait
            time.sleep(0.01)

def main():
    app = App()
    app.mainloop()

if __name__ == "__main__":
    main()