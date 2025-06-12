import pygame
import numpy as np

def generar_tono(frecuencia, duracion_ms):
    rate = 44100
    n_samples = int(rate * duracion_ms / 1000)
    buffer = (np.sin(2 * np.pi * np.arange(n_samples) * frecuencia / rate) * 32767).astype(np.int16)
    return pygame.sndarray.make_sound(np.column_stack([buffer, buffer]))

def reproducir_nota(frecuencia, duracion):
    if frecuencia == 0:
        pygame.time.delay(duracion)
    else:
        sonido = generar_tono(frecuencia, duracion)
        sonido.play()
        pygame.time.delay(int(duracion * 1.05))
        sonido.stop()