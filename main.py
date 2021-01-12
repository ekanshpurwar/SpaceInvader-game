import pygame
import random
import math
from pygame import mixer

# Press control + alt+ l to format python code properly
'''Anything happening inside the game window is known as event'''

# Initialize game
pygame.init()

# Create the screen
screen = pygame.display.set_mode((800, 600))

# Loading image for background
background = pygame.image.load("background.png")

# Game title and icon on game window
pygame.display.set_caption("SpaceInvader")
icon = pygame.image.load("ufo.png")
pygame.display.set_icon(icon)

# Background music
mixer.music.load("background.wav")
mixer.music.play(-1)

# Player
playerImg = pygame.image.load("player.png")
playerX = 370
playerY = 480
playerX_change = 0

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_enemies = 6
for i in range(num_enemies):
    enemyImg.append(pygame.image.load("enemy.png"))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(4)
    enemyY_change.append(20)

# Bullet
bulletImg = pygame.image.load("bullet.png")
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"

# Score
''''''
score_value = 0
font = pygame.font.Font("freesansbold.ttf", 32)
textX = 10
textY = 10

# Game over
game_over_font = pygame.font.Font("freesansbold.ttf", 64)
game_overX = 250
game_overY = 250


# Functions

def game_over(x, y):
    game_over_text = font.render("Game Over !", True, (255, 255, 255))
    screen.blit(game_over_text, (x, y))


def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def player(x, y):
    screen.blit(playerImg, (x, y))  # blit method is used to draw an image to the screen


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))  # blit method is used to draw an image to the screen


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))  # blit method is used to draw an image to the screen


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - enemyY, 2)) + (math.pow(bulletX - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


running = True
while running:

    # Change background color
    screen.fill((0, 255, 0))

    # Change background image
    screen.blit(background, (0, 0))  # Here(0,0) are coordinate from where background image to be appeared

    for event in pygame.event.get():  # To loop through all the event happening inside the game

        # Quit Event
        if event.type == pygame.QUIT:  # To check if event type is quit happend which is done by pressing the cross button on window
            running = False

        # Events
        # To check is the left arrow or right arrow key event is happend
        if event.type == pygame.KEYDOWN:  # keydown means if key is presses
            if event.key == pygame.K_LEFT:
                # print("Left key is pressed")
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                # print("Right key is pressed")
                playerX_change = 5
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    # play bullet sound
                    bullet_sound = mixer.Sound("laser.wav")
                    bullet_sound.play()

                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:  # keyup means if key is released
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # Player Movement
    playerX += playerX_change
    '''Check if player reaches to boundary then it should not cross the bounds'''
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:  # 800-64=736 because width of spaceship is 64px
        playerX = 736

    for i in range(num_enemies):

        # Game over
        if enemyY[i] > 440:
            for j in range(num_enemies):
                enemyY[j] = 2000 # if enemy is closer to spaceship then send enemy out of window in y-axis
            game_over(game_overX, game_overY)
            break

        # Enemy Movement
        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 4
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:  # 800-64=736 because width of spaceship is 64px
            enemyX_change[i] = -4
            enemyY[i] += enemyY_change[i]

        # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            # Adding collision sound
            collision_sound = mixer.Sound("explosion.wav")
            collision_sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    # Bullet Movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    # Function call
    show_score(textX, textY)
    player(playerX, playerY)
    pygame.display.update()  # so that the display always get updating whenever any event happens
