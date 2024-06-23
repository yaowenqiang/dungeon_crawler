import math

import pygame
import constants


class Character:
    def __init__(self, x, y, health, mob_animations, char_type, boss, size):
        self.char_type = char_type
        self.score = 0
        self.flip = False
        self.rect = pygame.Rect(0, 0, constants.TILE_SIZE * size, constants.TILE_SIZE * size)
        self.rect.center = (x, y)
        self.frame_index = 0
        self.action = 0  # 0 is idle, 1 is running
        self.update_time = pygame.time.get_ticks()
        self.animation_list = mob_animations[char_type]
        self.running = False
        self.boss = boss

        self.image = self.animation_list[self.action][self.frame_index]
        self.health = health
        self.alive = True

    def move(self, dx, dy, obstacle_tiles):
        screen_scroll = [0, 0]
        # control diagonal speed
        self.running = False
        if dx != 0 or dy != 0:
            self.running = True

        if dx < 0:
            self.flip = True
        else:
            self.flip = False

        if dx != 0 and dy != 0:
            # 计划物体对角线方向移动时对应的顶点坐标，等于速度 * √2/2
            # 就是计算正方形的对角线的长度,
            dx = dx * (math.sqrt(2) / 2)
            dy = dy * (math.sqrt(2) / 2)

        # check for collision with map in a directio
        self.rect.x += dx
        for obstacle in obstacle_tiles:
            if obstacle[1].colliderect(self.rect):
                if dx > 0:
                    self.rect.right = obstacle[1].left
                if dx < 0:
                    self.rect.left = obstacle[1].right
        self.rect.y += dy
        for obstacle in obstacle_tiles:
            if obstacle[1].colliderect(self.rect):
                if dy > 0:
                    self.rect.bottom = obstacle[1].top
                if dy < 0:
                    self.rect.top = obstacle[1].bottom

        if self.char_type == 0:
            if self.rect.right > (constants.SCREEN_WIDTH - constants.SCROLL_THRESH):
                screen_scroll[0] = constants.SCREEN_WIDTH - constants.SCROLL_THRESH - self.rect.right
                self.rect.right = constants.SCREEN_WIDTH - constants.SCROLL_THRESH
            if self.rect.left < constants.SCROLL_THRESH:
                screen_scroll[0] = constants.SCROLL_THRESH - self.rect.left
                self.rect.left = constants.SCROLL_THRESH

        if self.rect.bottom > (constants.SCREEN_HEIGHT - constants.SCROLL_THRESH):
            screen_scroll[1] = constants.SCREEN_HEIGHT - constants.SCROLL_THRESH - self.rect.bottom
            self.rect.bottom = constants.SCREEN_HEIGHT - constants.SCROLL_THRESH
        if self.rect.top < constants.SCROLL_THRESH:
            screen_scroll[1] = constants.SCROLL_THRESH - self.rect.top
            self.rect.top = constants.SCROLL_THRESH
        return screen_scroll

    def ai(self, screen_scroll):
        self.rect.x += screen_scroll[0]
        self.rect.y += screen_scroll[1]

    def update_action(self, new_action):
        if new_action != self.action:
            self.action = new_action
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def update(self):
        if self.health <= 0:
            self.health = 0
            self.alive = False

        if self.running:
            self.update_action(1)
        else:
            self.update_action(0)

        animation_cooldown = 70
        # handle animation
        self.image = self.animation_list[self.action][self.frame_index]
        # check if enough time has passed since the last update
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()
        if self.frame_index >= len(self.animation_list[self.action]):
            self.frame_index = 0
        # update image

    def draw(self, surface):
        flipped_image = pygame.transform.flip(self.image, self.flip, False)
        if self.char_type == 0:
            surface.blit(flipped_image, (self.rect.x, self.rect.y - constants.SCALE * constants.OFFSET))
        else:
            surface.blit(flipped_image, self.rect)
        pygame.draw.rect(surface, constants.RED, self.rect, 1)
