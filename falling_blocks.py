import pygame
import random

BACKGROUND_COLOR = (0,0,0)
SCREEN_SIZE = (600, 800)
CAPTION = "not tetris"
BLOCK_SIZE = 32
FPS = 60
PIECES = [ [(1,0), (0,0), (2,0), (3,0)],
           [(1,0), (0,0), (2,0), (0,1)],
           [(1,0), (0,0), (2,0), (2,1)],
           [(1,0), (0,0), (0,1), (1,1)],
           [(1,0), (2,0), (0,1), (1,1)],
           [(1,0), (0,0), (1,1), (2,1)],
           [(1,0), (0,0), (2,0), (1,1)] ]

class Piece:

    def __init__(self):
        self.blocks = []
        self.timer = FPS
        self.movement_timer = FPS/3
        self.moving_down = False
        self.moving_right = False
        self.moving_left = False

        new_piece = random.choice(PIECES)
        for block in new_piece:
            self.blocks.append(Block(block[0], block[1], BLOCK_SIZE, (200,20,20)))

    def draw(self, screen):
        for block in self.blocks:
            block.draw(screen)

    def update(self, playbox, block_grid):
         
        self.timer -= 1
        self.movement_timer -= 1

        move_down = self.moving_down or self.timer == 0
        move_right = self.moving_right
        move_left = self.moving_left

        return_value = 0

        if (self.movement_timer > 0 or self.timer %6 != 0) and self.movement_timer != FPS/3:
            move_down = False
            move_right = False
            move_left = False
        for block in self.blocks:
            if block.y > 18 or block_grid[block.x][block.y+1] is not None:
                move_down = False
            elif block.x > 8 or block_grid[block.x+1][block.y] is not None:
                move_right = False
            elif block.x < 1 or block_grid[block.x-1][block.y] is not None:
                move_left = False

        if self.timer == 0:
            for block in self.blocks:
                if block.y == 19 or block_grid[block.x][block.y+1] is not None:
                    self.move_to_grid(block_grid)
                    move_down = False
                    move_right = False
                    move_left = False
                    return_value = -1
                    break
            self.timer = FPS

        if move_down:
            for block in self.blocks:
                block.y += 1 

        if move_right:
            for block in self.blocks:
                block.x += 1
        elif move_left:
            for block in self.blocks:
                block.x -= 1

        return return_value
           
    def move_to_grid(self, block_grid):
        for block in self.blocks:
            block_grid[block.x][block.y] = block

    def rotate_piece(self):
        pivot = self.blocks[0]
        for i in range(1,4):
            x_diff = pivot.x - self.blocks[i].x
            y_diff = pivot.y - self.blocks[i].y
            if x_diff == 0:
                self.blocks[i].y = pivot.y
                self.blocks[i].x = pivot.x - y_diff
            elif y_diff == 0:
                self.blocks[i].x = pivot.x
                self.blocks[i].y = pivot.y + x_diff
            elif x_diff < 0 and y_diff < 0:
                self.blocks[i].x = pivot.x - y_diff
                self.blocks[i].y = pivot.y + x_diff
            elif x_diff < 0 and y_diff > 0:
                self.blocks[i].x = pivot.x - y_diff
                self.blocks[i].y = pivot.y + x_diff
            elif x_diff > 0 and y_diff > 0:
                self.blocks[i].x = pivot.x - y_diff
                self.blocks[i].y = pivot.y + x_diff
            elif x_diff > 0 and y_diff < 0:
                self.blocks[i].x = pivot.x - y_diff
                self.blocks[i].y = pivot.y + x_diff

class Block:

    def __init__(self, x, y, size, color):
        self.x = x
        self.y = y
        self.size = size
        self.color = color

class Playbox:

    def __init__(self):
        self.height = BLOCK_SIZE * 20 
        self.width = BLOCK_SIZE * 10
        self.x = (SCREEN_SIZE[0]-self.width)/2 
        self.y = (SCREEN_SIZE[1]-self.height)/2
        self.color = (100,100,100)
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, screen):
       pygame.draw.rect(screen, self.color, self.rect) 

class Game:

    def __init__(self):
        self.done = False
        self.screen = pygame.display.get_surface()
        self.playbox = Playbox()
        self.block_grid = [[None for i in range(20)] for j in range(10)]
        self.clock = pygame.time.Clock()
        self.current_piece = Piece()
        print self.block_grid[0][19]

    def draw(self):
        self.screen.fill(BACKGROUND_COLOR)
        self.playbox.draw(self.screen)
        for block in self.current_piece.blocks:
            self.draw_block(block, self.screen, self.playbox)
        for row in self.block_grid:
            for block in row:
                if block is not None:
                    self.draw_block(block, self.screen, self.playbox)
        pygame.display.update()

    def draw_block(self, block, screen, playbox):
        draw_rect = pygame.Rect(block.x*BLOCK_SIZE+playbox.x,block.y*BLOCK_SIZE+playbox.y,BLOCK_SIZE, BLOCK_SIZE)
        pygame.draw.rect(screen, block.color, draw_rect)
        pygame.draw.rect(screen, (25,25,25), draw_rect, 2)

    def update(self):
        self.clock.tick(FPS)
        if self.current_piece.update(self.playbox, self.block_grid) == -1:
            self.current_piece = Piece()
        self.check_grid()

    def check_grid(self):
        for y in range(len(self.block_grid[0])):
            full = True
            for x in range(len(self.block_grid)):
                if self.block_grid[x][y] is None:
                    full = False
            if full:
                for x in range(len(self.block_grid)):
                    self.block_grid[x][y] = None
                self.grid_fall(y)

    def grid_fall(self, height):
        for x in range(len(self.block_grid)):
            for y in range(height-1, -1, -1):
                if self.block_grid[x][y] is not None:
                    self.block_grid[x][y].y += 1
                    self.block_grid[x][y+1] = self.block_grid[x][y]
                    self.block_grid[x][y] = None

    def player_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.done = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    self.current_piece.moving_right = True
                    self.current_piece.moving_left = False
                    self.current_piece.movement_timer = FPS/3 +1
                elif event.key == pygame.K_LEFT:
                    self.current_piece.moving_right = False
                    self.current_piece.moving_left = True
                    self.current_piece.movement_timer = FPS/3 +1
                elif event.key == pygame.K_DOWN:
                    self.current_piece.moving_down = True
                    self.current_piece.movement_timer = FPS/3 +1
                elif event.key == pygame.K_UP:
                    self.current_piece.rotate_piece()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    self.current_piece.moving_right = False
                elif event.key == pygame.K_LEFT:
                    self.current_piece.moving_left = False
                elif event.key == pygame.K_DOWN:
                    self.current_piece.moving_down = False

    def game_loop(self):
        self.player_input()
        self.update()
        self.draw()

if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption(CAPTION)
    pygame.display.set_mode(SCREEN_SIZE)
    game_instance = Game()
    while not game_instance.done:
        game_instance.game_loop()
    pygame.quit()
