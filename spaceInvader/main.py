import pygame
import random
import math
from pygame import mixer

# Initialize the pygame
pygame.init()

# Title and Icon
pygame.display.set_caption("Space invaders")
icon = pygame.image.load("spaceInvader/space-shuttle.png")
pygame.display.set_icon(icon)

# Background
background = pygame.image.load("spaceInvader/background.jpg")

# Background sound
mixer.music.load("spaceInvader/background.wav")
mixer.music.play(-1)

# lazer sound

# create the screen
screen = pygame.display.set_mode((800, 600))

# player 
playerImg = pygame.image.load("spaceInvader/space-shuttle64.png")
playerX = 370
playerY = 480
playerX_change = 0

#alien
alienImg = []
alienX = []
alienY = []
alienX_change = []
alienY_change = []
number_of_enermies = 6

for i in range(number_of_enermies):
    alienChoice = "spaceInvader/" + random.choice(["alien1", "alien2", "alien3"]) + ".png"
    alienImg.append(pygame.image.load(alienChoice))
    alienX.append(random.randint(0, 735))
    alienY.append(random.randint(50, 350))
    alienX_change.append(0.3)
    alienY_change.append(40)

#Bullet
BulletImg = pygame.image.load("spaceInvader/bullet.png")
BulletX = 0
BulletY = 480
BulletX_change = 0
BulletY_change = 1.5
Bullet_state = "ready"

# score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10

def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (225, 255, 255))
    screen.blit(score, (x, y))

def player(x, y):
    screen.blit(playerImg, (x, y))

def alien(x, y, index):
    screen.blit(alienImg[index], (x, y))

def fire_bullet(x, y): 
    global Bullet_state
    Bullet_state = "fire"
    screen.blit(BulletImg, (x + 16, y + 10))

def isCollision(enermyX, enermyY, lazerX, lazerY):
    distance = math.sqrt((enermyX - lazerX)**2 + (lazerY - enermyY)**2)
    if distance < 27:
        return True
    return False

def game_over_text():
    score = font.render("GAME OVER", True, (225, 255, 255))
    screen.blit(score, (300, 250))

# Game loop
RUNNING = True
while RUNNING:
    #display
    screen.fill((0, 0, 0))
    screen.blit(background, (0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RUNNING = False

    # if keystroke is left or right
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                # print("left arrow pressed")
                playerX_change = -0.8
            if event.key == pygame.K_RIGHT:
                # print("right arrow pressed")
                playerX_change = 0.8
            if event.key == pygame.K_SPACE:
                if Bullet_state == "ready":
                    BulletX = playerX
                    fire_bullet(BulletX, BulletY)
                    Bullet_sound = mixer.Sound("spaceInvader/bullet.wav")
                    Bullet_sound.play()

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
                # print("key has been released")

    # player position change along x-axis
    playerX += playerX_change
 
    # boundery conditional for player
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # alien movement
    for i in range(number_of_enermies):
        # Game Over
        if alienY[i] > 440:
            for j in range(number_of_enermies):
                alienY[j] = 2000
            game_over_text()
            break


        alienX[i] += alienX_change[i]

        # alien boundery conditional
        if alienX[i] <= 0:
            alienX_change[i] = 0.3
            alienY[i] += alienY_change[i]
        elif alienX[i] >= 736:
            alienX_change[i] = -0.3
            alienY[i] += alienY_change[i]

        collision = isCollision(alienX[i], alienY[i], BulletX, BulletY)
        if collision:
            BulletY = 480
            Bullet_state = "ready"
            score_value += 1
            alienX[i] = random.randint(0, 735)
            alienY[i] = random.randint(50, 350)
            collision_sound = mixer.Sound("spaceInvader/hit.wav")
            collision_sound.play()

        alien(alienX[i], alienY[i], i)

    # bullet boundery  movement conditional
    if BulletY <= 0:
        BulletY = 480
        Bullet_state = "ready"

    # bullet movement conditional
    if Bullet_state == "fire":
        fire_bullet(BulletX, BulletY)
        BulletY -= BulletY_change

    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()
