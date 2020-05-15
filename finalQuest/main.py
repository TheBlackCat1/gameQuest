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

    def newLevel(self):
        self.enemySprites = pg.sprite.Group()
        self.enemy = Grunt(self)
        self.enemySprites.add(self.enemy)

    def level(self):
        #start another level and loop for the level
        self.newLevel()
        while self.running and self.player.hp > 0:
            self.events()
            self.draw()
            self.update()
            self.clock.tick(FPS)
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
            self.startScreen()
            #run play and start playing loop
            self.play()

    def update(self):
        #update every sprite
        self.allSprites.update()
        self.enemySprites.update()
    
    def draw(self):
        #draw everything on the screen
        self.screen.fill(BLACK)
        self.allSprites.draw(self.screen)
        self.enemySprites.draw(self.screen)
        pg.display.flip()
    
    def drawText(self, size, text, color, posx, posy):
        buttonText = pg.font.Font("freesansbold.ttf", size)
        textSurface = buttonText.render(text, True, color)
        textSurf, textRect = textSurface, textSurface.get_rect()
        textRect.center = (posx, posy)
        self.screen.blit(textSurf, textRect)

    def drawStartScreen(self):
        self.screen.fill(BLACK)
        #self.startScreenSprites = pg.sprite.Group()
        pg.draw.rect(self.screen, GREEN, (WIDTH/4-30, HEIGHT-HEIGHT/4, 60, 30))
        pg.draw.rect(self.screen, RED, (WIDTH-WIDTH/4-30, HEIGHT-HEIGHT/4, 60, 30))
        #pg.draw.rect(self.screen, ORANGE, (WIDTH/2-30, HEIGHT-HEIGHT/4, 60, 30))
        self.drawText(20, "PLAY", BLACK, WIDTH/4, HEIGHT-HEIGHT/4+15)
        self.drawText(20, "QUIT", BLACK, WIDTH-WIDTH/4, HEIGHT-HEIGHT/4+15)

        mouse = pg.mouse.get_pos()
        pressed = pg.mouse.get_pressed()
        if mouse[0] > WIDTH/4-30 and mouse[0] < WIDTH/4+30 and mouse[1] > HEIGHT-HEIGHT/4 and mouse[1] < HEIGHT-HEIGHT/4+30 and pressed[0] == 1:
            return True
        if mouse[0] > WIDTH-WIDTH/4-30 and mouse[0] < WIDTH-WIDTH/4+30 and mouse[1] > HEIGHT-HEIGHT/4 and mouse[1] < HEIGHT-HEIGHT/4+30 and pressed[0] == 1:
            self.running = False
        self.drawText(100, self.title, RED, WIDTH/2, HEIGHT/2 - self.titleHeight)

        pg.display.flip()
        return False

    
    def startScreen(self):
        #start screen loop
        self.titleHeight = 0
        while self.running:
            self.events()
            play = self.drawStartScreen()
            if self.title == "Rise":
                self.titleHeight += 2
                if self.titleHeight > 250:
                    self.title = "Fall"
            else:
                self.titleHeight -= 2
                if self.titleHeight < 0:
                    self.title = "Rise"
            
            if play:
                break
            
            self.clock.tick(FPS)

g = Game()
g.run()

pg.quit()