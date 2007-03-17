import pygame
import pygame.font

import sys, os

home = os.path.dirname(sys.argv[0])
imgdir = '..\\images'

def imgpath(filename):
    return '%s\\%s' % (imgdir, filename)

def load_image(filename):
    img = pygame.image.load(imgpath(filename))
    return img

def draw_text(surf, text, pos=(0,0), fg=(255,255,255), bg=None, size=15):
    #fontpath = os.path.join (home, "msyh.ttf")
    fontpath = os.path.join(os.environ['SystemRoot'], 'Fonts\\Tahoma.ttf')
    font = pygame.font.Font (fontpath, size)
    text = text.replace('\t', '        ')
    text = text.replace('\n', ' ')
    if bg is None:
        rendered = font.render (text, 0, fg)
    else:
        rendered = font.render (text, 0, fg, bg)
    surf.blit (rendered, pos)