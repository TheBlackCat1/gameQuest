#This file was created by: Carter Hively

#impoting pygame as pg and random and all things from settings and sprites
import pygame as pg
import random
from settings import *
from sprites import *

#creating the game class
class Game:
    def __init__(self):
        #initializing pygame and the game's window and system
        pg.init()
        self.title = "Rise"
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(self.title)
        self.clock = pg.time.Clock()
        self.running = True
    
    def events(self):
        #get all events that happen and if it is quit then stop the game
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
    
    def new(self):
        self.allSprites = pg.sprite.Group()
        self.player = Player(self)
        self.allSprites.add(self.player)
        pass

    def level(self):
        #start another level and loop for the level
        while self.running and self.player.hp > 0:
            self.events()
            self.draw()
            self.update()
        #return if the player died or not
        return True

    def play(self):
        #display messages befpre game start
        #start a new game
        self.new()
        while True:
            dead = self.level()
            if dead:
                break
    
    def run(self):
        #run the game and is the master loop of the game (if stopped, the game is quit)
        while self.running:
            #run start screen loop at start and when play ends
            self.drawStartScreen()
            #run play and start playing loop
            self.play()

    def update(self):
        #update every sprite
        self.allSprites.update()
    
    def draw(self):
        #draw everything on the screen
        self.screen.fill(BLACK)
        self.allSprites.draw(self.screen)
        pg.display.flip()
    
    def drawStartScreen(self):
        pass

g = Game()
g.run()

pg.quit()