import pygame as pg
from pygame.sprite import Sprite
from math import *
from pygame.math import Vector2 as vec
import os
from settings import *

# setup asset folders here - images sounds etc.
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, 'images')
snd_folder = os.path.join(game_folder, 'sounds')

class Player(Sprite):
    def __init__(self, game):
        Sprite.__init__(self)
        # self.image = pg.Surface((50, 50))
        # self.image.fill(GREEN)
        # use an image for player sprite...
        self.game = game
        self.image = pg.image.load(os.path.join(img_folder, 'theBigBell.png')).convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (0, 0)
        self.pos = vec(WIDTH/2, HEIGHT/2)
        self.vel = vec(0,0)
        self.acc = vec(0,0) 
    def controls(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_a]:
            self.acc.x = -5
        if keys[pg.K_d]:
            self.acc.x = 5
        if keys[pg.K_SPACE]:
            self.jump()
        if keys[pg.K_LSHIFT]:
            self.fire()
    def fire(self):
        mpos = pg.mouse.get_pos()
        targety = mpos[0]
        targetx = mpos[1]
        distance_x = targetx - self.rect.x
        distance_y =targety -self.rect.y
        angle = atan2(distance_y,distance_x)
        speed_x = 10*cos(angle)
        speed_y = 10*sin(angle)
        p= Gun(self.pos.x, self.pos.y-self.rect.height, 10, 10, speed_x, speed_y, "" )
        self.game.all_sprites.add(p)
    def jump(self):
        hits = pg.sprite.spritecollide(self, self.game.all_platforms, False)
        if hits:
            print("i can jump")
            self.vel.y = -PLAYER_JUMP
    def update(self):
        hitpoint = 100
        # CHECKING FOR COLLISION WITH MOBS
        mhits = pg.sprite.spritecollide(self, self.game.all_mobs, True)
        if mhits:
            hitpoint -= 10
        if hitpoint == 0:
            hitpoint = 100
            self.score -= 1
            self.pos = vec(WIDTH/2, HEIGHT/2)
                

        self.acc = vec(0,PLAYER_GRAV)
        self.controls()
        # if friction - apply here
        self.acc.x += self.vel.x * -PLAYER_FRIC
        # self.acc.y += self.vel.y * -0.3
        # equations of motion
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        self.rect.midbottom = self.pos

# platforms
class Gun(Sprite):
    def __init__(self, x, y, w, h, speed_x, speed_y, type):
        Sprite.__init__(self)
        self.image = pg.surface(w, h)
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.fired = False
    def update(self):
        self.rect.x +=self.speed_x
        self.rect.y +=self.speed_y
        if (self.rect.y < 0 or self.rect.y > HEIGHT or self.rect.x <0 or self.rect.x > WIDTH)
            self.kill()
class Platform(Sprite):
    def __init__(self, x, y, w, h, category):
        Sprite.__init__(self)
        self.image = pg.Surface((w, h))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        # if Player.vel.x > 0:
        #     self.rect.x -= Player.vel.x
        self.rect.y = y
        self.category = category
        self.speed = 0
        if self.category == "moving":
            self.speed = 5
    def update(self):
        if self.category == "moving":
            self.rect.x += self.speed
            if self.rect.x + self.rect.w > WIDTH or self.rect.x < 0:
                self.speed = -self.speed

class Mob(Sprite):
    def __init__(self, x, y, w, h, kind):
        Sprite.__init__(self)
        self.image = pg.Surface((w, h))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.kind = kind
        self.pos = vec(WIDTH/2, HEIGHT/2)

    def update(self):
        pass
        