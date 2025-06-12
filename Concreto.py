import pygame
import sys
import numpy as np
import json
import tkinter as tk
from tkinter import filedialog

modulos = []  # lista de listas de notas por módulo
modulo_actual = 0


pygame.init()
screen = pygame.display.set_mode((1350, 300))
pygame.display.set_caption("Editor Musical Arduino - Un Pentagrama")


# Colores
BLANCO, NEGRO, ROJO, AZUL, GRIS, VERDE = (255, 255, 255), (0, 0, 0), (220, 30, 30), (0, 0, 200), (150, 150, 150), (0, 200, 0)
fuente = pygame.font.SysFont(None, 22)

espaciado_linea = 20
radio_nota = 8
altura_bloque = 180
num_pentagramas = 1

# Notas
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

figura_actual = '3'
modificador = 0
notas = []
nota_seleccionada = None
arrastrando = False

# Botones
# Botones
botones = {
    "Reproducir": pygame.Rect(50, 10, 100, 30),
    "Exportar": pygame.Rect(180, 10, 100, 30),
    "Guardar": pygame.Rect(440, 10, 100, 30),  # movido arriba
    "Cargar": pygame.Rect(560, 10, 100, 30),   # movido arriba
    "Salir": pygame.Rect(310, 10, 100, 30)
}


# Crear botones de figuras
# Crear botones de figuras en la parte superior derecha
# Crear botones de figuras (1 al 5) en posición vertical, parte superior derecha
# Crear botones de figuras (1 al 5) en la parte superior derecha, en horizontal
figura_botones = {}
for i, clave in enumerate(['1', '2', '3', '4', '5', '0']):
    figura_botones[clave] = pygame.Rect(750 + i * 60, 10, 55, 30)






def generar_tono(frecuencia, duracion_ms):
    rate = 44100
    n_samples = int(rate * duracion_ms / 1000)
    buffer = (np.sin(2 * np.pi * np.arange(n_samples) * frecuencia / rate) * 32767).astype(np.int16)
    sonido = pygame.sndarray.make_sound(np.column_stack([buffer, buffer]))
    return sonido

def reproducir_nota(frecuencia, duracion):
    if frecuencia == 0:
        pygame.time.delay(duracion)
        return
    sonido = generar_tono(frecuencia, duracion)
    sonido.play()
    pygame.time.delay(int(duracion * 1.05))
    sonido.stop()

def obtener_nota_por_y(y_click):
    inicio_y = 80
    for i in range(len(notas_frecuencias)):
        y_nota = inicio_y + i * (espaciado_linea // 2)
        if abs(y_click - y_nota) < 6:
            return y_nota, notas_frecuencias[i], 0  # Siempre bloque 0
    return None, None, None


def dibujar_pentagramas():
    offset_y = 80
    for i in range(5):
        y = offset_y + 6 * espaciado_linea // 2 + i * espaciado_linea
        pygame.draw.line(screen, NEGRO, (50, y), (1300, y), 2)


def dibujar_notas():
    for x, y, freq, dur, fig, acc, bloque in notas:
        if freq == 0:
            pygame.draw.rect(screen, GRIS, (x - 6, y - 6, 12, 12))
            screen.blit(fuente.render("P", True, NEGRO), (x - 6, y - 25))
        else:
            pygame.draw.circle(screen, ROJO, (x, y), radio_nota)
            texto = fig[0][0] + ("#" if acc == 1 else "b" if acc == -1 else "")
            screen.blit(fuente.render(texto, True, AZUL), (x - 10, y - 30))

def exportar_a_arduino(nombre="ElPatoRenato.ino"):
    notas_ordenadas = sorted(notas, key=lambda n: n[0])
    with open(nombre, "w") as f:
        f.write("// Generado automáticamente\n")
        f.write("const int buzzerPin = 3;\n\n")
        f.write("void setup() {}\n\n")
        f.write("void loop() {\n")
        for _, _, freq, dur, _, _, _ in notas_ordenadas:
            if freq == 0:
                f.write(f"  delay({dur});\n")
            else:
                f.write(f"  tone(buzzerPin, {freq}, {dur});\n")
                f.write(f"  delay({int(dur * 1.2)});\n")
                f.write("  noTone(buzzerPin);\n")
        f.write("  delay(2000);\n")
        f.write("}\n")
    print(f"Exportado a: {nombre}")


def guardar_partitura(nombre="partitura.json"):
    with open(nombre, "w") as f:
        json.dump(notas, f)

def cargar_partitura(nombre="partitura.json"):
    global notas
    with open(nombre, "r") as f:
        notas = json.load(f)


def borrar_nota_mas_cercana(x_click, y_click):
    for i, (x, y, _, _, _, _, _) in enumerate(notas):
        if abs(x - x_click) <= 10 and abs(y - y_click) <= 10:
            del notas[i]
            break

ejecutando = True
while ejecutando:
    screen.fill(BLANCO)
    dibujar_pentagramas()
    dibujar_notas()

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
                        for _, _, freq, dur, _, _, _ in sorted(notas, key=lambda n: n[0]):
                            reproducir_nota(freq, dur)
                    elif texto == "Exportar":
                        exportar_a_arduino()
                    elif texto == "Guardar":
                        guardar_partitura()  # NUEVO
                    elif texto == "Cargar":
                        cargar_partitura()  # NUEVO
                    elif texto == "Salir":
                        ejecutando = False
            for clave, rect in figura_botones.items():
                if rect.collidepoint(evento.pos):
                    figura_actual = clave

            if evento.button == 1:
                for i, (nx, ny, freq, dur, fig, acc, bloque) in enumerate(notas):
                    if abs(nx - x) <= 10 and abs(ny - y_click) <= 10:
                        nota_seleccionada = i
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
    screen.blit(
        fuente.render(
            f"Figura: {tipo} ({figuras[figura_actual][1]} ms) | Alteración: {alt}", True, AZUL
        ),
        (50, 560)
    )

    pygame.display.flip()

pygame.quit()