import pygame,sys

pygame.init()
Clock = pygame.time.Clock()
FPS = 60
size = [1000,800]
bg = [0,0,0]
screen = pygame.display.set_mode(size)
pygame.display.set_caption('classes in pygame')


class Player:
    def __init__(self,vel,x,y):
        self.vel = vel
        self.vel_y = 16
        self.x = x
        self.y = y
        self.jump = False

    def move(self):
        k = pygame.key.get_pressed()
        if k[pygame.K_LEFT]:
            self.x -= self.vel
        if k[pygame.K_RIGHT]:
            self.x += self.vel
        if k[pygame.K_UP] and self.vel_y == 16:
            self.jump = True
        if self.jump:
            pass
            if self.vel_y >= -16:
                self.y -= self.vel_y
                self.vel_y -= 1
            else:
                self.jump = False
                self.vel_y = 16

    def draw(self):
        pygame.draw.rect(screen,(255,255,255),(self.x,self.y,50,100))

    def do(self):
        self.move()
        self.draw()
        
    

player = Player(2,500,600)

while True:
    screen.fill(bg)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    player.do()
    Clock.tick(FPS)
    pygame.display.update()
