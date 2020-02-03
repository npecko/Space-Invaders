import pygame
import random
import math
from pygame import mixer
from gameobjects import *

pygame.init()

screen = pygame.display.set_mode((1280, 720))

background = pygame.image.load('background.png')

mixer.music.load('background.wav')
mixer.music.play(-1)

pygame.display.set_caption('Space Invaders')
icon = pygame.image.load('logo.png')
pygame.display.set_icon(icon)

playerImg = pygame.image.load('player.png')
player = Player(610, 610)

enemyImg = pygame.image.load('enemy.png')
num_of_enemies = 6
enemies = []

for i in range (num_of_enemies):
    enemy = Enemy(random.randint(0, 1216), random.randint(50, 200), 3, 40)
    enemies.append(enemy)

rocketImg = pygame.image.load('rocket.png')
rocket = Rocket(0, 610, 10, 'ready')

score_value = 0
score_font = pygame.font.Font('space_age.ttf', 40)

over_font = pygame.font.Font('space_age.ttf', 128)

lives_font = pygame.font.Font('space_age.ttf', 40)
livesImg = pygame.image.load('heart.png')
number_of_lives = 3
livesX = 1140
lives = []

for i in range (number_of_lives):
    livesX += 30
    life = Life(livesX, 20)
    lives.append(life)

def show_score():
    score = score_font.render("Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (10, 10))
    global number_of_lives
    for i in range(number_of_lives):
        screen.blit(livesImg, (lives[i].x, lives[i].y))

def show_lives():
    lives = lives_font.render("Lives: ", True, (255, 255, 255))
    screen.blit(lives, (1000, 10))

def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (165, 250))

def draw_player(x, y):
    screen.blit(playerImg, (x, y))

def draw_enemy(x, y):
    screen.blit(enemyImg, (x, y))

def fire_rocket(x, y):
    rocket.rocket_state = 'fire'
    screen.blit(rocketImg, (x+16, y+10))

def isCollision(enemyX, enemyY, rocketX, rocketY):
    distance = math.sqrt(math.pow((enemyX - rocketX),2) + math.pow((enemyY - rocketY),2))
    if distance < 30:
        return True
    else:
        return False

running = True

while running:
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.x_change = -5
            if event.key == pygame.K_RIGHT:
                player.x_change = 5
            if event.key == pygame.K_SPACE:
                if rocket.rocket_state is 'ready':
                    rocket_sound = mixer.Sound('rocket.wav')
                    rocket_sound.play()
                    rocket.x = player.x
                    fire_rocket(rocket.x, rocket.y)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player.x_change = 0
    
    player.x += player.x_change
    
    if player.x <= 0:
        player.x = 0
    elif player.x >= 1216:
        player.x = 1216
    
    for i in range(num_of_enemies):
        if enemies[i].y > 550:
            number_of_lives -= 1
            enemies[i].y = random.randint(50, 200)
            break
    
        enemies[i].x += enemies[i].x_change
    
        if enemies[i].x <= 0:
            enemies[i].x_change = 3
            enemies[i].y += enemies[i].y_change
        elif enemies[i].x >= 1216:
            enemies[i].x_change = -3
            enemies[i].y += enemies[i].y_change
    
        if isCollision(enemies[i].x, enemies[i].y, rocket.x, rocket.y):
            explosion_sound = mixer.Sound('explosion.wav')
            explosion_sound.play()
            rocket.y = 610
            rocket.rocket_state = 'ready'
            score_value += 10
            enemies[i].x = random.randint(0, 1216)
            enemies[i].y = random.randint(50, 200)
    
        if number_of_lives > 0:
            draw_enemy(enemies[i].x, enemies[i].y)
    
    if rocket.y <= 0:
        rocket.y = 610
        rocket.rocket_state = 'ready'
    
    if rocket.rocket_state is 'fire':
        fire_rocket(rocket.x, rocket.y)
        rocket.y -= rocket.y_change
    
    if number_of_lives <= 0:
        game_over_text()

    if number_of_lives > 0:
        draw_player(player.x, player.y)
    show_score()
    show_lives()

    pygame.display.update()