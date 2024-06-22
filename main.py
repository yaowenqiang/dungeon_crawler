import pygame
import constants
from character import Character

pygame.init()

screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
pygame.display.set_caption("Dungeon Crawler!")

clock = pygame.time.Clock()
run = True

moving_left = False
moving_right = False
moving_up = False
moving_down = False

player = Character(100, 100)

while run:
    clock.tick(constants.FPS)
    screen.fill(constants.BG)
    dx = 0  # delta x
    dy = 0

    if moving_right:
        dx = constants.SPEED

    if moving_left:
        dx = -constants.SPEED

    if moving_up:
        dy = -constants.SPEED

    if moving_down:
        dy = constants.SPEED

    player.move(dx, dy)

    # draw player
    player.draw(screen)
    # event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            break

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                moving_left = True
            if event.key == pygame.K_d:
                moving_right = True
            if event.key == pygame.K_w:
                moving_up = True
            if event.key == pygame.K_s:
                moving_down = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                moving_left = False
            if event.key == pygame.K_d:
                moving_right = False
            if event.key == pygame.K_w:
                moving_up = False
            if event.key == pygame.K_s:
                moving_down = False


    pygame.display.update()

pygame.quit()
