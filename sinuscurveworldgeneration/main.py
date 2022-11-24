import pygame
import math

pygame.init()
clock = pygame.time.Clock()

screen_width = 1000
screen_height = 800
tile_size = 5

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Platformer')


class Object:
    def __init__(self,x,y,width,height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
    def update(self):
        self.Platform = pygame.Rect(self.x,self.y,self.width,self.height)

class Player:
    def __init__(self,vel,x,y,width=50,height=100):  #init the player
        self.vel = vel
        self.vel_y = 16
        self.vel_y2 = 0
        self.vx = 0
        self.vy = 0
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.jump = False
        self.rect = pygame.Rect(self.x,self.y,self.width,self.height)

    def move(self):
        k = pygame.key.get_pressed()
        if k[pygame.K_LEFT]:  #go left
            self.vx = -self.vel
        if k[pygame.K_RIGHT]:  #go right
            self.vx = self.vel
        if k[pygame.K_UP] and self.vel_y == 16:  #checking conditions for jumping
            self.jump = True
        if self.jump:   #jump
            if self.vel_y >= -16:
                self.vy = -self.vel_y
                self.vel_y -= 1
            else:
                self.jump = False
                self.vel_y = 16
        if self.jump == False:  #gravity is only enabled when the player is not jumping
            self.vel_y2 += 1
            if self.vel_y2 > 10:
                self.vel_y2 = 10
            self.vy += self.vel_y2

        for block in blocks:   #get data of every block
            if block.Platform.colliderect(self.x + self.vx, self.y, self.width, self.height): #checking x collision
                self.vx = 0
            if block.Platform.colliderect(self.x, self.y + self.vy, self.width, self.height): #checking y collision
                self.vy = 0
                # if block.Platform.y > self.y: #prevents a bug that makes the player jump through the block below
                    # self.y += block.Platform.top-self.rect.bottom  #remove remaining distance between floor and player

        self.x += self.vx #adding velocity to coordinates
        self.y += self.vy
        self.vx = 0
        self.vy = 0
        self.rect = pygame.Rect(self.x,self.y,self.width,self.height)  #player rect

    def draw(self): #draw the player
        self.figur = pygame.draw.rect(screen,(255,255,255),(self.x,self.y,self.width,self.height))

    def do(self):
        self.move()
        self.draw()

player = Player(10,350,5,10,20) #setting up the level
blocks = list()


tiles = []

for i in range(int(screen_height/tile_size)):
    tiles.append([])
    for j in range(int(screen_width/tile_size)):
        tiles[i].append(0)




line = [(i, screen_width/2.5 + math.sin((math.radians(i*2)*1))*100) for i in range(screen_width)]

for i in line:
    b_x = int(i[0]/tile_size)
    b_y = int(i[1]/tile_size)
    tiles[b_y][b_x] = 1
    blocks.append(Object(int(i[0]),int(i[1]),tile_size,500))

for i, column in enumerate(tiles):
    for j, row in enumerate(column):
        if row == 1:
            for t in range(i+1,len(tiles)):
                tiles[t][j] = 2

##############################################################################################################################
run = True
while run:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    for idy,y in enumerate(tiles):
        for idx,x in enumerate(y):
            if x <= 0:
                pygame.draw.rect(screen,(47,157,226),(idx*tile_size,idy*tile_size,tile_size,tile_size)) #sky
            elif x == 1:
                pygame.draw.rect(screen,(65,152,10),(idx*tile_size,idy*tile_size,tile_size,tile_size)) #grass
            elif x > 1:
                pygame.draw.rect(screen,(86,52,27),(idx*tile_size,idy*tile_size,tile_size,tile_size)) #dirt

    for b in blocks:
        b.update()

    player.do()
    pygame.display.update()
    clock.tick(60)

pygame.quit()
