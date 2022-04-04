import os.path

import pygame
from config import *


class SoundManager:
    config = {
        'select': 'select.wav',
        'menu': 'menu.wav',
        'hit1': 'hit1.wav',
        'hit2': 'hit2.wav',
        'hit3': 'hit3.wav',
        'game_over': 'game_over.wav',
        'win': 'win.wav',
        'ball': 'ball.wav',
    }
    current = ''
    for i in config.keys():
        config[i] = os.path.join(ASSETS, config[i])
    # def __init__(self):
    #     self.config = {
    #         'select': 'select.wav',
    #     }
    #     self.current = ''

    @classmethod
    def play(cls, sound):
        for i in range(2):
            if not pygame.mixer.Channel(i).get_busy():
                cls.current = sound
                pygame.mixer.Channel(i).play(pygame.mixer.Sound(cls.config[sound]))
                return
        if sound == cls.current and pygame.mixer.music.get_busy():
            return
        cls.current = sound
        # pygame.mixer.music.play()
