# This file was created by: Daniel Zhu
# This code was inspired by Zelda and informed by Chris Bradfield


import pygame as pg
from Settings import *

HITPOINTS = 100
def set_hitpoints():
    global HITPOINTS
    hitpoints = 100

print(HITPOINTS)
#defines a class "player" in the group sprites
class Player(pg.sprite.Sprite):
# initiate the size, the color, and where it is.
    def __init__(self, game, x, y):
        self.groups=game.all_sprites
        # Initilizes superclass
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
    # Game loop, IPO, if key pressed, velocity
    def get_keys(self):
        self.vx, self.vy = 0, 0
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.vx = -PLAYER_SPEED  
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.vx = PLAYER_SPEED  
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.vy = -PLAYER_SPEED  
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            self.vy = PLAYER_SPEED
        if self.vx != 0 and self.vy != 0:
            self.vx *= 0.7071
            self.vy *= 0.7071

            
# moves where the sprite is
    # def move(self, dx=0, dy=0):
    #     if not self.collide_with_walls(dx,dy):
    #         self.x += dx
    #         self.y += dy

    # def collide_with_walls(self, dx=0, dy=0):
    #     for wall in self.game.walls:
    #         if wall.x == self.x + dx and wall.y == self.y + dy:
    #             return True
    #         return False
# Collision detection
    def collide_with_walls(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vx > 0:
                    self.x = hits[0].rect.left - self.rect.width
                if self.vx < 0:
                    self.x = hits[0].rect.right
                self.vx = 0
                self.rect.x = self.x
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vy > 0:
                    self.y = hits[0].rect.top - self.rect.height
                if self.vy < 0:
                    self.y = hits[0].rect.bottom
                self.vy = 0
                self.rect.y = self.y
# Update the player,speed and collisons
    def update(self):
         self.get_keys()
         self.x += self.vx * self.game.dt
         self.y += self.vy * self.game.dt
         self.rect.x = self.x
         self.collide_with_walls('x')
         self.rect.y = self.y
         self.collide_with_walls('y')
# defines a class "wall" in the group Sprites
class Wall(pg.sprite.Sprite):
# Initiates the size, color, and where it is
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

