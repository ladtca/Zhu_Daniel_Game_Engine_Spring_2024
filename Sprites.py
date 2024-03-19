# This file was created by: Daniel Zhu
# This code was inspired by Zelda and informed by Chris Bradfield


import pygame as pg
from Settings import *


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
        self.moneybag = 0
        self.speed = 600
        self.HITPOINTS = 100
        self.weapon_drawn = False

    # Game loop, IPO, if key pressed, velocity
    def get_keys(self):
        self.vx, self.vy = 0, 0
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.vx = -self.speed  
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.vx = self.speed  
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.vy = -self.speed  
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            self.vy = self.speed
        if keys[pg.K_e]:
            print("trying to shoot...")
            self.pew()
        if self.vx != 0 and self.vy != 0:
            self.vx *= 0.7071
            self.vy *= 0.7071
        if keys[pg.K_f]:
            if not self.weapon_drawn:
                Sword(self.game, self.rect.x+TILESIZE, self.rect.y-TILESIZE)
                self.weapon_drawn = True
    def pew(self):
        p = PewPew(self.game, self.rect.x, self.rect.y)
        print(p.rect.x)
        print(p.rect.y)

            
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
    def collide_with_group(self, group, kill):
        hits = pg.sprite.spritecollide(self, group, kill)
        if hits:
            if str(hits[0].__class__.__name__) == "Coin":
                self.moneybag += 1
            if str(hits[0].__class__.__name__) == "PowerUp":
                "give gun for projectile"
            if str(hits[0].__class__.__name__) == "Magmawall":
                print("Collided with wall/ game over")
                self.HITPOINTS += -100



# Update the player,speed and collisons
    def update(self):
        self.get_keys()
        self.x += self.vx * self.game.dt
        self.y += self.vy * self.game.dt
        self.rect.x = self.x
        # add collision later
        self.collide_with_walls('x')
        self.rect.y = self.y
        # add collision later
        self.collide_with_walls('y')
        self.collide_with_group(self.game.coins, True)
        self.collide_with_group(self.game.power_ups, True)
        self.collide_with_group(self.game.magmawall, False)

        if self.HITPOINTS == 0:
            quit()

          
        # coin_hits = pg.sprite.spritecollide(self.game.coins, True)
        # if coin_hits:
        #     print("I got a coin")
       
# defines a class "wall" in the group Sprites
class Wall(pg.sprite.Sprite):
# Initiates the size, color, and where it is
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

# Makes "Coin" with sizes and color
class Coin(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.coins
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

# class PowerUp(pg.sprite.Sprite):
#     def __init__(self, game, x, y):
#         self.groups = game.all_sprites, game.power_ups
#         pg.sprite.Sprite.__init__(self, self.groups)
#         self.game = game
#         self.image = pg.Surface((TILESIZE, TILESIZE))
#         self.image.fill(ORANGE)
#         self.rect = self.image.get_rect()
#         self.x = x
#         self.y = y
#         self.rect.x = x * TILESIZE
#         self.rect.y = y * TILESIZE
# Makes the mob thingy and creates it size and other characteristics.
class Magmawall(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.magmawall
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.vx, self.vy = 100, 100
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.speed = 0.5
    def collide_with_walls(self, dir):
        if dir == 'x':
            # print('colliding on the x')
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                self.vx *= -1
                self.rect.x = self.x
        if dir == 'y':
            # print('colliding on the y')
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                self.vy *= -1
                self.rect.y = self.y
    def update(self):
        # self.rect.x += 1
        self.rect.x += TILESIZE * self.speed
        if self.rect.x > WIDTH-1 or self.rect.x < 1:
            self.speed *= -1
        
        self.rect.x = self.x
        self.collide_with_walls('x')
        self.rect.y = self.y
        self.collide_with_walls('y')

# The gun, shoots a projectile.
class PewPew(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.pew_pews
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE/4, TILESIZE/4))
        self.image.fill(ORANGE)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y
        self.speed = 25
        print("I created a pew pew...")
    def collide_with_group(self, group, kill):
        hits = pg.sprite.spritecollide(self, group, kill)
    def update(self):
        self.collide_with_group(self.game.magmawall, True)
        self.rect.x -= -self.speed
        # pass
# class Sword(pg.sprite.Sprite):
#     def __init__(self, game, x, y):
#         self.groups = game.all_sprites, game.weapons
#         pg.sprite.Sprite.__init__(self, self.groups)
#         self.game = game
#         self.image = pg.Surface((TILESIZE/4, TILESIZE))
#         self.image.fill(LIGHTBLUE)
#         self.rect = self.image.get_rect()
#         self.x = x
#         self.y = y
#         self.rect.x = x
#         self.rect.y = y
#         self.speed = 10
#         print("I created a sword")
#     def collide_with_group(self, group, kill):
#         hits = pg.sprite.spritecollide(self, group, kill)
#         if hits:
#             if str(hits[0].__class__.__name__) == "Mob":
#                 print("you kilt a mob!")
#     def update(self):
#         # self.collide_with_group(self.game.coins, True)
#         self.rect.x = self.game.player1.rect.x+TILESIZE
#         self.rect.y = self.game.player1.rect.y-TILESIZE
#         self.collide_with_group(self.game.mobs, True)
#         if not self.game.player1.weapon_drawn:
#             print("killed the sword")
#             self.kill()
#         # pass