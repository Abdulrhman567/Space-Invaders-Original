import pygame
from random import randint
import os
import sys

pygame.font.init()
pygame.mixer.init()

# COLORS
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# FONTS
LOSER_FONT = pygame.font.SysFont("comicsans", 100)
SCORE_FONT = pygame.font.SysFont("comicsans", 30)
HIGHEST_SCORE_FONT = pygame.font.SysFont("comicsans", 20)

# SOUNDS

BACKGROUND_TRACK = pygame.mixer.Sound(os.path.join('Assets', 'background.wav'))
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'laser.wav'))
DESTRUCTION_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'explosion.wav'))

# RESOLUTION AND FPS
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
FPS = 60

# VELOCITY
# 5, 4, 1
PLAYER_VEL = 5
BULLET_VEL = 5
ENEMY_VEL = 2

# ENEMIES AND BULLETS NUMBERS
MAX_BULLETS = 3
MAX_ENEMIES = 10

# EVENTS

PLAYER_HIT = pygame.USEREVENT + 1
ENEMY_HIT = pygame.USEREVENT + 2

# LOADING IMAGES
PLAYER = pygame.image.load(os.path.join('Assets', 'player.png'))
BULLET = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'bullet.png')), (13, 15))
ENEMY = pygame.image.load(os.path.join('Assets', 'ufo.png'))
SPACE = pygame.image.load(os.path.join('Assets', 'background.png'))

# CREATING WINDOW
WINDOW = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space Invaders Original!")


def handle_player_movement(key_pressed, player):
    """
    Moves the spaceship left when pressing the left key and moves it right when pressing the right key
    :param key_pressed: key_pressed
    :param player: player
    :return: None
    """
    if key_pressed[pygame.K_LEFT] and player.x > 0:
        player.x -= PLAYER_VEL
    if key_pressed[pygame.K_RIGHT] and player.x < SCREEN_WIDTH - player.width:
        player.x += PLAYER_VEL


def handle_bullets(player_bullets, enemies):
    """
    handles the bullets movements and when it collides with the enemies it disappears
    or when it gets out of the screen boundaries
    :param player_bullets: player_bullets
    :param enemies: enemies
    :return: None
    """
    for bullet in player_bullets:
        bullet.y -= BULLET_VEL
        for enemy in enemies:
            if bullet.colliderect(enemy):
                pygame.event.post(pygame.event.Event(ENEMY_HIT))
                enemies.remove(enemy)
                player_bullets.remove(bullet)
        if bullet.y < 0:
            player_bullets.remove(bullet)


def produce_enemies(enemies):
    """
    Picks a random position for the enemy and puts the enemy at that position
    :param enemies: enemies
    :return: None
    """
    x_pos = randint(0, SCREEN_WIDTH - ENEMY.get_width())
    y_pos = randint(0, SCREEN_HEIGHT - 400)
    enemy = pygame.Rect(x_pos, y_pos, ENEMY.get_width(), ENEMY.get_height())
    enemies.append(enemy)


def handle_enemies(player, enemies):
    """
    handles the enemies movements and when an enemy collides with the spaceship or
    when the enemy gets out of the screen boundaries
    :param player: player
    :param enemies: enemies
    :return:None
    """
    for enemy in enemies:
        enemy.y += ENEMY_VEL
        if player.colliderect(enemy):
            pygame.event.post(pygame.event.Event(PLAYER_HIT))
        elif enemy.y > SCREEN_HEIGHT:
            enemies.remove(enemy)


def highest_score(score):
    """
    returns the highest score from the txt file by comparing the last highest score
    and your current score and returns the highest
    :param score: score
    :return:
    """
    with open("High-score.txt", "r") as file:
        high_score = int(file.read())

    if score > high_score:
        with open("High-score.txt", "w") as file:
            file.write(str(score))

    with open("High-score.txt", 'r') as file:
        high_score = file.read()

    return high_score


def draw_window(player, player_bullets, enemies, score):
    """
    Displays(Draws)the different objects on the screen
    :param player: player
    :param player_bullets: player_bullets
    :param enemies: enemies
    :param score: score
    :return: None
    """
    WINDOW.blit(SPACE, (0, 0))

    score_text = SCORE_FONT.render(f'Score: {score}', 1, WHITE)
    WINDOW.blit(score_text, (10, 10))

    WINDOW.blit(PLAYER, (player.x, player.y))

    for enemy in enemies:
        WINDOW.blit(ENEMY, (enemy.x, enemy.y))

    for bullet in player_bullets:
        WINDOW.blit(BULLET, (bullet.x, bullet.y))

    pygame.display.update()


def game_over(loser_text, score):
    """
    Displays(Draws)the loser text, final score and the highest score when an enemy collides with the spaceship
    :param loser_text: loser_text
    :param score: score
    :return: None
    """
    text = LOSER_FONT.render(loser_text, 1, WHITE)
    score_text = SCORE_FONT.render(f"Your final score: {score}", 1, WHITE)
    WINDOW.blit(text, (SCREEN_WIDTH/2 - text.get_width()/2, SCREEN_HEIGHT/2 - text.get_height()))
    WINDOW.blit(score_text, (SCREEN_WIDTH/2 - score_text.get_width()/2, SCREEN_HEIGHT/2))

    final_high_score = highest_score(score)
    highest_score_text = HIGHEST_SCORE_FONT.render(f"Highest Score: {final_high_score}", 1, WHITE)
    WINDOW.blit(highest_score_text,
                (SCREEN_WIDTH/2 - highest_score_text.get_width()/2, SCREEN_HEIGHT/2 + score_text.get_height()))

    pygame.display.update()
    pygame.time.delay(2000)


def game():
    pygame.mixer.pause()
    BACKGROUND_TRACK.play()

    player = pygame.Rect(SCREEN_WIDTH/2 - PLAYER.get_width()/2, SCREEN_HEIGHT - 100,
                         PLAYER.get_width(), PLAYER.get_height())
    enemies = []

    player_bullets = []

    score = 0

    clock = pygame.time.Clock()
    game_on = True
    while game_on:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_on = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and len(player_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(player.x + player.width//2 - BULLET.get_width()//2, player.y,
                                         BULLET.get_width(), BULLET.get_height())
                    player_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

            if len(enemies) < MAX_ENEMIES:
                produce_enemies(enemies)

            if event.type == PLAYER_HIT:
                loser_text = "You Lose!"
                DESTRUCTION_SOUND.play()
                game_over(loser_text, score)
                game()
            if event.type == ENEMY_HIT:
                score += 1
                # OPTIONAL:
                # DESTRUCTION_SOUND.play()

        key_pressed = pygame.key.get_pressed()
        handle_player_movement(key_pressed, player)
        handle_bullets(player_bullets, enemies)
        handle_enemies(player, enemies)

        draw_window(player, player_bullets, enemies, score)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    game()
