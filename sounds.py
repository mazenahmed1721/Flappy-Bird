import array
import math
import random
import pygame
def _sweep(rate, start_freq, end_freq, duration, volume=0.3, square=True):
    count = int(rate * duration)
    samples = []
    phase = 0.0
    for i in range(count):
        t = i / count
        freq = start_freq + (end_freq - start_freq) * t
        phase += 2 * math.pi * freq / rate
        value = math.sin(phase)
        if square: 
            value = 1.0 if value >= 0 else -1.0
        samples.append(value * volume * (1.0 -t))
    return samples
def _noise(rate, duration, volume=0.4):
    count = int(rate * duration)
    return [
        random.uniform(-1.0, 1.0) * volume * (1.0 - i / count) ** 2
        for i in range(count)
    ]
def _to_sound(samples, channels):
    data = array.array("h")
    for sample in samples:
        value = int(max(-1.0, min(1.0, sample))* 32767)
        for _ in range(channels):
            data.append(value)
    return pygame.mixer.Sound(buffer=data.tobytes())
class Sounds:
    def __init__(self):
        self.muted = False
        self.effets = {}
        try: 
            if pygame.mixer.get_init() is None:
                pygame.mixer.init(22050, -16, 1, 512)
            rate, fmt, channels = pygame.mixer.get_init()
            if fmt != -16:
                return
            self.effets = {
                "flap": _to_sound(_sweep(rate, 420, 760, 0.09, 0.25), channels),
                "score": _to_sound(
                    _sweep(rate, 880, 880, 0.07, 0.25)
                    + _sweep(rate, 1320, 1320, 0.12, 0.25),
                    channels,
                ),
                "hit": _to_sound(
                    _noise(rate, 0.1, 0.45)
                    + _sweep(rate, 380, 90, 0.28, 0.35, square=False),
                    channels,
                ),
            }
        except pygame.error:
            self.effets = {}
    def play(self, name):
        if self.muted:
            return
        sound = self.effets.get(name)
        if sound:
            sound.play()
    def toggle(self):
        self.muted = not self.muted