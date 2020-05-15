import pygame as pg
import random
from settings import *
vec = pg.math.Vector2

class Player(pg.sprite.Sprite):
    def __init__(self, game):
        #initialize the sprite and set the color, size, and possition
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((30,30))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.rect.bottom = self.rect[1] + self.rect[3]
        self.rect.right = self.rect[0] + self.rect[2]
        self.rect.top = self.rect[1]
        self.rect.left = self.rect[0]
        self.pos = vec(WIDTH / 2, HEIGHT / 2)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.game = game

        #set hitpoints
        self.hp = 100
    
    def update(self):
        #reset acceleration
        self.acc = vec(0, 0)
        #when pressing a direction you accelerate in that direction
        keys = pg.key.get_pressed()
        if keys[pg.K_a]:
            self.acc.x = -PLAYER_ACC
        if keys[pg.K_d]:
            self.acc.x = PLAYER_ACC
        if keys[pg.K_w]:
            self.acc.y = -PLAYER_ACC
        if keys[pg.K_s]:
            self.acc.y = PLAYER_ACC
        
        #apply friction and acceleration
        self.acc += self.vel * -PLAYER_FRIC
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        #change the objects possition on the display to the possition
        self.rect.center = self.pos

class Grunt(pg.sprite.Sprite):
    def __init__(self, game):
        #initialize the sprite and set the color, size, and possition
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((20,20))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.rect.bottom = self.rect[1] + self.rect[3]
        self.rect.right = self.rect[0] + self.rect[2]
        self.rect.top = self.rect[1]
        self.rect.left = self.rect[0]
        self.pos = vec(WIDTH / 2, HEIGHT / 2)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.game = game
        self.player = self.game.player
    
    def setAcc(self):
        # direction = random.randint(0,4)
        # if direction == 0:
        #     self.acc = vec(0,0)
        # elif direction == 1:
        #     self.acc.x = -GRUNT_ACC
        # elif direction == 2:
        #     self.acc.x = GRUNT_ACC
        # elif direction == 3:
        #     self.acc.y = -GRUNT_ACC
        # elif direction == 4:
        #     self.acc.y = GRUNT_ACC
        
        if self.player.pos.x > self.pos.x:
            self.acc.x = GRUNT_ACC
        elif self.player.pos.x < self.pos.x:
            self.acc.x = -GRUNT_ACC
        if self.player.pos.y > self.pos.y:
            self.acc.y = GRUNT_ACC
        elif self.player.pos.y < self.pos.y:
            self.acc.y = -GRUNT_ACC
    
    def update(self):
        #reset acceleration
        #set the direction randomly and accelerate in that direction
        self.setAcc()
        
        #apply friction and acceleration
        self.acc += self.vel * -GRUNT_FRIC
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        #change the objects possition on the display to the possition
        self.rect.center = self.pos