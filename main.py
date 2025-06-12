import pygame
import sys
import os
from config import *
from estado import *
from drawing import dibujar_pentagramas, dibujar_notas, dibujar_linea_tiempo
from estado import nota_inicio
from estado import notas
from audio import reproducir_nota
from file_io import exportar_a_arduino, guardar_partitura, cargar_partitura
from drawing import cargar_y_escalar_imagen  # al inicio del main





pygame.init()
screen = pygame.display.set_mode((1350, 300))
pygame.display.set_caption("Editor Musical Arduino - Un Pentagrama")

# Cargar imágenes de figuras
imagenes_figuras = {}
ruta_imagenes = "C:/Users/Zeka/PycharmProjects/PlataformaMusicalZumbador/figuras_musicales"

figura_a_imagen = {
    '5': "Redonda.png",
    '4': "Blanca.png",
    '3': "Negra.png",
    '2': "Corchea.png",
    '1': "Semicorchea.png",
    '0': "Silencio.png"
}
for clave, nombre_archivo in figura_a_imagen.items():
    path = os.path.join(ruta_imagenes, nombre_archivo)
    if os.path.exists(path):
        imagen = cargar_y_escalar_imagen(path, size=(28, 28))
        imagenes_figuras[clave] = imagen

botones = {
    "Reproducir": pygame.Rect(50, 10, 100, 30),
    "Exportar": pygame.Rect(180, 10, 100, 30),
    "Guardar": pygame.Rect(440, 10, 100, 30),
    "Cargar": pygame.Rect(560, 10, 100, 30),
    "Salir": pygame.Rect(310, 10, 100, 30)
}

figura_botones = {}
for i, clave in enumerate(['1', '2', '3', '4', '5', '0']):
    figura_botones[clave] = pygame.Rect(750 + i * 60, 10, 55, 30)

def obtener_nota_por_y(y_click):
    inicio_y = 80
    for i in range(len(notas_frecuencias)):
        y_nota = inicio_y + i * (espaciado_linea // 2)
        if abs(y_click - y_nota) < 6:
            return y_nota, notas_frecuencias[i], 0
    return None, None, None

def borrar_nota_mas_cercana(x_click, y_click):
    for i, (x, y, _, _, _, _, _) in enumerate(notas):
        if abs(x - x_click) <= 10 and abs(y - y_click) <= 10:
            del notas[i]
            break

ejecutando = True
while ejecutando:
    screen.fill(BLANCO)
    dibujar_pentagramas(screen)
    dibujar_notas(screen, imagenes_figuras)

    for texto, rect in botones.items():
        pygame.draw.rect(screen, VERDE, rect)
        screen.blit(fuente.render(texto, True, NEGRO), (rect.x + 10, rect.y + 5))

    for clave, rect in figura_botones.items():
        pygame.draw.rect(screen, GRIS if clave != figura_actual else AZUL, rect)
        screen.blit(fuente.render(clave, True, BLANCO), (rect.x + 15, rect.y + 5))

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            x, y_click = evento.pos
            for texto, rect in botones.items():
                if rect.collidepoint(evento.pos):
                    if texto == "Reproducir":
                        notas_ordenadas = sorted(notas, key=lambda n: n[0])
                        inicio = nota_inicio if nota_inicio is not None else 0
                        for x_pos, _, freq, dur, _, _, _ in notas_ordenadas[inicio:]:

                            screen.fill(BLANCO)
                            dibujar_pentagramas(screen)
                            dibujar_notas(screen, imagenes_figuras)
                            for t, r in botones.items():
                                pygame.draw.rect(screen, VERDE, r)
                                screen.blit(fuente.render(t, True, NEGRO), (r.x + 10, r.y + 5))
                            for k, r in figura_botones.items():
                                pygame.draw.rect(screen, GRIS if k != figura_actual else AZUL, r)
                                screen.blit(fuente.render(k, True, BLANCO), (r.x + 15, r.y + 5))
                            dibujar_linea_tiempo(screen, x_pos)
                            tipo = "Pausa" if figura_actual == '0' else figuras[figura_actual][0]
                            alt = "#" if modificador == 1 else "b" if modificador == -1 else "natural"
                            screen.blit(
                                fuente.render(f"Figura: {tipo} ({figuras[figura_actual][1]} ms) | Alteración: {alt}",
                                              True, AZUL), (50, 560))
                            pygame.display.flip()
                            reproducir_nota(freq, dur)

                    elif texto == "Exportar":
                        exportar_a_arduino()
                    elif texto == "Guardar":
                        guardar_partitura()
                    elif texto == "Cargar":
                        cargar_partitura()
                    elif texto == "Salir":
                        ejecutando = False
            for clave, rect in figura_botones.items():
                if rect.collidepoint(evento.pos):
                    figura_actual = clave

            if evento.button == 1:
                for i, (nx, ny, freq, dur, fig, acc, bloque) in enumerate(notas):
                    if abs(nx - x) <= 10 and abs(ny - y_click) <= 10:
                        nota_seleccionada = i
                        nota_inicio = i  # Guardar como nota de inicio de reproducción
                        arrastrando = True
                        break
                else:
                    if figura_actual == '0':
                        _, _, bloque = obtener_nota_por_y(y_click)
                        if bloque is not None:
                            y = y_click
                            notas.append((x, y, 0, figuras[figura_actual][1], figuras[figura_actual], 0, bloque))
                    else:
                        y, nota, bloque = obtener_nota_por_y(y_click)
                        if nota:
                            freq = int(nota[1] * (2 ** (modificador / 12.0)))
                            notas.append((x, y, freq, figuras[figura_actual][1], figuras[figura_actual], modificador, bloque))

            elif evento.button == 3:
                borrar_nota_mas_cercana(x, y_click)

        elif evento.type == pygame.MOUSEBUTTONUP:
            if evento.button == 1:
                arrastrando = False
                nota_seleccionada = None

        elif evento.type == pygame.MOUSEMOTION and arrastrando and nota_seleccionada is not None:
            x, y_click = evento.pos
            y, nota, bloque = obtener_nota_por_y(y_click)
            if figura_actual == '0' or nota is None:
                y = y_click
                freq = 0
            else:
                freq = int(nota[1] * (2 ** (notas[nota_seleccionada][5] / 12.0)))
            notas[nota_seleccionada] = (x, y, freq, notas[nota_seleccionada][3], notas[nota_seleccionada][4], notas[nota_seleccionada][5], bloque)

        elif evento.type == pygame.KEYDOWN:
            if evento.key in (pygame.K_PLUS, pygame.K_EQUALS):
                modificador = 1
            elif evento.key == pygame.K_MINUS:
                modificador = -1
            elif evento.key == pygame.K_n:
                modificador = 0

    tipo = "Pausa" if figura_actual == '0' else figuras[figura_actual][0]
    alt = "#" if modificador == 1 else "b" if modificador == -1 else "natural"
    screen.blit(fuente.render(f"Figura: {tipo} ({figuras[figura_actual][1]} ms) | Alteración: {alt}", True, AZUL), (50, 560))
    if nota_inicio is not None and 0 <= nota_inicio < len(notas):
        x_linea = notas[nota_inicio][0]
        dibujar_linea_tiempo(screen, x_linea)

    pygame.display.flip()

pygame.quit()