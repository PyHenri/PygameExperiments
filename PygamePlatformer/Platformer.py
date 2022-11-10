import pygame
import sys

pygame.init()
Clock = pygame.time.Clock()
FPS = 60
size = [1000, 800]
bg = [255, 255, 255]
screen = pygame.display.set_mode(size)
pygame.display.set_caption('classes in pygame')


class Obstacle:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

class Level:
    def __init__(self,obstacles: list):
        self.obstacles = obstacles
    
    def block_add(self, x, y, width, height):
        self.obstacles.append(Obstacle(x=x,y=y,width=width,height=height))

    def draw(self):
        for block in self.obstacles:
            pygame.draw.rect(screen, (0, 0, 0), block.rect)

class Player:
    def __init__(self, x, y, width, height, speed, level_data):
        self.speed = speed
        self.jumping_speed = 16
        self.vel = 0  # velocity
        self.vel_y = 0  # jumping velocity
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.IsJump = False
        self.falling_speed = 0

        self.collision = [False, False]  # x, y
        self.on_bottom = False

        self.level_data = level_data  # getting all data about obstacles

    def handle_input(self):
        k = pygame.key.get_pressed()

        if k[pygame.K_LEFT]:
            self.vel = -self.speed
        elif k[pygame.K_RIGHT]:
            self.vel = +self.speed
        if k[pygame.K_UP] and self.jumping_speed == 16 and self.on_bottom:
            self.IsJump = True

    def jump(self):
        if self.IsJump:  # jump
            self.falling_speed = 0
            self.on_bottom = False
            if self.jumping_speed >= 0:
                self.vel_y = -self.jumping_speed
                self.jumping_speed -= 1
            else:
                self.IsJump = False
                self.jumping_speed = 16
    
    def gravity(self):
        # applying gravity
        if self.falling_speed <= 16 and not self.IsJump and not self.on_bottom:
            self.falling_speed += 3
        elif self.on_bottom:
            self.falling_speed = 1
        self.vel_y += self.falling_speed
        
    
    def detect_collision(self):
        # collision detection
        test_rect_x = pygame.Rect(self.x + self.vel, self.y, self.width, self.height)
        test_rect_y = pygame.Rect(self.x, self.y + self.vel_y, self.width, self.height)
        self.collision = [False, False]  # x, y
        self.on_bottom = False

        for block in self.level_data:
            if test_rect_x.colliderect(block.rect):  # checke ob es eine self.collision auf der x-achse gibt
                self.collision[0] = True
                if self.vel > 0:  # setzte player an block den er berührt um abstand zu verhindern
                    self.x = block.rect.left - self.width
                    test_rect_y.x = block.rect.left - self.width
                elif self.vel < 0:
                    self.x = block.rect.right
                    test_rect_y.x = block.rect.right

            if test_rect_y.colliderect(block.rect):  # checke ob es eine self.collision auf der y-achse gibt
                self.collision[1] = True
                if self.vel_y < 0:
                    self.y = block.rect.bottom
                    self.IsJump = False  # resete jump um an der decke fliegen zu verhindern
                    self.jumping_speed = 16
                elif self.vel_y > 0:
                    self.on_bottom = True
                    self.y = block.rect.top - self.height
                
            # Actually this only corrects one aspect.
            # You could still see the same problem in reverse,
            # as the x collision check is performed first
            # and doesn't take into account if there's been any movement in the y axis

    def update(self):
        self.handle_input()
        self.jump()
        self.gravity()
        self.detect_collision()

        # wenn es eine colision gibt:
        if self.collision[0]:
            # verhindere movement
            self.vel = 0
        if self.collision[1]:
            self.vel_y = 0

        # verändere player cords je nach velocity
        self.x += self.vel
        self.y += self.vel_y
        self.vel = 0
        self.vel_y = 0

    def draw(self):
        pygame.draw.rect(screen, (231, 111, 81), (self.x, self.y, self.width, self.height))

level = Level(obstacles=[])

level.block_add(0, size[1] - 50, size[0], 10)
level.block_add(100,size[1] - 100, 100, 20)
level.block_add(300,size[1] - 150, 70, 20)
level.block_add(500,size[1] - 150, 100, 20)
level.block_add(700,size[1] - 200, 70, 20)
level.block_add(900,size[1] - 250, 100, 20)

player = Player(500, 600, 20, 40, 4, level.obstacles)

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    level.draw()
    player.update()
    player.draw()
    

    Clock.tick(FPS)
    pygame.display.update()
    screen.fill(bg)
