import math
import random
import pygame

# Constants
sw = 800
sh = 500
player_x = 370
player_y = 380
enemy_miny = 50
enemy_maxy = 150
enemy_speedx = 4
enemy_speedy = 40
bullet_speedy = 10
collision_distance = 27

# Initialize
pygame.init()
screen = pygame.display.set_mode((sw, sh))

# Title
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('hostile.jpg')
pygame.display.set_icon(icon)
background = pygame.image.load('bg.jpg')

# Player
playerIMG = pygame.image.load('player.jpg')
playerX = player_x
playerY = player_y
playerX_change = 0

# OPFOR
enemyIMG = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
OPFORforce = 8

# Creating enemies
for _ in range(OPFORforce):
    enemyIMG.append(pygame.image.load('alien.jpg'))
    enemyX.append(random.randint(9, sw - 64))
    enemyY.append(random.randint(enemy_miny, enemy_maxy))
    enemyX_change.append(enemy_speedx)
    enemyY_change.append(enemy_speedy)

# Bullet
bulletIMG = pygame.image.load('bullet.jpg')
bulletX = 0
bulletY = player_y
bulletX_change = 0
bulletY_change = bullet_speedy
bullet_state = "ready"

# Scoring
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10

over_font = pygame.font.Font('freesansbold.ttf', 64)


def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def game_over():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))


def player(x, y):
    screen.blit(playerIMG, (x, y))


def enemy(x, y, i):
    screen.blit(enemyIMG[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletIMG, (x + 16, y + 10))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((enemyX - bulletX)**2 + (enemyY - bulletY)**2)
    return distance < collision_distance


running = True
while running:
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    for i in range(OPFORforce):
        if enemyY[i] > 340:
            for j in range(OPFORforce):
                enemyY[j] = 2000
            game_over()
            running = False
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 4
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -4
            enemyY[i] += enemyY_change[i]

        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            bulletY = 380
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(9, sw - 64)
            enemyY[i] = random.randint(enemy_miny, enemy_maxy)

        enemy(enemyX[i], enemyY[i], i)

    if bulletY <= 0:
        bulletY = 380
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()
