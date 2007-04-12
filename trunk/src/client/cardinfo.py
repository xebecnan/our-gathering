
class CardType:
	Artifact = 0
	Creature = 1
	Enchantment = 2
	Instant = 3
	Land = 4
	Sorcery = 5

class CardInfo:
    def __init__(self):
            self.id = None
            self.name = None
            self.mana_cost = None
            self.type = None
            self.desc = None
            self.power = None
            self.toughness = None
            self.ablity = None
            self.color = None
            self.image = "card001.jpg"

def clone_cardinfo(info):
	ret = CardInfo()
	ret.id = info.id
	ret.name = info.name
	ret.image = info.image
	return ret