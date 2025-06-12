import json
import tkinter as tk
from tkinter import filedialog
from estado import notas
from estado import notas

import json
import tkinter as tk
from tkinter import filedialog
from estado import notas

def exportar_a_arduino():
    root = tk.Tk()
    root.withdraw()
    nombre = filedialog.asksaveasfilename(
        defaultextension=".ino",
        filetypes=[("Código Arduino", "*.ino")],
        title="Exportar a archivo .ino"
    )
    if nombre:
        notas_ordenadas = sorted(notas, key=lambda n: n[0])
        with open(nombre, "w") as f:
            f.write("// Generado automáticamente\n")
            f.write("const int buzzerPin = 3;\n\n")
            f.write("void setup() {}\n\n")
            f.write("void loop() {\n")
            for _, _, freq, dur, *_ in notas_ordenadas:
                if freq == 0:
                    f.write(f"  delay({dur});\n")
                else:
                    f.write(f"  tone(buzzerPin, {freq}, {dur});\n")
                    f.write(f"  delay({int(dur * 1.2)});\n")
                    f.write("  noTone(buzzerPin);\n")
            f.write("  delay(2000);\n")
            f.write("}\n")


def guardar_partitura():
    root = tk.Tk()
    root.withdraw()  # Ocultar ventana principal de Tkinter
    nombre = filedialog.asksaveasfilename(
        defaultextension=".json",
        filetypes=[("Archivos JSON", "*.json")],
        title="Guardar partitura como"
    )
    if nombre:
        with open(nombre, "w") as f:
            json.dump(notas, f)

def cargar_partitura():
    global notas
    root = tk.Tk()
    root.withdraw()
    nombre = filedialog.askopenfilename(
        defaultextension=".json",
        filetypes=[("Archivos JSON", "*.json")],
        title="Cargar partitura"
    )
    if nombre:
        with open(nombre, "r") as f:
            notas[:] = json.load(f)