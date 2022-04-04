import time

import pygame

from config import *
from objects import *
from menu import Menu
from sounds import SoundManager


class Game(Menu):
    def __init__(self):
        super().__init__('Game')
        self.player = Player()
        self.enemy = Enemy()
        self.blocks = [
            # Block(i * 100, 50) for i in range(8)
        ]
        self.block_timer = time.time()
        self.ball = Ball()
        self.initialized = False
        self.game_over = False
        self.started = False

    def update(self, events):
        for e in events:
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_RETURN or e.key == pygame.K_KP_ENTER:
                    self.started = True
                    SoundManager.play('ball')
        if not self.initialized:
            rows = len(self.blocks) // 8
            if rows < 6:
                if time.time() - self.block_timer > 0.05:
                    self.block_timer = time.time()
                    if rows <= 4:
                        self.blocks.extend([Block(i * 100, rows * 50 + 50) for i in range(8)])
                    else:
                        self.blocks.extend([Block(i * 100, rows * 50 + 50) for i in range(8)])
            else:
                self.initialized = True
                # for i in [0, 7, 14, 21, 28, 35]:
                #     self.blocks.pop(i)
                # self.blocks = self.blocks[:1]
        else:
            if len([i for i in self.blocks if i.active]) <= 0:
                self.game_over = True
        if self.started:
            self.player.update(events)
            self.enemy.update(events)
            self.enemy.use_ai(self.ball)
            self.ball.update(events)
            self.ball.collide(self.player, self.enemy, self.blocks)
        for i in self.blocks:
            i.update(events)
        if self.ball.lives <= 0:
            return False
        if self.game_over:
            return True

    def draw(self, surf: pygame.Surface):
        for i in self.blocks:
            i.draw(surf)
        self.player.draw(surf)
        self.enemy.draw(surf)
        self.ball.draw(surf)
        if not self.started:
            t = text('Press    Enter    to    Start')
            surf.blit(t, t.get_rect(center=(screen_width // 2, screen_height // 2)))
        t = text(f'Lives   {self.ball.lives}')
        surf.blit(t, (0, 0))
