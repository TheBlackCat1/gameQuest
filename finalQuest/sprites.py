import pygame as pg
import random
from settings import *
vec = pg.math.Vector2

#player sprite class
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
        self.bullets = pg.sprite.Group()

        #set hitpoints
        self.hp = PLAYER_HP
    
    def shoot(self):
        mouse = pg.mouse.get_pos()
        pressed = pg.mouse.get_pressed()
        if pressed[0]:
            self.bullets.add(Bullet(self, mouse))
    
    def checkBoundaries(self):
        if self.rect.top < 0:
            self.rect.top = 0
            if self.acc.y < 0:
                self.acc.y = 0
            if self.vel.y < 0:
                self.vel.y = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
            if self.acc.y > 0:
                self.acc.y = 0
            if self.vel.y > 0:
                self.vel.y = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
            if self.acc.x > 0:
                self.acc.x = 0
            if self.vel.x > 0:
                self.vel.x = 0
        if self.rect.left < 0:
            self.rect.left = 0
            if self.acc.x < 0:
                self.acc.x = 0
            if self.vel.x < 0:
                self.vel.x = 0
    
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

        self.shoot()
        
        self.rect.center = self.pos
        self.checkBoundaries()

#bullet sprite
class Bullet(pg.sprite.Sprite):
    def __init__(self, player, mousePos):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((5,5))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.rect.bottom = self.rect[1] + self.rect[3]
        self.rect.right = self.rect[0] + self.rect[2]
        self.rect.top = self.rect[1]
        self.rect.left = self.rect[0]
        self.pos = vec(player.pos.x, player.pos.y)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.player = player
        self.game = self.player.game
        self.enemies = self.game.enemySprites
        self.mouse = mousePos
        self.ticks = 0
    
    def setAcc(self):
        self.acc = vec(0, 0)
        ratioX = self.mouse[0] - self.pos.x
        ratioY = self.mouse[1] - self.pos.y
        if ratioX > 0:
            self.acc.x = BULLET_SPEED
        if ratioX < 0:
            self.acc.x = -BULLET_SPEED
        if ratioY > 0:
            self.acc.y = BULLET_SPEED
        if ratioY < 0:
            self.acc.y = -BULLET_SPEED
    
    def checkBoundaries(self):
        if self.pos.x > WIDTH or self.pos.x < 0 or self.pos.y > HEIGHT or self.pos.y < 0:
            self.player.bullets.remove(self)
    
    def countTick(self):
        self.ticks += 1
        if self.ticks > 100:
            self.player.bullets.remove(self)
    
    def checkEnemy(self):
        for i in self.enemies:
            if self.rect.top < i.rect.bottom and self.rect.bottom > i.rect.top and self.rect.right > i.rect.left and self.rect.left < i.rect.right:
                i.hp -= BULLET_ATK
    
    def update(self):
        self.setAcc()
        self.checkBoundaries()
        self.countTick()

        self.checkEnemy()

        #apply friction and acceleration
        self.acc += self.vel * -GRUNT_FRIC
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        #check if in enemy
        #change the objects possition on the display to the possition
        self.rect.center = self.pos

#health pack sprite class
class HealthPack(pg.sprite.Sprite):
    def __init__(self, game):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((30,30))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        spawnX = random.randint(0, WIDTH)
        spawnY = random.randint(0, HEIGHT)
        self.rect.center = (spawnX, spawnY)
        self.rect.bottom = self.rect[1] + self.rect[3]
        self.rect.right = self.rect[0] + self.rect[2]
        self.rect.top = self.rect[1]
        self.rect.left = self.rect[0]
        self.pos = vec(spawnX, spawnY)
        self.game = game
        self.player = self.game.player
    
    def update(self):
        if self.player.rect.top < self.rect.bottom and self.player.rect.bottom > self.rect.top and self.player.rect.right > self.rect.left and self.player.rect.left < self.rect.right:
            self.player.hp += HEALING
            if self.player.hp > PLAYER_HP:
                self.player.hp = PLAYER_HP
            self.game.healthPacks.remove(self)

        self.rect.center = self.pos



#enemy sprite classes
#grunt class
class Grunt(pg.sprite.Sprite):
    def __init__(self, game):
        #initialize the sprite and set the color, size, and possition
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((20,20))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        spawnX = random.randint(0, WIDTH)
        spawnY = random.randint(0, HEIGHT)
        self.rect.center = (spawnX, spawnY)
        self.rect.bottom = self.rect[1] + self.rect[3]
        self.rect.right = self.rect[0] + self.rect[2]
        self.rect.top = self.rect[1]
        self.rect.left = self.rect[0]
        self.pos = vec(spawnX, spawnY)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.game = game
        self.player = self.game.player
        self.canMove = False
        self.ticks = 0
        self.hp = GRUNT_HP
    
    def setAcc(self):
        #go in the direction of the player
        self.acc = vec(0,0)
        if self.player.pos.x > self.pos.x:
            self.acc.x = GRUNT_ACC
        elif self.player.pos.x < self.pos.x:
            self.acc.x = -GRUNT_ACC
        if self.player.pos.y > self.pos.y:
            self.acc.y = GRUNT_ACC
        elif self.player.pos.y < self.pos.y:
            self.acc.y = -GRUNT_ACC
        #if close to the player on a certain axis then stop 
        #(there is no need to go further that direction)
        #(used to stop the bouncing sceen when it is heading in one axis direction)
        if self.pos.x > self.player.rect.left and self.pos.x < self.player.rect.right:
            self.acc.x = 0
        if self.pos.y > self.player.rect.top and self.pos.y < self.player.rect.bottom:
            self.acc.y = 0

    def tickMove(self):
        self.ticks += 1
        if self.ticks > 50:
            self.canMove = True
    
    def update(self):
        #reset acceleration
        #set the direction randomly and accelerate in that direction
        if self.canMove:
            self.setAcc()
        else:
            self.tickMove()
        
        if self.hp <= 0:
            print("BLEH")
            self.game.enemySprites.remove(self)
        
        #apply friction and acceleration
        self.acc += self.vel * -GRUNT_FRIC
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        if self.rect.bottom > self.player.rect.top and self.rect.top < self.player.rect.bottom and self.rect.left < self.player.rect.right and self.rect.right > self.player.rect.left:
            self.player.hp -= GRUNT_ATK
        #change the objects possition on the display to the possition
        self.rect.center = self.pos