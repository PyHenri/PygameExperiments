# import all modules
import pygame
import sys

# init the game
pygame.init()
WIDTH = 500
HEIGHT = 500
FPS = 60
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("game")
clock = pygame.time.Clock()


class Player:
    # init the player
    def __init__(self, x, y, width, height, world):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.speed = 5
        self.velocity = [0,0] # current speed [x,y]
        self.worldshift = [0,0] # amount the world has been shifted
        self.scroll = [0,0] # camera movement

        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.pos = [self.rect.x + self.worldshift[0], self.rect.y + self.worldshift[1]]

        self.world = world

        self.special_ability = None
        self.ability_recharge = 0

    # handle all events
    def handle_events(self, keys):
        # reset all velocity values
        self.velocity = [0,0]
        self.scroll = [0,0]

        # basic movement
        if keys[pygame.K_a]:
            self.velocity[0] = -self.speed
        if keys[pygame.K_d]:
            self.velocity[0] = self.speed
        if keys[pygame.K_w]:
            self.velocity[1] = -self.speed
        if keys[pygame.K_s]:
            self.velocity[1] = self.speed
        if keys[pygame.K_q] and self.special_ability is None and self.ability_recharge == 0:
            self.special_ability = "dash"
            self.dash_distance = 50

    # prevent collisions
    def detect_collisions(self):
        # Collision Detection works like this:
        # 1. Create a rect as a copy from the player rect, but with the velocity applied, which is not yet applied to the official player rect
        # 2. Loop through all obstacles and detect collisions
        # 3. Find the Collision-side and block movement for the x/y velocity, so that the player cant move through the block
        # 4. move the player rect by the distance between block and player, to remove gaps between block and player


        future_rect = pygame.Rect(self.rect.x + self.velocity[0], self.rect.y+ self.velocity[1], self.width, self.height)
        for obstacle in self.world:

            if obstacle.type != "no_coll": 
                # add worldshift to obstacle
                real_obstacle = pygame.Rect(obstacle.x-self.worldshift[0], obstacle.y-self.worldshift[1], obstacle.width, obstacle.height)
                # if obstacle in range:
                if real_obstacle.x + real_obstacle.width > 0 and real_obstacle.x < WIDTH and real_obstacle.y + real_obstacle.height > 0 and real_obstacle.y < HEIGHT:
                    if future_rect.colliderect(real_obstacle):

                        if self.velocity[0] > 0: # Moving right
                            distance = future_rect.right - real_obstacle.left
                            if distance <= self.velocity[0]:
                                self.velocity[0] = 0
                                self.rect.x = real_obstacle.left-self.rect.width
                        elif self.velocity[0] < 0: # Moving left
                            distance = future_rect.left - real_obstacle.right
                            if distance >= self.velocity[0]:
                                self.velocity[0] = 0
                                self.rect.x = real_obstacle.right

                        if self.velocity[1] > 0: # Moving down
                            distance = future_rect.bottom - real_obstacle.top
                            if distance <= self.velocity[1]:
                                self.velocity[1] = 0
                                self.rect.y = real_obstacle.top - self.rect.width
                        elif self.velocity[1] < 0: # Moving up
                            distance = future_rect.top - real_obstacle.bottom
                            if distance >= self.velocity[1]:
                                self.velocity[1] = 0
                                self.rect.y = real_obstacle.bottom

    # dash ability
    def dash(self):
        # always uses guard clauses they are cool
        if not self.special_ability == "dash": return
        if self.dash_distance//10 == 0 or self.dash_distance < 1: self.special_ability = None; self.ability_recharge = 100

        self.velocity[0] *= self.dash_distance//10
        self.velocity[1] *= self.dash_distance//10
        self.dash_distance -= 1

    # camera system
    def camera(self):
        player_x = self.rect.centerx
        player_y = self.rect.centery
        
        # if player x hits border of box camera
        if player_x < WIDTH/5 and self.velocity[0] < 0:
            self.scroll[0] = self.velocity[0]
            player.velocity[0] = 0

        elif player_x > WIDTH - WIDTH/5 and self.velocity[0] > 0:
            self.scroll[0] = self.velocity[0]
            player.velocity[0] = 0
        
        # if player y hits border of box camera
        if player_y < HEIGHT/5 and self.velocity[1] < 0:
            self.scroll[1] = self.velocity[1]
            player.velocity[1] = 0

        elif player_y > HEIGHT - HEIGHT/5 and self.velocity[1] > 0:
            self.scroll[1] = self.velocity[1]
            player.velocity[1] = 0

    # handle the movement
    def move(self):
        
        # prevent high velocity while traveling diagional
        if self.velocity[0] != 0 and self.velocity[1] != 0:
            self.velocity[0] = round(self.velocity[0] * 0.707)
            self.velocity[1] = round(self.velocity[1] * 0.707)

        self.dash()
        self.detect_collisions()
        self.camera()

        # add velocity to x,y
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        # add scroll to worldshift
        self.worldshift[0] += self.scroll[0]
        self.worldshift[1] += self.scroll[1]

        # calculate real position
        self.pos = [self.rect.x+self.worldshift[0],self.rect.y+self.worldshift[1]]

    # update the player
    def update(self, display):
        if self.ability_recharge > 0:
            self.ability_recharge -= 1
        keys = pygame.key.get_pressed()
        self.handle_events(keys)

        self.move()
        pygame.draw.rect(display, (255, 0, 0), self.rect)


class Obstacle:
    def __init__(self, x, y, width, height, type="block"):
        # types:
        #   block: basic block
        #   no_coll: block without collisions 
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.type = type
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)


class World:
    def __init__(self):
        self.world = []

    def object_add(self, obstacle):
        self.world.append(obstacle)

    def draw(self):
        for obstacle in self.world:
            # if obstacle on screen
            if obstacle.x + obstacle.width - player.worldshift[0] > 0 and obstacle.x - player.worldshift[0] < WIDTH and obstacle.y + obstacle.height - player.worldshift[1] > 0 and obstacle.y - player.worldshift[1] < HEIGHT:
                # then draw it
                pygame.draw.rect(screen, (0,0,0), (obstacle.x-player.worldshift[0], obstacle.y-player.worldshift[1], obstacle.width, obstacle.height))


world = World()
world.object_add(Obstacle(100,100,100,100))
world.object_add(Obstacle(100,500,100,100))
world.object_add(Obstacle(100,800,100,100))
player = Player(400, 300, 32, 32, world.world)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    world.draw()
    player.update(screen)

    pygame.display.update()
    clock.tick(FPS)
    screen.fill((255,255,255))
