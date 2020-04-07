# © 2019 KidsCanCode LLC / All rights reserved

# KidsCanCode - Game Development with Pygame video series
# Jumpy! (a platform game) - Part 2
# Video link: https://www.youtube.com/watch?v=8LRI0RLKyt0
# Player movement

import pygame as pg
# from pg.sprite import Sprite
import random
from settings import *
from sprites import *

class Game:
    def __init__(self):
        # initialize game window, etc
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True

    def new(self):
        # start a new game
        self.all_sprites = pg.sprite.Group()
        self.player = Player(self)
        self.plat1 = Platform(self, (WIDTH/2, HEIGHT - HEIGHT/8))
        self.plat2 = Platform(self, (WIDTH/4, HEIGHT - HEIGHT/4))
        self.platform = Platform(self, (WIDTH/2, HEIGHT))
        platforms = []
        platforms.append(self.plat1)
        platforms.append(self.plat2)
        platforms.append(self.platform)
        for i in range(10):
            i = Platform(self, (random.randint(1, WIDTH), random.randint(1, HEIGHT)))
            go = True
            for a in platforms:
                if i.pos.x > a.pos.x - 200 and i.pos.x < a.pos.x + 200 or i.pos.y > HEIGHT - 100:
                    if i.pos.y > a.pos.y - 40 and i.pos.y < a.pos.y + 40:
                        go = False
            if go:
                self.all_sprites.add(i)
                platforms.append(i)
        self.all_sprites.add(self.player)
        self.all_sprites.add(self.platform)
        self.all_sprites.add(self.plat1)
        self.all_sprites.add(self.plat2)
        self.run()

    def run(self):
        # Game Loop
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def update(self):
        # Game Loop - Update
        self.all_sprites.update()

    def events(self):
        # Game Loop - events
        for event in pg.event.get():
            # check for closing window
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False

    def draw(self):
        # Game Loop - draw
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        # *after* drawing everything, flip the display
        pg.display.flip()

    def show_start_screen(self):
        # game splash/start screen
        pass

    def show_go_screen(self):
        # game over/continue
        pass

g = Game()
g.show_start_screen()
while g.running:
    g.new()
    g.show_go_screen()

pg.quit()