import pygame
import constants
from character import Character
from weapon import Weapon
from items import Item

pygame.init()

screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
pygame.display.set_caption("Dungeon Crawler!")

clock = pygame.time.Clock()
run = True

moving_left = False
moving_right = False
moving_up = False
moving_down = False

# define font

font = pygame.font.Font("assets/fonts/AtariClassic.ttf", 20)


def scale_image(image, scale):
    w = image.get_width() * scale
    h = image.get_height() * scale
    return pygame.transform.scale(image, (w, h))


# load weapon images
bow_image = scale_image(pygame.image.load("assets/images/weapons/bow.png").convert_alpha(), constants.WEAPON_SCALE)
arrow_image = scale_image(pygame.image.load("assets/images/weapons/arrow.png").convert_alpha(), constants.WEAPON_SCALE)
heart_empty_image = scale_image(pygame.image.load("assets/images/items/heart_empty.png").convert_alpha(),
                                constants.ITEM_SCALE)
heart_half_image = scale_image(pygame.image.load("assets/images/items/heart_half.png").convert_alpha(),
                               constants.ITEM_SCALE)
heart_full_image = scale_image(pygame.image.load("assets/images/items/heart_full.png").convert_alpha(),
                               constants.ITEM_SCALE)

# load coin images
coin_images = []
for x in range(4):
    image = scale_image(pygame.image.load(f"assets/images/items/coin_f{x}.png").convert_alpha(),
                        constants.ITEM_SCALE)
    coin_images.append(image)

    red_potion = scale_image(pygame.image.load(f"assets/images/items/potion_red.png").convert_alpha(),
                             constants.POTION_SCALE)

bow = Weapon(bow_image, arrow_image)

mob_types = ['elf', 'imp', 'skeleton', 'goblin', 'muddy', 'tiny_zombie', 'big_demon']

animation_types = ['idle', 'run']

mob_animations = []
for mob in mob_types:
    animation_list = []
    for animation in animation_types:
        tmp_list = []
        for i in range(4):
            img = pygame.image.load(f'assets/images/characters/{mob}/{animation}/{i}.png').convert_alpha()
            img = scale_image(img, constants.SCALE)
            tmp_list.append(img)
        animation_list.append(tmp_list)
    mob_animations.append(animation_list)


# damage text class

class DamageText(pygame.sprite.Sprite):
    def __init__(self, x, y, damage, color):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.image = font.render(damage, True, color)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.counter = 0

    def update(self):
        # move damage text up
        self.rect.y -= 1
        self.counter += 1
        if self.counter >= 30:
            self.kill()


def draw_text(text, font, text_color, x, y):
    img = font.render(text, True, text_color)
    screen.blit(img, (x, y))


def draw_info():
    pygame.draw.rect(screen, constants.PANEL_COLOR, (0, 0, constants.SCREEN_WIDTH, 50))
    pygame.draw.line(screen, constants.WHITE, (0, 50), (constants.SCREEN_WIDTH, 50))
    have_heart_drawn = False
    for i in range(5):
        if player.health >= ((i + 1) * 20):
            screen.blit(heart_full_image, (i * 50 + 10, 0))
        elif (player.health % 20 > 0) and have_heart_drawn == False:
            screen.blit(heart_half_image, (i * 50 + 10, 0))
            have_heart_drawn = True
        else:
            screen.blit(heart_empty_image, (i * 50 + 10, 0))

    # show score
    draw_text(f'X: {player.score}', font, constants.WHITE, constants.SCREEN_WIDTH - 250,
              (50 - font.get_height()) / 2)


player = Character(100, 100, 15, mob_animations, 0)
enemy = Character(200, 200, 100, mob_animations, 1)

# create enemy
enemy_list = [enemy]

damage_text_group = pygame.sprite.Group()
#
# damage_text = DamageText(300, 400, '50', constants.RED)
# damage_text_group.add(damage_text)


# create sprite groups

arrow_group = pygame.sprite.Group()
item_group = pygame.sprite.Group()

potion = Item(200, 200, 1, [red_potion])
coin = Item(400, 400, 0, coin_images)
score_coin = Item(constants.SCREEN_WIDTH - 150, 23, 0, coin_images)

item_group.add(potion)
item_group.add(coin)
item_group.add(score_coin)

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

    for enemy in enemy_list:
        enemy.update()

    arrow = bow.update(player)
    if arrow:
        arrow_group.add(arrow)

    for arrow in arrow_group:
        damage, damage_pos = arrow.update(enemy_list)
        if damage:
            damage_text = DamageText(damage_pos.centerx, damage_pos.y, str(damage), constants.RED)
            damage_text_group.add(damage_text)

    # for damage in damage_text_group:
    #     damage.update()

    damage_text_group.update()
    item_group.update(player)

    # draw player
    player.draw(screen)
    bow.draw(screen)
    for arrow in arrow_group:
        arrow.draw(screen)

    for enemy in enemy_list:
        enemy.draw(screen)

    damage_text_group.draw(screen)
    item_group.draw(screen)

    draw_info()
    score_coin.draw(screen)

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
