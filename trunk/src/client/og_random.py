
import random

def shuffle(cards):
    if len(cards) > 0:
        for i in range(len(cards)):
            j = random.randint(0,len(cards)-1)
            cards[i], cards[j] = cards[j], cards[i]