import pygame
import random
from pygame import mixer

sw, sh = 500, 400
ms = 5
fs = 72

pygame.init()

bg_img = pygame.transform.scale(pygame.image.load("bg (1).jpg"), (sw, sh))
font = pygame.font.Font('freesansbold.ttf', 32)

score_value = 0
textX, textY = 10, 10

def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

class Sprite(pygame.sprite.Sprite):
    def __init__(self, color, height, width):
        super().__init__()
        self.image = pygame.Surface([width, height])
        pygame.draw.rect(self.image, color, pygame.Rect(0, 0, width, height))
        self.rect = self.image.get_rect()

    def move(self, x_change, y_change):
        self.rect.x = max(min(self.rect.x + x_change, sw - self.rect.width), 0)
        self.rect.y = max(min(self.rect.y + y_change, sh - self.rect.height), 0)

screen = pygame.display.set_mode((sw, sh))
pygame.display.set_caption("Score Increases on Collision")

allsprite = pygame.sprite.Group()

sprite1 = Sprite(pygame.Color("yellow"), 20, 20)
sprite1.rect.x, sprite1.rect.y = random.randint(0, sw - sprite1.rect.width), random.randint(0, sh - sprite1.rect.height)
allsprite.add(sprite1)

sprite2 = Sprite(pygame.Color("green"), 20, 20)
sprite2.rect.x, sprite2.rect.y = random.randint(0, sw - sprite2.rect.width), random.randint(0, sh - sprite2.rect.height)
allsprite.add(sprite2)

running = True
clock = pygame.time.Clock()

def spawn_new_box():
    new_box = Sprite(pygame.Color("green"), 20, 20)
    new_box.rect.x, new_box.rect.y = random.randint(0, sw - new_box.rect.width), random.randint(0, sh - new_box.rect.height)
    allsprite.add(new_box)
    return new_box

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_x):
            running = False

    screen.blit(bg_img, (0, 0))

    keys = pygame.key.get_pressed()
    x_change = (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * ms
    y_change = (keys[pygame.K_DOWN] - keys[pygame.K_UP]) * ms
    sprite1.move(x_change, y_change)

    if sprite1.rect.colliderect(sprite2.rect):
        
        score_value += 1
        allsprite.remove(sprite2)
        sprite2 = spawn_new_box()

    allsprite.update()
    allsprite.draw(screen)
    show_score(textX, textY)

    pygame.display.flip()
    clock.tick(90)

pygame.quit()
