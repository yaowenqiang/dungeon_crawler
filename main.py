import pygame
from pygame import mixer
import csv
import constants
from character import Character
from weapon import Weapon
from items import Item
from world import World
from button import Button

mixer.init()
pygame.init()

screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
pygame.display.set_caption("Dungeon Crawler!")

clock = pygame.time.Clock()

# define game variables
level = 2
start_game = False
pause_game = False
start_intro = False
run = True
screen_scroll = [0, 0]

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


# load music and sounds

pygame.mixer.music.load("assets/audio/music.wav")
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(-1, 0.0, 5000)

shoot_fx = pygame.mixer.Sound('assets/audio/arrow_shot.mp3')
shoot_fx.set_volume(0.5)

hit_fx = pygame.mixer.Sound('assets/audio/arrow_hit.wav')
hit_fx.set_volume(0.5)

coin_fx = pygame.mixer.Sound('assets/audio/coin.wav')
coin_fx.set_volume(0.5)

heal_fx = pygame.mixer.Sound('assets/audio/heal.wav')
heal_fx.set_volume(0.5)

# load weapon images
bow_image = scale_image(pygame.image.load("assets/images/weapons/bow.png").convert_alpha(), constants.WEAPON_SCALE)
arrow_image = scale_image(pygame.image.load("assets/images/weapons/arrow.png").convert_alpha(), constants.WEAPON_SCALE)
fireball_image = scale_image(pygame.image.load("assets/images/weapons/fireball.png").convert_alpha(),
                             constants.FIREBALL_SCALE)
heart_empty_image = scale_image(pygame.image.load("assets/images/items/heart_empty.png").convert_alpha(),
                                constants.ITEM_SCALE)
heart_half_image = scale_image(pygame.image.load("assets/images/items/heart_half.png").convert_alpha(),
                               constants.ITEM_SCALE)
heart_full_image = scale_image(pygame.image.load("assets/images/items/heart_full.png").convert_alpha(),
                               constants.ITEM_SCALE)

start_image = scale_image(pygame.image.load("assets/images/buttons/button_start.png").convert_alpha(),
                          constants.BUTTON_SCALE)
exit_image = scale_image(pygame.image.load("assets/images/buttons/button_exit.png").convert_alpha(),
                         constants.BUTTON_SCALE)
restart_image = scale_image(pygame.image.load("assets/images/buttons/button_restart.png").convert_alpha(),
                            constants.BUTTON_SCALE)
resume_image = scale_image(pygame.image.load("assets/images/buttons/button_resume.png").convert_alpha(),
                           constants.BUTTON_SCALE)

tile_list = []
for x in range(constants.TILE_TYPES):
    tile_image = pygame.image.load(f"assets/images/tiles/{x}.png").convert_alpha();
    tile_image = pygame.transform.scale(tile_image, (constants.TILE_SIZE, constants.TILE_SIZE))
    tile_list.append(tile_image)

# load coin images
coin_images = []
for x in range(4):
    image = scale_image(pygame.image.load(f"assets/images/items/coin_f{x}.png").convert_alpha(),
                        constants.ITEM_SCALE)
    coin_images.append(image)

red_potion = scale_image(pygame.image.load(f"assets/images/items/potion_red.png").convert_alpha(),
                         constants.POTION_SCALE)

item_images = [coin_images, red_potion]

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
        self.rect.x += screen_scroll[0]
        self.rect.y += screen_scroll[1]
        # move damage text up
        self.rect.y -= 1
        self.counter += 1
        if self.counter >= 30:
            self.kill()


class ScreenFade:
    def __init__(self, direction, color, speed):
        self.direction = direction
        self.color = color
        self.speed = speed
        self.fade_counter = 0

    def fade(self):
        fade_complete = False
        self.fade_counter += self.speed
        if self.direction == 1:
            pygame.draw.rect(screen, self.color,
                             (0 - self.fade_counter, 0, constants.SCREEN_WIDTH // 2, constants.SCREEN_HEIGHT))
            pygame.draw.rect(screen, self.color, (
                constants.SCREEN_WIDTH // 2 + self.fade_counter, 0, constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
            pygame.draw.rect(screen, self.color,
                             (0, 0 - self.fade_counter, constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT // 2))
            pygame.draw.rect(screen, self.color, (
                0, constants.SCREEN_HEIGHT // 2 + self.fade_counter, constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
        elif self.direction == 2:
            pygame.draw.rect(screen, self.color,
                             (0, 0, constants.SCREEN_WIDTH, 0 + self.fade_counter))
        if self.fade_counter >= constants.SCREEN_HEIGHT:
            fade_complete = True

        return fade_complete


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

    # level
    draw_text(f'L: {level}', font, constants.WHITE, constants.SCREEN_WIDTH - 300,
              (50 - font.get_height()) / 2)
    # show score
    draw_text(f'X: {player.score} ', font, constants.WHITE, constants.SCREEN_WIDTH - 150,
              (50 - font.get_height()) / 2)

    draw_text(f'H: {player.health} ', font, constants.WHITE, constants.SCREEN_WIDTH - 450,
              (50 - font.get_height()) / 2)


intro_fade = ScreenFade(1, constants.BLACK, 4)
death_fade = ScreenFade(2, constants.PINK, 4)

world_data = []
for row in range(constants.ROWS):
    r = [-1] * constants.COLS
    world_data.append(r)

with open(f'levels/level{level}_data.csv', encoding='utf-8', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for x, row in enumerate(reader):
        for y, tile in enumerate(row):
            world_data[x][y] = int(tile)

world = World()
world.process_data(world_data, tile_list, item_images, mob_animations)


def draw_grid():
    for x in range(30):
        pygame.draw.line(screen, constants.WHITE, (x * constants.TILE_SIZE, 0),
                         (x * constants.TILE_SIZE, constants.SCREEN_HEIGHT))
        pygame.draw.line(screen, constants.WHITE, (0, x * constants.TILE_SIZE),
                         (constants.SCREEN_WIDTH, x * constants.TILE_SIZE))


def reset_level():
    damage_text_group.empty()
    arrow_group.empty()
    item_group.empty()
    fireball_group.empty()
    data = []
    for row in range(constants.ROWS):
        r = [-1] * constants.COLS
        data.append(r)

    return data


# player = Character(400, 300, 15, mob_animations, 0)
player = world.player

# enemy = Character(300, 300, 100, mob_animations, 1)

# create enemy
enemy_list = world.character_list

damage_text_group = pygame.sprite.Group()
#
# damage_text = DamageText(300, 400, '50', constants.RED)
# damage_text_group.add(damage_text)


# create sprite groups

arrow_group = pygame.sprite.Group()
item_group = pygame.sprite.Group()
fireball_group = pygame.sprite.Group()

# potion = Item(200, 200, 1, [red_potion])
# coin = Item(400, 400, 0, coin_images)
score_coin = Item(constants.SCREEN_WIDTH - 150, 23, 0, coin_images, True)
# item_group.add(potion)
# item_group.add(coin)
item_group.add(score_coin)

for item in world.item_list:
    item_group.add(item)

start_button = Button(constants.SCREEN_WIDTH // 2 - 145, constants.SCREEN_HEIGHT // 2 - 150, start_image)
exit_button = Button(constants.SCREEN_WIDTH // 2 - 110, constants.SCREEN_HEIGHT // 2 + 50, exit_image)
restart_button = Button(constants.SCREEN_WIDTH // 2 - 175, constants.SCREEN_HEIGHT // 2 - 50, restart_image)
resume_button = Button(constants.SCREEN_WIDTH // 2 - 175, constants.SCREEN_HEIGHT // 2 - 150, resume_image)

while run:
    clock.tick(constants.FPS)
    if not start_game:
        screen.fill(constants.MENU_BG)
        if start_button.draw(screen):
            start_game = True
            start_intro = True
        if exit_button.draw(screen):
            run = False
    else:
        if pause_game:
            screen.fill(constants.MENU_BG)
            if resume_button.draw(screen):
                pause_game = False
            if exit_button.draw(screen):
                run = False
        else:
            screen.fill(constants.BG)
            draw_grid()
            if player.alive:
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

                screen_scroll, level_complete = player.move(dx, dy, world.obstacle_tiles, world.exit_tile)

                # update all objects
                player.update()

                world.update(screen_scroll)
                for enemy in enemy_list:
                    fireball = enemy.ai(player, world.obstacle_tiles, screen_scroll, screen, fireball_image)
                    if fireball:
                        fireball_group.add(fireball)
                    if enemy.alive:
                        enemy.update()

                arrow = bow.update(player)
                if arrow:
                    arrow_group.add(arrow)
                    shoot_fx.play()

                for arrow in arrow_group:
                    damage, damage_pos = arrow.update(screen_scroll, world.obstacle_tiles, enemy_list)
                    if damage:
                        hit_fx.play()
                        damage_text = DamageText(damage_pos.centerx, damage_pos.y, str(damage), constants.RED)
                        damage_text_group.add(damage_text)

                for damage in damage_text_group:
                    damage.update()

                for fireball in fireball_group:
                    fireball.update(screen_scroll, player)

                damage_text_group.update()
                item_group.update(screen_scroll, player, coin_fx, heal_fx)

            world.draw(screen)

            # draw player
            player.draw(screen)
            bow.draw(screen)
            for arrow in arrow_group:
                arrow.draw(screen)

            for fireball in fireball_group:
                fireball.draw(screen)

            for enemy in enemy_list:
                enemy.draw(screen)

            damage_text_group.draw(screen)
            item_group.draw(screen)

            draw_info()
            score_coin.draw(screen)

            # check level complete

            if level_complete:
                start_intro = True
                level += 1
                world_data = reset_level()
                with open(f'levels/level{level}_data.csv', encoding='utf-8', newline='') as csvfile:
                    reader = csv.reader(csvfile, delimiter=',')
                    for x, row in enumerate(reader):
                        for y, tile in enumerate(row):
                            world_data[x][y] = int(tile)
                world = World()
                world.process_data(world_data, tile_list, item_images, mob_animations)
                temp_hp = player.health
                temp_score = player.score
                player = world.player
                player.health = temp_hp
                player.score = temp_score

                enemy_list = world.character_list
                score_coin = Item(constants.SCREEN_WIDTH - 150, 23, 0, coin_images, True)
                item_group.add(score_coin)
                for item in world.item_list:
                    item_group.add(item)

            if start_intro:
                if intro_fade.fade():
                    start_intro = False
                    intro_fade.fade_counter = 0

            if not player.alive:
                if death_fade.fade():
                    if restart_button.draw(screen):
                        death_fade.fade_counter = 0
                        start_intro = True
                        world_data = reset_level()
                        with open(f'levels/level{level}_data.csv', encoding='utf-8', newline='') as csvfile:
                            reader = csv.reader(csvfile, delimiter=',')
                            for x, row in enumerate(reader):
                                for y, tile in enumerate(row):
                                    world_data[x][y] = int(tile)
                        world = World()
                        world.process_data(world_data, tile_list, item_images, mob_animations)
                        temp_score = player.score
                        player = world.player
                        player.score = temp_score

                        enemy_list = world.character_list
                        score_coin = Item(constants.SCREEN_WIDTH - 150, 23, 0, coin_images, True)
                        item_group.add(score_coin)
                        for item in world.item_list:
                            item_group.add(item)

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
            if event.key == pygame.K_ESCAPE:
                pause_game = True

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
