import random
import time

from config import *
from utils import *
import pygame
from sounds import SoundManager


class BaseObject:
    def __init__(self, name: str, x=0, y=0):
        self.name = name
        self.x = x
        self.y = y

    def update(self, events: list[pygame.event.Event]):
        pass

    def draw(self, surf: pygame.Surface):
        pass


class Player(BaseObject):
    def __init__(self, x=screen_width // 2 - 50, y=screen_height - 50):
        super().__init__('player', x, y)
        self.dimensions = [100, 25]
        self.dx = 0

    def get_rect(self):
        return pygame.Rect(self.x, self.y, *self.dimensions)

    def update(self, events: list[pygame.event.Event]):
        self.dx = 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.dx = -10
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.dx = 10
        self.x += self.dx
        w = self.dimensions[0]
        self.x = clamp(self.x, 0, screen_width - w)

    def draw(self, surf: pygame.Surface):
        pygame.draw.rect(surf, 'white', (self.x, self.y, *self.dimensions))


class Enemy(BaseObject):
    def __init__(self, x=screen_width // 2 - 50, y=screen_height - 500):
        super().__init__('enemy', x, y)
        self.dimensions = [100, 25]
        self.dx = 0

    def get_rect(self):
        return pygame.Rect(self.x, self.y, *self.dimensions)

    def update(self, events: list[pygame.event.Event]):
        pass

    def use_ai(self, ball: 'Ball'):
        if self.y + 150 > ball.y > self.y:
            if not (self.x - 10 < ball.x < self.x + 10):
                self.x += 10 if ball.x > self.x else -10
        self.x = clamp(self.x, 0, screen_width - self.dimensions[0])

    def draw(self, surf: pygame.Surface):
        pygame.draw.rect(surf, 'white', (self.x, self.y, *self.dimensions))


class Block(BaseObject):
    def __init__(self, x=screen_width // 2, y=50):
        super().__init__('block', x, y)
        self.dimensions = [100, 50]
        self.start_dimensions = [50, 25]
        self.active = True

    def get_rect(self):
        if self.start_dimensions != self.dimensions:
            w, h = self.start_dimensions
            w1, h1 = self.dimensions
            return pygame.Rect(self.x + (w1 - w) // 2, self.y + (h1 - h) // 2, w, h)
        else:
            return pygame.Rect(self.x, self.y, *self.dimensions)

    def update(self, events: list[pygame.event.Event]):
        if self.start_dimensions != self.dimensions:
            self.start_dimensions[0] += 4
            self.start_dimensions[1] += 2
            if self.start_dimensions[0] > 100:
                self.start_dimensions[0] = 100
            if self.start_dimensions[1] > 50:
                self.start_dimensions[1] = 50

    def draw(self, surf: pygame.Surface):
        c = ['white', 'black']
        if not self.active:
            c = ['black', 'white']
        pygame.draw.rect(surf, c[0], self.get_rect())
        pygame.draw.rect(surf, c[1], self.get_rect(), 3)


class Ball(BaseObject):
    def __init__(self):
        super().__init__('ball', screen_width // 2, screen_height - 350)
        self.r = 10
        self.dx = 0
        self.dy = 0
        self.x -= self.r
        self.y -= self.r
        self.angle = 90 + random.randint(5, 10) * random.choice([-1, 1])
        self.speed = 10
        self.launched = False
        self.lives = 10

    def collide(self, player: Player, enemy: Enemy, blocks: list[Block]):
        angle = math.radians(self.angle)
        self.dx = math.cos(angle)
        self.dy = math.sin(angle)
        self.x += self.dx * self.speed
        # if player_rect.colliderect(self_rect):
        #     self.dx = 0
        #     self.dy = 0
        #     if self_rect.x < player_rect.x:
        #         self.x = player_rect.x - self_rect.w
        #     else:
        #         self.x = player_rect.x + player_rect.w
        self.y += self.dy * self.speed
        player_rect = player.get_rect()
        self_rect = self.get_rect()
        enemy_rect = enemy.get_rect()
        # enemy_rect = pygame.Rect(-100, -100, 10, 10)
        if player_rect.colliderect(self_rect):
            SoundManager.play('hit1')
            self.angle += random.randint(0, 2) * random.choice([-1, 1])
            # check if it is left-right or top-bottom collision
            if player_rect.x <= self.x + self_rect.w // 2 <= player_rect.x + player_rect.w:  # top-bottom
                if 0 <= self.angle <= 180:
                    self.y = player_rect.y - self_rect.h
                elif 180 <= self.angle <= 360:
                    self.y = player_rect.y + player_rect.h
                self.angle = 360 - self.angle
            else:
                self.angle = 180 - self.angle
            self.angle += player.dx
            # if self_rect.y + self_rect.h > player_rect.y + player_rect.h:
            #     self.y = player_rect.y + player_rect.h
            # elif self_rect.y + self_rect.h > player_rect.y:
            #     self.y = player_rect.y - self_rect.h
            # self.angle -= 180 + player.dx * 10
            # self.angle += 180 if self.angle <= 90 else -180
            # self.angle = 360 - self.angle
        elif enemy_rect.colliderect(self_rect):
            SoundManager.play('hit1')
            self.angle += random.randint(0, 2) * random.choice([-1, 1])
            if enemy_rect.x <= self.x + self_rect.w // 2 <= enemy_rect.x + enemy_rect.w:  # top-bottom
                if 0 <= self.angle <= 180:
                    self.y = enemy_rect.y - self_rect.h
                elif 180 <= self.angle <= 360:
                    self.y = enemy_rect.y + enemy_rect.h
                self.angle = 360 - self.angle
            else:
                self.angle = 180 - self.angle
            # if self_rect.y < enemy_rect.y:
            #     self.y = enemy_rect.y - self_rect.h
            # elif self_rect.y < enemy_rect.y + enemy_rect.h:
            #     self.y = enemy_rect.y + enemy_rect.h
            # self.angle = 360 - self.angle
        else:
            if self_rect.y < 0:
                SoundManager.play('hit3')
                self.angle += random.randint(0, 2) * random.choice([-1, 1])
                self.y = 0
                self.angle = 360 - self.angle
            elif self_rect.x < 0 or self_rect.x > screen_width - self_rect.w:
                SoundManager.play('hit3')
                self.angle += random.randint(0, 2) * random.choice([-1, 1])
                self.x = clamp(self.x, 0, screen_width - self_rect.w)
                self.angle = 180 - self.angle
            else:
                for i in blocks:
                    if i.active:
                        rect = i.get_rect()
                        if rect.colliderect(self_rect):
                            SoundManager.play('hit2')
                            self.angle += random.randint(0, 2) * random.choice([-1, 1])
                            i.active = False
                            # check if it is left-right or top-bottom collision
                            if rect.x <= self.x + self_rect.w // 2 <= rect.x + rect.w:  # top-bottom
                                if 0 <= self.angle <= 180:
                                    self.y = rect.y - self_rect.h
                                elif 180 <= self.angle <= 360:
                                    self.y = rect.y + rect.h
                                self.angle = 360 - self.angle
                            else:
                                self.angle = 180 - self.angle
        self.angle %= 360
        if self.y > screen_height + 100:
            self.lives -= 1
            self.y = screen_height - 350
            self.x = player.x + player_rect.w // 2
            self.angle = 90 + random.choice([-1, 1]) * random.randint(0, 30)
            SoundManager.play('ball')

    def get_rect(self):
        return pygame.Rect(self.x, self.y, 2 * self.r, 2 * self.r)

    def update(self, events: list[pygame.event.Event]):
        pass

    def draw(self, surf: pygame.Surface):
        # pygame.draw.rect(surf, 'white', self.get_rect(), 2)
        pygame.draw.circle(surf, 'red', (self.x + self.r, self.y + self.r), self.r)
