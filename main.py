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


def scale_image(image, scale):
    w = image.get_width() * scale
    h = image.get_height() * scale
    return pygame.transform.scale(image, (w, h))


animation_types = ['idle', 'run']

animation_list = []
for animation in animation_types:
    tmp_list = []
    for i in range(4):
        img = pygame.image.load(f'assets/images/characters/elf/{animation}/{i}.png').convert_alpha()
        img = scale_image(img, constants.SCALE)
        tmp_list.append(img)
    animation_list.append(tmp_list)

player = Character(100, 100, animation_list)

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

    # update player
    player.update()

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
