import pygame
import copy
pygame.init()

running = True
SCREEN_SIZE = WIDTH, HEIGHT = 750, 750
TITLE = "Card Game"
BACKGROUND = (0,0,0)
clock = pygame.time.Clock()
font = pygame.font.Font('freesansbold.ttf', 32)

pygame.display.set_caption(TITLE)
screen = pygame.display.set_mode(SCREEN_SIZE)


class Card:
    # global variables in Class:
    card_selected = False
    heighest_z = 0

    def __init__(self, z_index: int, position: tuple, name: str, health: int, power: int, special_effects: str):

        self.z_index = z_index
        self.active = False
        self.rect = pygame.Rect(position[0],position[1],100,100)
        self.drag_offset = pygame.Vector2()

        self.info = {
            "name": name,
            "health": health,
            "power": power,
            "special_effects": special_effects,
        }

        if self.z_index > Card.heighest_z:
            Card.heighest_z = self.z_index
    
    def handle_events(self, events, deck):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and not Card.card_selected:

                if self.rect.collidepoint(event.pos):
                    Card.card_selected = True
                    self.active = True
                    self.drag_offset = pygame.Vector2(event.pos) - self.rect.topleft

                    # Last Taken Card should have the highest z-index
                    cards_1 = copy.deepcopy(deck.cards)
                    cards_2 = copy.deepcopy(deck.cards)

                    for idx, card in enumerate(cards): # find index in desk of card
                        if card.z_index == self.z_index:
                            target_pos = idx
                            cards_1[idx].z_index = Card.heighest_z
                            break

                    # create the target_pos for a reversed list
                    cards_2[target_pos] = "here"
                    cards_2 = cards_2[::-1]
                    my_pos_reversed = cards_2.index("here")

                    for idx in range(len(cards)):
                        if idx == my_pos_reversed:
                            break
                        cards_1[::-1][idx].z_index -= 1

                    # sort cards:
                    cards_1.sort(key=lambda x: x.z_index)
                    deck.cards = cards_1

            elif event.type == pygame.MOUSEBUTTONUP and self.active:
                self.active = False
                Card.card_selected = False

    def drag(self):
        self.rect.topleft = pygame.Vector2(pygame.mouse.get_pos()) - self.drag_offset

    def draw(self):
        text = font.render(str(self.z_index), True, "green", "blue")
        textRect = text.get_rect()
        textRect.center = (self.rect.x, self.rect.y)
        screen.blit(text, textRect)
        if self.active:
            pygame.draw.rect(screen, (0,255,0), self.rect)
        else:
            pygame.draw.rect(screen, (255,0,0), self.rect)

    def update(self, events, cards):

        self.handle_events(events, cards)

        if not self.active: return # use Guard Clauses!!! They are cool!
        self.drag()

class Deck:
    def __init__(self, cards):
        self.cards = cards

    def update(self, events):
        # cards get reversed for update methode, because the Card with the lowest z_index should be looped at last
        cards_reversed = sorted(self.cards, key=lambda x: x.z_index, reverse=True)

        for card in cards_reversed:
            card.update(events, self)

        for card in self.cards:
            card.draw()


cards = [Card(i, (100 + i * 20, 75), "", 100, 100, "") for i in range(5)]
deck = Deck(cards)

while running:

    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit

    deck.update(events)

    clock.tick(120)
    pygame.display.update()
    screen.fill(BACKGROUND)
