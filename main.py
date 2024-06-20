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

dx = 0  # delta x
dy = 0

if moving_right:
    dx = 5

if moving_left:
    dx = -5

if moving_up:
    dy = -5

if moving_down:
    dy = 5

while run:
    clock.tick(constants.FPS)
    screen.fill(constants.BG)
    # draw player
    player.draw(screen)
    # event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            break

    keys = pygame.key.get_pressed()
    if keys is not False:
        print(keys)
    if keys[pygame.K_a]:
        moving_left = True
    if keys[pygame.K_d]:
        moving_right = True
    if keys[pygame.K_w]:
        moving_up = True
    if keys[pygame.K_s]:
        moving_down = True
    player.move(dx, dy)


    pygame.display.update()

pygame.quit()
