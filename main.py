# This is a sample Python script.
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import os

import pygame

pygame.font.init()
pygame.mixer.init()

WELCOME_TEXT = "Learning / Showcase Purpose - Vipul Tawde."

WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Demo Game")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

FPS = 60
BORDER = pygame.Rect(WIDTH / 2 - 5, 0, 10, HEIGHT)

SS_SIZE = (50, 30)
BULLET_VEL = 10
VEL = 5

YLW_SS_IMG = pygame.image.load(os.path.join('Assets', 'spaceship_yellow.png'))
YLW_SS_POS = (50, 50)
YLW_SS = pygame.transform.rotate(pygame.transform.scale(YLW_SS_IMG, SS_SIZE), 90)

RED_SS_IMG = pygame.image.load(os.path.join('Assets', 'spaceship_red.png'))
RED_SS_POS = (450, 50)
RED_SS = pygame.transform.rotate(pygame.transform.scale(RED_SS_IMG, SS_SIZE), -90)

SPACE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'space.png')), (WIDTH, HEIGHT))

BULLET_WIDTH = 4
BULLET_HEIGHT = 2
MAX_BULLETS = 3

YLW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)
WELCOME_FONT = pygame.font.SysFont('comicsans', 40)

BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Gun+Silencer.mp3'))
BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Grenade+1.mp3'))


def init_ss():
    WIN.blit(YLW_SS, YLW_SS_POS)
    WIN.blit(RED_SS, RED_SS_POS)
    pygame.display.update()


def ylw_movement(ylw_p, keys_pressed):
    # WASD - Up, Left, Down, Right
    if keys_pressed[pygame.K_a] and ylw_p.x - VEL > 0:
        ylw_p.x -= VEL
    if keys_pressed[pygame.K_d] and ylw_p.x + VEL < BORDER.x - ylw_p.width:
        ylw_p.x += VEL
    if keys_pressed[pygame.K_w] and ylw_p.y - VEL > 0:
        ylw_p.y -= VEL
    if keys_pressed[pygame.K_s] and ylw_p.y + VEL < HEIGHT - ylw_p.height:
        ylw_p.y += VEL


def red_movement(red_p, keys_pressed):
    # WASD - Up, Left, Down, Right
    if keys_pressed[pygame.K_LEFT] and red_p.x - VEL > BORDER.x + BORDER.width:
        red_p.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and red_p.x + VEL < WIDTH - red_p.width:
        red_p.x += VEL
    if keys_pressed[pygame.K_UP] and red_p.y - VEL > 0:
        red_p.y -= VEL
    if keys_pressed[pygame.K_DOWN] and red_p.y + VEL < HEIGHT - red_p.height:
        red_p.y += VEL


def handle_bullets(ylw_bullets, red_bullets, ylw_p, red_p):
    for bullet in ylw_bullets:
        bullet.x += BULLET_VEL
        if red_p.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            ylw_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            ylw_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.x -= BULLET_VEL
        if ylw_p.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YLW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)


def draw_winner(text):
    winner_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(winner_text, (WIDTH / 2 - winner_text.get_width() / 2, HEIGHT / 2 - winner_text.get_height() / 2))
    pygame.display.update()
    pygame.time.delay(5000)


def draw_welcome_page(text):
    welcome_text = WELCOME_FONT.render(text, 1, YELLOW)
    WIN.blit(welcome_text, (WIDTH / 2 - welcome_text.get_width() / 2, HEIGHT / 2 - welcome_text.get_height() / 2))
    pygame.display.update()
    pygame.time.delay(5000)


def draw_window(red_p, ylw_p, red_bullets, ylw_bullets, red_health, ylw_health):
    # WIN.fill(WHITE)  # Clears previous images
    WIN.blit(SPACE, (0, 0))
    pygame.draw.rect(WIN, BLACK, BORDER)
    red_health_text = HEALTH_FONT.render("HEALTH: " + str(red_health), 1, WHITE)
    ylw_health_text = HEALTH_FONT.render("HEALTH: " + str(ylw_health), 1, WHITE)
    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
    WIN.blit(ylw_health_text, (10, 10))

    # Comment Me
    # pygame.draw.rect(WIN, RED, ylw_p)
    # pygame.draw.rect(WIN, YELLOW, red_p)

    WIN.blit(YLW_SS, ylw_p)
    WIN.blit(RED_SS, red_p)


    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)
    for bullet in ylw_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)
    pygame.display.update()


def main():
    # init_bg()
    draw_welcome_page(WELCOME_TEXT)
    init_ss()
    red_p = pygame.Rect(RED_SS_POS, (SS_SIZE[1], SS_SIZE[0]))
    ylw_p = pygame.Rect(YLW_SS_POS, (SS_SIZE[1], SS_SIZE[0]))
    clock = pygame.time.Clock()

    red_bullets = []
    ylw_bullets = []

    ylw_health = 10
    red_health = 10

    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_b and len(ylw_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(
                        ylw_p.x + ylw_p.width, ylw_p.y + ylw_p.height / 2 - BULLET_HEIGHT / 2,
                        BULLET_WIDTH, BULLET_HEIGHT
                    )
                    ylw_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

                if event.key == pygame.K_KP0 and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(
                        red_p.x - BULLET_WIDTH, red_p.y + red_p.height / 2 - BULLET_HEIGHT / 2,
                        BULLET_WIDTH, BULLET_HEIGHT
                    )
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

            if event.type == YLW_HIT:
                ylw_health -= 1
                BULLET_HIT_SOUND.play()

            if event.type == RED_HIT:
                red_health -= 1
                BULLET_HIT_SOUND.play()

        winner_text = ""
        if red_health <= 0:
            winner_text = "Yellow Wins"
        if ylw_health <= 0:
            winner_text = "Red Wins"
        if winner_text != "":
            draw_winner(winner_text)
            break

        keys_pressed = pygame.key.get_pressed()
        ylw_movement(ylw_p, keys_pressed)
        red_movement(red_p, keys_pressed)
        handle_bullets(ylw_bullets, red_bullets, ylw_p, red_p)

        draw_window(red_p, ylw_p, red_bullets, ylw_bullets, red_health, ylw_health)

    main()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
