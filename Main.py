# This File was created by: Daniel Zhu
'''

Moving Enemy
Projectile
DIfferent levels/maps




'''
# Imports pygame as a shorter way to say it, also imports the values from a different tab called "Settings"
import pygame as pg
from Settings import *
from random import randint
from Sprites import *
import sys
from os import path

LEVEL1 = "level1.txt"
LEVEL2 = "level2.txt"
#create/define function "Game"
class Game:
    # Allows us to assign properties to the class
    def __init__(self):
        #  initilaize pygame
        pg.init()
        # When run, create a screen with the widths from settings and height from settings and called "Title" from settings.
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        # setting Game Clock
        self.clock = pg.time.Clock()
        self.load_data()
    def load_data(self):
       self.game_folder = path.dirname(__file__)
       self.map_data = []
       with open(path.join(self.game_folder, LEVEL1), 'rt') as f:
            for line in f:
                print(line)
                self.map_data.append(line)

    def test_method(self):
        print("I can be called from Sprites...")
    # added level change method
    def change_level(self, lvl):
        # kill all existing sprites first to save memory
        for s in self.all_sprites:
            s.kill()
        # reset criteria for changing level
        self.player1.moneybag = 0
        # reset map data list to empty
        self.map_data = []
        # open next level
        with open(path.join(self.game_folder, lvl), 'rt') as f:
            for line in f:
                print(line)
                self.map_data.append(line)
        # repopulate the level with stuff
        for row, tiles in enumerate(self.map_data):
            print(row)
            for col, tile in enumerate(tiles):
                print(col)
                if tile == '1':
                    print("a wall at", row, col)
                    Wall(self, col, row)
                if tile == 'P':
                    self.player1 = Player(self, col, row)
                if tile == 'C':
                    Coin(self, col, row)
                if tile == 'M':
                    Mob(self, col, row)
                if tile == 'S':
                    PowerUp(self, col, row)
        self.player1 = Player(self, 100, 100)
        # Puts "player" into "all sprites"
        self.all_sprites.add(self.player1)
        for x in range(10,20):
            Wall(self, x, 5)       

# creates a way to run the game.
    # defines the methow new.
    def new(self):
        # Creates a group "all sprites"
        self.all_sprites = pg.sprite.Group()
        # Puts walls into the group
        self.walls=pg.sprite.Group()
        self.coins=pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.power_ups = pg.sprite.Group()
        self.pew_pews = pg.sprite.Group()
        for row, tiles in enumerate(self.map_data):
            print(row)
            for col, tile in enumerate(tiles):
                print(col)
                if tile == '1':
                    print("a wall at", row, col)
                    Wall(self, col, row)
                if tile == 'P':
                    self.player1 = Player(self, col, row)
                if tile == 'C':
                    print("a coin at", col, row)
                    Coin(self, col,row)
                if tile == 'S':
                    print("a power up at", col, row)
                    PowerUp(self, col,row)
                if tile == 'M':
                    print("a mob at", col, row)
                    Mob(self, col, row)
        # Sets size of "player"
        self.player1 = Player(self, 100, 100)
        # Puts "player" into "all sprites"
        self.all_sprites.add(self.player1)
        for x in range(10,20):
            Wall(self, x, 5)

# Run the game
    def run(self):
        self.playing= True
        while self.playing:
            # Set fps
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()
    def quit(self):
        pg.quit()
        sys.exit()
    
    def update(self):
        self.all_sprites.update()
        if self.player1.moneybag > 0:
            self.change_level(LEVEL2)
# Sets the color and size of each tile for the grid.
    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x,0), (x,HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0,y), (WIDTH,y))

    def draw_text(self, surface, text, size, color, x, y):
        font_name = pg.font.match_font('arial')
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.topleft = (x*TILESIZE,y*TILESIZE)
        surface.blit(text_surface, text_rect)
    



    def draw(self):
        # Fill screen with color
        self.screen.fill(BGCOLOR)
        # draw grid
        # self.draw_grid()
        # Draw all sprites
        self.all_sprites.draw(self.screen)
        pg.display.flip()
    def show_start_screen(self):
        self.screen.fill(BGCOLOR)
        self.draw_text(self.screen, "This is the start screen", 24, WHITE, WIDTH/2 - 32, 2)
        pg.display.flip()
        self.wait_for_key()

    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.quit()
                if event.type == pg.KEYUP:
                    waiting = False
    def events(self):
        # Quit the game when hit x
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            # Moves the character left, up, right, down
            # if event.type == pg.KEYDOWN:
            #     if event.key == pg.K_a:
            #         self.player1.move(dx=-1)
            # if event.type ==pg.KEYDOWN:
            #     if event.key ==pg.K_d:
            #         self.player1.move(dx=1)
            # if event.type ==pg.KEYDOWN:
            #     if event.key ==pg.K_s:
            #         self.player1.move(dy=1)
            # if event.type ==pg.KEYDOWN:
            #     if event.key ==pg.K_w:
            #         self.player1.move(dy=-1)

#  Instatiate game
g = Game()
# Use game method to run the game
g.show_start_screen()

while True:
    g.new() 
    g.run()
    # g.show_go_screen()