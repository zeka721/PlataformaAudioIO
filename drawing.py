import pygame
from config import *
from estado import notas

def dibujar_pentagramas(screen):
    offset_y = 80
    for i in range(5):
        y = offset_y + 6 * espaciado_linea // 2 + i * espaciado_linea
        pygame.draw.line(screen, NEGRO, (50, y), (1300, y), 2)

def cargar_y_escalar_imagen(path, size=(32, 32), eliminar_blanco=True):
    img = pygame.image.load(path).convert_alpha()
    img = pygame.transform.smoothscale(img, size)
    return img

def dibujar_notas(screen, imagenes_figuras):
    for x, y, freq, dur, fig, acc, bloque in notas:
        clave = None

        # Detectar qué clave corresponde a esta figura
        for k, v in figuras.items():
            if fig == v:
                clave = k
                break

        img = imagenes_figuras.get(clave)
        if img:
            rect = img.get_rect(center=(x, y))
            screen.blit(img, rect)
        else:
            pygame.draw.circle(screen, ROJO, (x, y), radio_nota)

        # Mostrar alteración textual
        if freq != 0:
            alteracion = "#" if acc == 1 else "b" if acc == -1 else ""
            if alteracion:
                screen.blit(fuente.render(alteracion, True, AZUL), (x - 5, y - 30))




def dibujar_linea_tiempo(screen, x_pos):
    pygame.draw.line(screen, AZUL, (x_pos, 70), (x_pos, 240), 2)
