import sys
import pygame
import random
import math
from pygame import mixer

# Initialize the pygame.
pygame.init()

# Background music and game over music
game_over_sound = mixer.Sound("gameover.wav")
mixer.music.load("backgroundmusic.wav")
mixer.music.play(-1)


# Setting the screen sizes. Where 800 is width and 600 is height.
screen = pygame.display.set_mode((800, 600))

# Setting background image
background = pygame.image.load("back_ground.png")


# Caption and Icon.
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('enemy.png')
pygame.display.set_icon(icon)

# Player and its position
player_image = pygame.image.load('player.png')
playerX = 375
playerY = 500
playerX_change = 0

# Enemy
enemy_image = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
no_of_enemies = 6


for i in range(no_of_enemies):
    enemy_image.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50, 200))
    enemyX_change.append(3)
    enemyY_change.append(40)

# Bullet
bullet_image = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 20
bullet_state = "ready"


# Score
score_value = 0
font = pygame.font.Font("stargedi.TTF", 32)
textX = 10
textY = 10

# Game over text
game_over = pygame.font.Font("stargedi.TTF", 64)


def game_over_music():
    mixer.music.stop()
    mixer.Sound.play(game_over_sound)


def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def player(x, y):
    # blit means TO DRAW
    screen.blit(player_image, (x, y))


def enemy(x, y, i):
    screen.blit(enemy_image[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet_image, (x + 16, y + 10))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if distance < 25:
        return True
    else:
        return False


def game_over_text():
    text = game_over.render("Game over", True, (255, 255, 255))
    screen.blit(text, (200, 250))


# To make the screen appear constantly.
while True:
    # Screen.fill is placed in while loop because it should appear constantly as the screen. RGB - red, green, blue
    screen.fill((0, 0, 0))

    # Background image set
    screen.blit(background, (0, 0))

    for event in pygame.event.get():

        # Key Stroke left or right
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bulletX = playerX
                    bullet_sound = mixer.Sound("laser.wav")
                    bullet_sound.play()
                    # Get the current X coordinates of player (Spaceship)
                    fire_bullet(bulletX, bulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

        # To exit the game
        if event.type == pygame.QUIT:
            sys.exit()

    # Checking for player boundaries so it doesn't go out of bounds
    # Player Movement
    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # Checking for enemy boundaries X position so it doesn't go out of bounds
    # Enemy Movement
    for i in range(no_of_enemies):

        # Game over
        if enemyY[i] > 450:
            for j in range(no_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            game_over_music()

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 2.5
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -2.5
            enemyY[i] += enemyY_change[i]

    # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            collision_sound = mixer.Sound("blast.wav")
            collision_sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value = score_value + 1
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 200)

        if score_value % 10 == 0 and score_value != 0:
            enemyY_change[i] += 0.1

        enemy(enemyX[i], enemyY[i], i)

    # Bullet Movement
    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    player(playerX, playerY)
    show_score(textX, textY)

# Every time when a new element is included the display has to be UPDATED.
    pygame.display.update()
