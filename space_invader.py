from pygame import mixer
import pygame
import random
import math

#import turtle

# initialize the pygame
pygame.init()

# create the screen
screen = pygame.display.set_mode((800, 600))
backgroundimg = pygame.image.load('dh6w_sbm8_210607.jpg')

# background sound
mixer.music.load('I lay my love on you.mp3')
mixer.music.play(-1)

# Title and Icon
pygame.display.set_caption('CeayHollertech Space Invader')
icon = pygame.image.load('image.png')
pygame.display.set_icon(icon)


# player
playerimg = pygame.image.load('002-arcade-game.png')
playerx = 370
playery = 480
playerX_change = 0

# enemy
enemyimg = []
enemyx = []
enemyy = []
enemyX_change = []
enemyY_change = []
number_of_enemies = 6

for i in range(number_of_enemies):
    enemyimg.append(pygame.image.load('enemy.png'))
    enemyx.append(random.randint(0, 735))
    enemyy.append(random.randint(0, 150))
    enemyX_change.append(1)
    enemyY_change.append(40)

# Bullet
bulletimg = pygame.image.load('001-bullet.png')
bulletx = 0
bullety = 480
bulletY_change = 5
bullet_state = 'ready'

# score
score_value = 0 
font = pygame.font.Font('Thai Coala - Personal Use.otf', 40)
textX = 10
textY = 10

# game over text
over_font = pygame.font.Font('Thai Coala - Personal Use.otf', 72)

def show_score(x, y):
    score = font.render('Score : ' + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

def game_over_text():
    over_text = over_font.render('GAME OVER', True, (255, 255, 255))
    screen.blit(over_text, (200, 250))
def player(x, y):
    screen.blit(playerimg, (x, y))

def enemy(x, y, i):
    screen.blit(enemyimg[i], (x, y))

def fire_bullet(x, y): 
    global bullet_state
    bullet_state = 'fire'
    screen.blit(bulletimg, (x + 16, y + 10))

def iscolission(enemyx, enemyy, bulletx, bullety):
    distance = math.sqrt(math.pow(enemyx - bulletx, 2)) + (math.pow(enemyy - bullety, 2))
    if distance < 27:
        return True

# Game loop
running = True
while running:

    # rgb
    screen.fill((0, 0, 0))

    # background image
    screen.blit(backgroundimg, (0,0))
    #playerx += 0.1
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # checking if key is pressed
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -0.5
            if event.key == pygame.K_RIGHT:
                playerX_change = 0.5
            if event.key == pygame.K_SPACE:
                if bullet_state == 'ready':
                    bulletx = playerx
                    fire_bullet(playerx, bullety) 
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                 playerX_change = 0

    # boundary   
    playerx += playerX_change
    if playerx < 0:
        playerx = 0

    elif playerx >= 736:
        playerx = 736

    # enemy movement
    for i in range(number_of_enemies):

        # Game over
        if enemyy[i] > 430:
            for j in range(number_of_enemies):
                enemyy[j] = 2000
            game_over_text()
            break
        

        enemyx[i] += enemyX_change[i]
        if enemyx[i] < 0:
            enemyX_change[i] = 1
            enemyy[i] += enemyY_change[i]

        elif enemyx[i] >= 736:
            enemyX_change[i] = -1
            enemyy[i] += enemyY_change[i]

        # collision
        collision = iscolission(enemyx[i], enemyy[i], bulletx, bullety)
        if collision:
            bullet_sound = mixer.Sound('mixkit-arcade-space-shooter-dead-notification-272.wav')
            bullet_sound.play()
            bullety = 480
            bullet_state = 'ready'
            score_value += 1
            enemyx[i] = random.randint(0, 735)
            enemyy[i] = random.randint(0, 150)

        enemy(enemyx[i], enemyy[i], i)

    # bullet movement
    if bullety < 0:
        bullety = 480
        bullet_state = 'ready'

    if bullet_state == 'fire':
        fire_bullet(bulletx, bullety)
        bullety -= bulletY_change

    player(playerx, playery)
    show_score(textX, textY)
    pygame.display.update() 