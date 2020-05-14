# © 2019 KidsCanCode LLC / All rights reserved

# Sprite classes for platform game
import pygame as pg
# from pg.sprite import Sprite
from settings import *
vec = pg.math.Vector2

class Player(pg.sprite.Sprite):
    def __init__(self, game):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((30, 40))
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
        self.gravNum = 3
        self.jumpHeight = -PLAYER_JUMP_HEIGHT
        self.grav = self.gravNum
        self.game = game
    
    def gravity(self):
        self.acc.y += self.grav
    
    def jump(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_w] and self.acc.y == 0:
            self.acc.y = self.jumpHeight
            self.grav = self.gravNum
    
    def screenBorder(self):
        if self.rect.top < 0:
            self.rect.top = 0
            if self.acc.y < 0:
                self.acc.y = 0
        elif self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
            if self.acc.y > 0:
                self.acc.y = 0

    def update(self):
        self.acc = vec(0, 0)
        keys = pg.key.get_pressed()
        if keys[pg.K_a]:
            self.acc.x = -PLAYER_ACC
        if keys[pg.K_d]:
            self.acc.x = PLAYER_ACC
        self.gravity()
        # self.screenBorder()
        self.jump()
        

        # apply friction
        self.acc += self.vel * PLAYER_FRICTION
        # equations of motion
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        # wrap around the sides of the screen
        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH

        self.rect.center = self.pos

class Platform(pg.sprite.Sprite):
    def __init__(self, game, pos):
        pg.sprite.Sprite.__init__(self)
        if pos == (WIDTH/2, HEIGHT):
            self.image = pg.Surface((WIDTH, 30))
        else:
            self.image = pg.Surface((100, 20))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.pos = vec(WIDTH / 2, HEIGHT / 2)
        self.game = game
        self.pos.x = pos[0]
        self.pos.y = pos[1]
    def playerStop(self):
        if self.rect.top <= self.game.player.rect.bottom and self.rect.bottom >= self.game.player.rect.top:
            if self.rect.left <= self.game.player.rect.right and self.rect.right >= self.game.player.rect.left:
                if self.game.player.vel.y >= 0:
                    self.game.player.rect.bottom = self.rect.top
                    if self.game.player.acc.y > 0:
                        self.game.player.grav = 0
                        self.game.player.acc.y = 0
                        self.game.player.vel.y = 0
                
            else:
                self.game.player.grav = self.game.player.gravNum
    def update(self):
        self.playerStop()
        self.rect.center = self.pos

class Bullet(pg.sprite.Sprite):
    def __init__(self, dir, player, game):
        pg.sprite.Sprite.__init__(self)
        self.direction = dir
        self.player = player
        self.game = game
        self.image = pg.Surface((10, 10))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.pos = vec(WIDTH / 2, HEIGHT / 2)
    def update(self):
        self.pos.y += 4
