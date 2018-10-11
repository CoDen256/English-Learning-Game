import pygame
import sys

pygame.init()

def add_message(surface, text, size, color, x, y, font_="font.otf", angle=0):

    font = pygame.font.Font(font_, size) if (font_.endswith('.otf') or font_.endswith('.ttf')) else pygame.font.SysFont(font_, size)

    textS, textR = font.render(text, True, color), font.render(text, True, color).get_rect()

    textS = pygame.transform.rotate(textS, angle)

    textR.center = x, y
    surface.blit(textS, textR)

def quit_game():
    sys.exit()

def load_data(filename, sep=' '):
    f = open(filename, "r").readlines()
    data = []

    for line in f:
        data.append(tuple([l.strip() for l in line.split(sep)]))
    return data

def dt_format(dt):
    return str(int(str(dt).replace('.',':').split(":")[2])+
           (60*int(str(dt).replace('.',':').split(":")[1])))


def init_score(filename, sep=' - '):
    return [("Default Player Name", '0'),("Default PLayer 2 Name", '10'), (None, None), ("Default Player 3 Name", '2'),(None, None),(None, None)]
    return load_data(filename, sep=sep)


