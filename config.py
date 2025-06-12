import pygame

# Inicialización de pygame para fuentes
pygame.font.init()

BLANCO, NEGRO, ROJO, AZUL, GRIS, VERDE = (255, 255, 255), (0, 0, 0), (220, 30, 30), (0, 0, 200), (150, 150, 150), (0, 200, 0)
fuente = pygame.font.SysFont(None, 22)

espaciado_linea = 20
radio_nota = 8

notas_frecuencias = {
    0: ("A6", 1760), 1: ("G6", 1568), 2: ("F6", 1397), 3: ("E6", 1319),
    4: ("D6", 1175), 5: ("C6", 1047), 6: ("B5", 988), 7: ("A5", 880),
    8: ("G5", 784), 9: ("F5", 698), 10: ("E5", 659), 11: ("D5", 587),
    12: ("C5", 523), 13: ("B4", 494), 14: ("A4", 440), 15: ("G4", 392),
    16: ("F4", 349), 17: ("E4", 330), 18: ("D4", 294), 19: ("C4", 262)
}

figuras = {
    '1': ("Semicorchea", 100), '2': ("Corchea", 200),
    '3': ("Negra", 400), '4': ("Blanca", 800),
    '5': ("Redonda", 1600), '0': ("Pausa", 400)
}