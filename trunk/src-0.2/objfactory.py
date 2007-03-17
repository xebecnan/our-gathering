from card import Card

class ObjFactory:
    def __init__(self, ptr_base):
        self.objs = {}
        self.ptr = self.ptr_base = ptr_base
        self.full = True
        
    def set_ptr_base(self, ptr_base):
        self.ptr = self.ptr_base = ptr_base
        #print 'new ptr_base %d' % self.ptr
    
    def create_card(self, card_info_id, info=None):
        card = Card(card_info_id, info)
        card.objid = self._gen_objid(card)
        if self.objs.has_key(card.objid): raise "Duplicated obj id!"
        self.objs[card.objid] = card
        
        return card
    
    def remove_obj(self, obj):
        if not self.objs.has_key(obj.objid): raise "Obj not managed by objfactory!"
        self.objs.pop(obj.objid)
        self.full = False
    
    def _gen_objid(self, card):
        if self.full:
            temp = self.ptr
            self.ptr += 1
            return temp
        else:
            for i in range(self.ptr_base, self.ptr):
                if not self.objs.has_key(i):
                    return i
            self.full = True
            temp = self.ptr
            self.ptr += 1
            return temp
    
    def obj(self, objid):
        if self.objs.has_key(objid):
            return self.objs[objid]
        else:
            return None
        
    def reg_card(self, card):
        card.objid = self._gen_objid(card)
        if self.objs.has_key(card.objid): raise "Duplicated obj id!"
        self.objs[card.objid] = card
        
    def reg_cards(self, cards):
        for card in cards:
            self.reg_card(card)
            
    def reg_card_with_objid(self, card):
        if self.objs.has_key(card.objid) : raise "Duplicated obj id: %s!" % card.objid
        self.objs[card.objid] = card

#class ObjFactory:
#    instance = ObjFactoryClass()
#    def __getattr__(self, name):
#        return getattr(ObjFactory.instance, name)
#    def __setattr__(self, name, value):
#        return setattr(ObjFactory.instance, name, value)