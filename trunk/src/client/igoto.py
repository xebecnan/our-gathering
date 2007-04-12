
from locals import *
from deskobject import *

class IGoto(DeskObject):
    def __init__(self):
        DeskObject.__init__(self)
        
        self.anim_status = ANIM_STATUS_NORMAL
        self.target_pos = None
        
    def update(self):
        if self.anim_status == ANIM_STATUS_GOTO:
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
                self.anim_status = ANIM_STATUS_NORMAL
            else:
                self.rect.move_ip(vx,vy)
                self.dirty = True
                
    def goto(self, pos):
        self.anim_status = ANIM_STATUS_GOTO
        self.target_pos = pos