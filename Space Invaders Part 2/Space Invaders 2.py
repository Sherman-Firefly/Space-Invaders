import math
import random
import pygame
from pygame import mixer

# Constants
sw = 800
sh = 500
player_x = 370
player_y = 380
enemy_miny = 50
enemy_maxy = 150
enemy_speedx = 1  # Slower speed
enemy_speedy = 3  # Slower speed
bullet_speedy = 2  # Slower speed
collision_distance = 27
OPFORforce = 8  # Max number of enemies

# Initialize
pygame.init()
screen = pygame.display.set_mode((sw, sh))

mixer.music.load("background.wav")
mixer.music.play(-1)
mixer.music.set_volume(0.3)

# Title
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('hostile.png')
pygame.display.set_icon(icon)
background = pygame.image.load('bg.jpg')

# Player
playerIMG = pygame.image.load('player.png')
playerX = player_x
playerY = player_y
playerX_change = 0

# Enemies
enemyIMG = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
enemyActive = [True] * OPFORforce  # Tracks if the enemy is currently active

# Create enemies
for _ in range(OPFORforce):
    enemyIMG.append(pygame.image.load('alien.png'))
    enemyX.append(random.randint(9, sw - 64))
    enemyY.append(random.randint(enemy_miny, enemy_maxy))
    enemyX_change.append(enemy_speedx)
    enemyY_change.append(enemy_speedy)

# Bullet
bulletIMG = pygame.image.load('bullet.png')
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
                playerX_change = -1  # Slower speed
            if event.key == pygame.K_RIGHT:
                playerX_change = 1  # Slower speed
            if event.key == pygame.K_SPACE:
                bulletSound = mixer.Sound("laser.wav")
                bulletSound.play()
                bulletSound.set_volume(0.4)
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

    active_enemies = 0  # Count active enemies

    for i in range(OPFORforce):
        if not enemyActive[i]:
            continue  # Skip inactive enemies

        active_enemies += 1

        # Game Over Condition
        if enemyY[i] > 340:
            for j in range(OPFORforce):
                enemyY[j] = 2000
            game_over()
            running = False
            break

        # Enemy Movement
        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = enemy_speedx
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -enemy_speedx
            enemyY[i] += enemyY_change[i]

        # Collision Detection
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosionSound = mixer.Sound("explosion.wav")
            explosionSound.play()
            explosionSound.set_volume(0.7)
            bulletY = 380
            bullet_state = "ready"
            score_value += 1
            enemyActive[i] = False  # Mark the enemy as inactive

        if enemyActive[i]:  # Only draw active enemies
            enemy(enemyX[i], enemyY[i], i)

    # End game if all enemies are defeated
    if active_enemies == 0:
        game_over()
        running = False

    # Bullet Movement
    if bulletY <= 0:
        bulletY = 380
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()
 