
from locals import *

class MessagePool:
    def __init__(self):
        self.messages = []
    
    def add(self, msg):
        self.messages.insert(0,msg)
        self.adjust_pos()
        
    def remove(self, msg):
        if msg in self.messages:
            self.messages.remove(msg)
    
    def adjust_pos(self):
        for i, msg in zip(range(len(self.messages)), self.messages):
            top = self.calc_top(i)
            if msg.rect.top != top:
                msg.goto((msg.rect.left, top))
            
    def calc_top(self, index):
        return MESSAGEPOOL_TOP + (MESSAGE_SPACING + MESSAGE_HEIGHT) * index