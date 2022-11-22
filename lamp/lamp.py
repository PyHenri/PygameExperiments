import pygame
pygame.init()
screen = pygame.display.set_mode((500, 500))
clock = pygame.time.Clock()

class lamp:
    def __init__(self, radius):
        self.radius = radius

        self.cover_surf = pygame.Surface((self.radius*2, self.radius*2))
        self.cover_surf.fill(0)

        self.cover_surf.set_colorkey((255, 255, 255))
        pygame.draw.circle(self.cover_surf, (255, 255, 255), (self.radius, self.radius), self.radius)

    def update(self):
        clip_center = pygame.mouse.get_pos()
        clip_rect = pygame.Rect(clip_center[0]-self.radius, clip_center[1]-self.radius, self.radius*2, self.radius*2)
        screen.set_clip(clip_rect)

        # draw the scene
        for x in range(10):
            for y in range(10):
                color = (255, 255, 255) if (x + y) % 2 == 0 else (255, 0, 0)
                pygame.draw.rect(screen, color, (x * 50, y * 50, 50, 50))

        # draw transparent circle and update display
        screen.blit(self.cover_surf, clip_rect)

lamp = lamp(100)

run = True
while run:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # clear screen and set clipping region
    screen.fill(0)

    lamp.update()
    pygame.display.update()
