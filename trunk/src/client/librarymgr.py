
import os

from locals import *

from og_random import shuffle
from card import Card
#from objfactory import ObjFactory

#LIBFILE = 'library.dat'
#LIBFILE = 'lib_2.dat'
#LIBFILE = 'darkrush.txt'
#LIBFILE = 'artifactcreature.txt'
#LIBFILE = 'WhiteGreenCycling.txt'

class LibraryMgr:
    def load(self, libfile, shuffled=True):
        ret = []
        
        for line in open(os.path.join(DECKS_DIR, libfile), 'r'):
            try:
                if 'x' in line:
                    token = line.split('x')
                    times = int(token[0])
                    info_id = int(token[1])
                    for i in range(times):
                        card = Card(info_id)
                        ret.append(card)
                else:
                    card_info_id = int(line)
                    card = Card(card_info_id)
                    ret.append(card)
            except:
                continue
            
        if shuffled:
            shuffle(ret)
            
        return ret