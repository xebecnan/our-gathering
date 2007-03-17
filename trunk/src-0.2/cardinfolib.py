import pickle
from locals import *
from cardinfo import *

class CardInfoLib:
	def __init__(self):
		self.lib = None
		self.load()
	def load(self):
		self.lib = pickle.load (open(CardInfoLibFile))
	def save(self):
		pickle.dump (self.lib, open(CardInfoLibFile, 'w'))
	def add(self, card):
		if self.lib.has_key (card.id): raise "duplicated card!"
		self.lib[card.id] = card
	def remove(self, card_id):
		if not self.lib.has_key (card_id): raise "card not exist!"
		self.lib.pop(card_id)
	def exist(self, card):
		return self.lib.has_key (card.id)
	def new_id(self):
		if len(self.lib) == 0: return 0
		else: return max(self.lib.keys()) + 1
	def cardinfo(self,card_id):
		try:
			return self.lib[card_id]
			#ret = clone_cardinfo(self.lib[card_id])
			#return ret
		except:
			print self.lib
			print card_id
			raise


	
# singleton
class CILS:
	inst = CardInfoLib()
	def __getattr__(self, name):
		return getattr(CILS.inst, name)
	def __setattr__(self, name, value):
		return setattr(CILS.inst, name, value)