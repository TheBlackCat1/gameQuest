import pygame as pg
import random


class Player(pg.sprite.Sprite):
    def __init(self):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((30,30))