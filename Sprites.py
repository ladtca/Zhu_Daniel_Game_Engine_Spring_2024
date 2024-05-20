# This file was created by: Daniel Zhu
# This code was inspired by Zelda and informed by Chris Bradfield


import pygame as pg
from Settings import *
from os import path
import random

SPRITESHEET = 'player.png'

dir = path.dirname(__file__)
img_dir = path.join(dir, 'images')


SPRITESHEET = "player.png"
game_folder = path.dirname(__file__)
img_folder = path.join(game_folder, 'images')
class Spritesheet:
    # utility class for loading and parsing spritesheets
    def __init__(self, filename):
        self.spritesheet = pg.image.load(filename).convert()

    def get_image(self, x, y, width, height):
        # grab an image out of a larger spritesheet
        image = pg.Surface((width, height))
        image.blit(self.spritesheet, (0, 0), (x, y, width, height))
        # image = pg.transform.scale(image, (width, height))
        image = pg.transform.scale(image, (width * 1, height * 1))
        return image
    
#defines a class "player" in the group sprites
class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.spritesheet = Spritesheet(path.join(img_folder, SPRITESHEET))
        self.load_images()
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        self.r_pressed = False
        self.e_pressed = False  
        self.sniper_cooldown = 2000  # Cooldown duration 
        self.last_sniper_shot = 0  
        self.pistol_cooldown = 500  # Cooldown duration 
        self.last_pistol_shot = 0  
        self.moneybag = 0
        self.speed = 450
        self.HITPOINTS = 100
        self.current_frame = 0
        self.walking = False
        self.last_update = 0
        self.choicegun = "pistol"
        self.display_timer = 0
        self.displayed_text = ""  # Initialize displayed text
        self.font = pg.font.Font(None, 36)  # Load a font
    
    def get_keys(self):
        self.vx, self.vy = 0, 0
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.vx = -self.speed
            self.walking = True
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.vx = self.speed
            self.walking = True
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.vy = -self.speed
            self.walking = True
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            self.vy = self.speed
            self.walking = True
        if keys[pg.K_e]:
            if not self.e_pressed:  # Only fire if the key was not already pressed
                if self.choicegun == 'pistol':
                    current_time = pg.time.get_ticks()
                    if current_time - self.last_pistol_shot >= self.pistol_cooldown:
                        self.pew()  # Fire the pistol
                        self.last_pistol_shot = current_time  # Update the time of the last shot
                elif self.choicegun == 'rifle':
                        self.riflepew()  # Fire the rifle  
                elif self.choicegun == 'sniper':
                    current_time = pg.time.get_ticks()
                    if current_time - self.last_sniper_shot >= self.sniper_cooldown:
                        self.sniperpew()  # Fire the sniper
                        self.last_sniper_shot = current_time  #
                self.e_pressed = True  
            else:
                self.e_pressed = False  # Reset the flag when the key is released
        if self.vx != 0 and self.vy != 0:
                self.vx *= 0.7071
                self.vy *= 0.7071
        if keys[pg.K_r] and not self.r_pressed:  # Check if 'R' is pressed and not already processed
            skibidi = ['rifle', 'pistol', 'sniper']
            self.choicegun = random.choice(skibidi)
            print(self.choicegun)
            self.displayed_text = f"You rolled {self.choicegun}!"  
            self.display_timer = 2000  
            self.r_pressed = True  
        if not keys[pg.K_r]:
            self.r_pressed = False  
    def pew(self):
        p = PewPew(self.game, self.rect.x, self.rect.y)

    def sniperpew(self):
        p = SniperPew(self.game, self.rect.x, self.rect.y)

    def riflepew(self):
        p = Rifle(self.game, self.rect.x, self.rect.y)

            
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
            if str(hits[0].__class__.__name__) == "Mob":
                print("Killed by mob")
                self.HITPOINTS += -100
    



# Update the player,speed and collisons
    def update(self):
        keys = pg.key.get_pressed()
        self.get_keys()
        self.animate()
        current_time = pg.time.get_ticks()
        if current_time - self.last_sniper_shot >= self.sniper_cooldown:
            self.e_pressed = False  # Reset sniper shot cooldown flag
        self.x += self.vx * self.game.dt
        self.y += self.vy * self.game.dt
        self.rect.x = self.x
        self.collide_with_walls('x')
        self.rect.y = self.y
        self.collide_with_walls('y')
        self.collide_with_group(self.game.coins, True)
        self.collide_with_group(self.game.power_ups, True)
        self.collide_with_group(self.game.mob, False)

        if self.HITPOINTS == 0:
            quit()
        if self.display_timer > 0:
            self.display_timer -= self.game.dt  # Decrease the timer
            if self.display_timer <= 0:
                self.displayed_text = ""  # Clear the displayed text when the timer is up
    def draw_text(self, text, font, color, x, y):
        text_surface = font.render(text, True, color)  # Render the text
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)  # Set the position of the text
        self.game.screen.blit(text_surface, text_rect)  # Draw the text on the screen

          
        # coin_hits = pg.sprite.spritecollide(self.game.coins, True)
        # if coin_hits:
        #     print("I got a coin")
    def load_images(self):
        self.standing_frames = [self.spritesheet.get_image(0,0, 32, 32), 
                                self.spritesheet.get_image(64,0, 32, 32)]
        self.walking_frames = [
                                self.spritesheet.get_image(0,9, 32, 32),
                                self.spritesheet.get_image(32,32, 32, 32),
                                self.spritesheet.get_image(64,32, 32, 32),
                                self.spritesheet.get_image(96,32, 32, 32),
                                ]
    def animate(self):
        now = pg.time.get_ticks()
        if now - self.last_update > 350:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.standing_frames)
            bottom = self.rect.bottom
            self.image = self.standing_frames[self.current_frame]
            self.rect = self.image.get_rect()
            if not self.walking:
                self.image = self.standing_frames[self.current_frame]
            else:
                self.image = self.walking_frames[self.current_frame]
            self.rect = self.image.get_rect()
            self.rect.bottom = bottom
    
       
# defines a class "wall" in the group Sprites
class Wall(pg.sprite.Sprite):
# Initiates the size, color, and where it is
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game 
        # self.image = pg.Surface((TILESIZE, TILESIZE)) 
        self.image = self.game.walls_img
        self.image = pg.transform.scale(self.image, (32, 32))
        # self.image.fill(WHITE)
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
        self.image = self.game.coins_img
        self.image = pg.transform.scale(self.image, (32,32))
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
class Mob(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.mob
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image = self.game.mob1_img
        self.image = pg.transform.scale(self.image, (32,32))
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.vx, self.vy = 100, 100
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.speed = 0.5
        self.HITPOINTS = 100
    def collide_with_walls(self, dir):
        if dir == 'x':
            # print('colliding on the x')
            hits = pg.sprite.spritecollide(self, self.game.walls, True)
            if hits:
                self.vx *= -1
                self.rect.x = self.x
        if dir == 'y':
            # print('colliding on the y')
            hits = pg.sprite.spritecollide(self, self.game.walls, True)
            if hits:
                self.vy *= -1
                self.rect.y = self.y
    def take_damage(self, damage):
        self.HITPOINTS -= damage  # Reduce hit points by the damage value
        if self.HITPOINTS <= 0:
            self.kill()  # Kill the mob if hit points drop to or below 0
    def update(self):
        # self.rect.x += 1
        self.rect.x += TILESIZE * self.speed
        if self.rect.x > WIDTH-1 or self.rect.x < 1:
            self.speed *= -1
        
        self.rect.x = self.x
        self.collide_with_walls('x')
        self.rect.y = self.y
        self.collide_with_walls('y')
    def collide_with_group(self, group, kill, damage):
        hits = pg.sprite.spritecollide(self, group, kill)
        for hit in hits:
            if isinstance(hit, PewPew) or isinstance(hit, SniperPew) or isinstance(hit, Rifle):
                hit.kill()  # Kill the projectile when it hits the mob
                self.take_damage(damage)  # Apply damage to the mob
        
# The gun, shoots a projectile.
class PewPew(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.pew_pews
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.damage = 20
        self.image = pg.Surface((TILESIZE/4, TILESIZE/4))
        self.image = self.game.bullet_img
        self.image = pg.transform.scale(self.image, (28,28))
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y
        self.speed = 25
    
    def update(self):
        if pg.sprite.spritecollideany(self, self.game.walls):
            self.kill()  # Remove bullet if it hits a wall
        self.collide_with_group(self.game.mob, False)
        self.rect.x += self.speed

    def collide_with_group(self, group, kill):
        hits = pg.sprite.spritecollide(self, group, kill)
        for hit in hits:
            if isinstance(hit, Mob):
                hit.take_damage(self.damage)
                self.kill()
class SniperPew(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.sniper_pew
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.damage = 100
        self.image = pg.Surface((TILESIZE/4, TILESIZE/4))
        self.image = self.game.bullet_img
        self.image = pg.transform.scale(self.image, (28,28))
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y
        self.speed = 50
    
    def update(self):
        if pg.sprite.spritecollideany(self, self.game.walls):
            self.kill()  # Remove bullet if it hits a wall
        self.collide_with_group(self.game.mob, False)
        self.rect.x += self.speed

    def collide_with_group(self, group, kill):
        hits = pg.sprite.spritecollide(self, group, kill)
        for hit in hits:
            if isinstance(hit, Mob):
                hit.take_damage(self.damage)
                self.kill()
class Rifle(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.rifle_pew
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.damage = 10
        self.image = pg.Surface((TILESIZE/4, TILESIZE/4))
        self.image = self.game.bullet_img
        self.image = pg.transform.scale(self.image, (28,28))
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y
        self.speed = 15
    
    def update(self):
        if pg.sprite.spritecollideany(self, self.game.walls):
            self.kill()  # Remove bullet if it hits a wall
        self.collide_with_group(self.game.mob, False)
        self.rect.x += self.speed

    def collide_with_group(self, group, kill):
        hits = pg.sprite.spritecollide(self, group, kill)
        for hit in hits:
            if isinstance(hit, Mob):
                hit.take_damage(self.damage)
                self.kill()
    
    
        
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