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
        game_folder = path.dirname(__file__)
        self.map_data = []
        # 'r'     open for reading (default)
        # 'w'     open for writing, truncating the file first
        # 'x'     open for exclusive creation, failing if the file already exists
        # 'a'     open for writing, appending to the end of the file if it exists
        # 'b'     binary mode
        # 't'     text mode (default)
        # '+'     open a disk file for updating (reading and writing)
        # 'U'     universal newlines mode (deprecated)
        # below opens file for reading in text mode
        # with 
        '''
        The with statement is a context manager in Python. 
        It is used to ensure that a resource is properly closed or released 
        after it is used. This can help to prevent errors and leaks.
        '''
        with open(path.join(game_folder, 'map.txt'), 'rt') as f:
            for line in f:
                print(line)
                self.map_data.append(line)
    

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
            self.screen.fill(BGCOLOR)
            self.draw_grid()
            self.all_sprites.draw(self.screen)
            self.draw_text(self.screen, str(self.player1.HITPOINTS), 64, WHITE, 2, 2)

            pg.display.flip()


    def draw(self):
        # Fill screen with color
        self.screen.fill(BGCOLOR)
        # draw grid
        # self.draw_grid()
        # Draw all sprites
        self.all_sprites.draw(self.screen)
        pg.display.flip()
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
# g.show_start_screen()
while True:
    g.new() 
    g.run()
    # g.show_go_screen()