import pygame
from utils import *
from sounds import SoundManager


class Menu:
    def __init__(self, name='menu', options=('OK', 'OK')):
        self.name = name
        self.options = options
        self.c = 0

    def update(self, events: list[pygame.event.Event]):
        for e in events:
            if e.type == pygame.KEYDOWN:
                if e.key in (pygame.K_UP, pygame.K_DOWN):
                    SoundManager.play('menu')
                if e.key == pygame.K_UP:
                    self.c -= 1
                if e.key == pygame.K_DOWN:
                    self.c += 1
                if e.key == pygame.K_RETURN or e.key == pygame.K_KP_ENTER:
                    SoundManager.play('select')
                    return self.options[self.c]
        if len(self.options) > 0:
            self.c %= len(self.options)

    def draw(self, surf: pygame.Surface):
        t = text(self.name, 100)
        surf.blit(t, t.get_rect(center=(screen_width // 2, 100)))

        for i in range(len(self.options)):
            color = 'green' if i == self.c else 'white'
            t = text(self.options[i], 75, color)
            surf.blit(t, t.get_rect(center=(screen_width // 2, 450 + i * 100)))

        if len(self.options) > 0:
            t = text('Use  Arrow  Keys  to  change  options', 30)
            surf.blit(t, t.get_rect(center=(screen_width // 2, screen_height - 100)))
            t = text('and  Enter  to  Select', 30)
            surf.blit(t, t.get_rect(center=(screen_width // 2, screen_height - 50 - 15)))


class GameWonMenu(Menu):
    def __init__(self):
        super().__init__('GAME WON!', options=['Home', 'Quit'])

    def draw(self, surf: pygame.Surface):
        super().draw(surf)
        t = text('Congratulations!', 50)
        surf.blit(t, t.get_rect(center=(screen_width // 2, 250)))
        t = text('You  Won  The  Game!', 50)
        surf.blit(t, t.get_rect(center=(screen_width // 2, 300)))


class GameLostMenu(Menu):
    def __init__(self):
        super().__init__('GAME OVER!', options=['Retry', 'Home', 'Quit'])


class Home(Menu):
    def __init__(self):
        super().__init__('BreakPong!', options=['Play', 'Help', 'Quit'])


class Guide(Menu):
    def __init__(self):
        super().__init__('GUIDE', options=())
        self.phases = ['controls', 'lights', 'ball', 'twist', 'tips']
        self.phase = 0
        self.msg = {
            'controls': [
                '', '',
                'Move   your   paddle   using',
                'Left and Right arrows',
                'or', 'using  A  and  D',
            ],
            'lights': [
                '',
                'There will  be  a  group of white',
                'Lights  on  the screen',
                'You   need  to  destroy all',
                'Lights  And  make it dark'
            ],
            'ball': [
                'To   do   so   you   will   get',
                'A   Red   Ball',
                'which  can  bounce',
                'off  surfaces',
                'Use  it  to  destroy  all',
                'the  Lights'
            ],
            'twist': [
                'But Wait',
                'You   are   your   own   enemy!',
                'Your  Clone  will  try  to  block',
                'the ball from  going  up',
                'Play against yourself and',
                'destroy all lights to Win!'
            ],
            'tips': [
                '',
                'You  may  speed  up  the  paddles',
                'and hit  the ball  while moving',
                'to  add  a  small  force',
                'to  the  ball  to  change',
                'its  direction'
            ]
        }
        self.player = pygame.Rect(screen_width // 2 - 50, 700, 100, 25)
        self.player_k = 1
        self.enemy = pygame.Rect(screen_width // 2 - 50, 600, 100, 25)
        self.enemy_k = -1

    def update(self, events: list[pygame.event.Event]):
        for e in events:
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_RETURN or e.key == pygame.K_KP_ENTER:
                    self.phase += 1
                    if self.phase >= len(self.phases):
                        self.phase = len(self.phases) - 1
                        SoundManager.play('select')
                        return True
                    else:
                        SoundManager.play('menu')

    def draw(self, surf: pygame.Surface):
        super().draw(surf)
        t = text(self.phases[self.phase].upper(), 75, 'white')
        surf.blit(t, t.get_rect(center=(screen_width // 2, 225)))
        for i in range(len(self.msg[self.phases[self.phase]])):
            t = text(self.msg[self.phases[self.phase]][i], 50, 'white')
            surf.blit(t, t.get_rect(center=(screen_width // 2, 300 + i * 50)))
        self.player.x += self.player_k * 2
        self.enemy.x += self.enemy_k * 2
        if self.player.x < 300 or self.player.x + self.player.w > screen_width - 300:
            self.player_k *= -1
        if self.enemy.x < 300 or self.enemy.x + self.enemy.w > screen_width - 300:
            self.enemy_k *= -1
        if self.phase == 0:
            pygame.draw.rect(surf, 'white', self.player)
        elif self.phase == 1:
            pygame.draw.rect(surf, 'white', (250, 650, 100, 50))
            pygame.draw.rect(surf, 'black', (250, 650, 100, 50), 2)
            pygame.draw.rect(surf, 'black', (screen_width - 250 - 100, 650, 100, 50))
            pygame.draw.rect(surf, 'white', (screen_width - 250 - 100, 650, 100, 50), 2)
        elif self.phase == 2:
            pygame.draw.circle(surf, 'red', (screen_width // 2, 650), 10)
        elif self.phase == 3:
            pygame.draw.rect(surf, 'white', self.player)
            pygame.draw.rect(surf, 'white', self.enemy)
        t = text('Press   Enter   To   Proceed', 50, 'green')
        surf.blit(t, t.get_rect(center=(screen_width // 2, screen_height - 100)))
        t = text(f'Page {self.phase + 1} of {len(self.phases)}', 30, 'white')
        surf.blit(t, t.get_rect(center=(screen_width // 2, screen_height - 50)))
