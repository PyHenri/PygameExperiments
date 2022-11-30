import pygame
from config import *

pygame.init()
clock = pygame.time.Clock()
running = True
screen = pygame.display.set_mode((width, height))

time = 0

def drawGrid():
    for x in range(0, width, blockSize):
        for y in range(0, height, blockSize):
            rect = pygame.Rect(x, y, blockSize, blockSize)
            pygame.draw.rect(screen, "grey", rect, 1)

class Block:
    def __init__(self, pos):
        self.pos = pos
        self.placed = False
        self.direction = 1
        self.speed = 0.1

    def update(self):
        if not self.placed:
            if self.pos[0] == width//blockSize - 1:
                self.direction = -1
            elif self.pos[0] == 0:
                self.direction = 1

            self.pos[0] += self.direction

    def draw(self):
        pygame.draw.rect(screen, (0, 0, 0), (self.pos[0] * blockSize, self.pos[1] * blockSize, blockSize, blockSize))


class Tower:
    def __init__(self):
        self.max_tower_height = height//blockSize
        self.tower_height = 0
        self.blocks = [Block([0, height//blockSize - 1])]
        self.time = 0
        self.cool_down = 10


    def update(self):
        self.time += clock.get_time()
        if self.cool_down < 10:
            self.cool_down += 1

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.cool_down == 10:  # Place Block at position
            if self.blocks[self.tower_height].pos[0] == self.blocks[self.tower_height-1].pos[0] or len(self.blocks) == 1:
                self.blocks[self.tower_height].placed = True
                self.cool_down = 0
            else:
                running = False

        if self.time/1000 > self.blocks[self.tower_height].speed:
            self.time = 0

            self.blocks[self.tower_height].update()
            if self.blocks[self.tower_height].placed:  # If Block is placed, generate another one
                self.tower_height += 1
                self.blocks.append(Block([0, height//blockSize - 1 - self.tower_height]))

        for b in self.blocks:
            b.draw()


tower = Tower()


while running:
    screen.fill((255, 255, 255))
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False

    drawGrid()
    tower.update()
    
    clock.tick(60)
    pygame.display.flip()
    screen.fill((255, 255, 255))

pygame.quit()
