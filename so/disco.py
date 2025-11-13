import time
from collections import deque
import random  # Para darle un poco de variabilidad al consumo

class SistemaArchivos:
    def __init__(self, tamano_disco=50):
        # El disco tiene 50 MB por defecto
        self.tamano_disco = tamano_disco
        self.disco = [None] * tamano_disco
        self.cola = deque()
        self.archivos = {}  # nombre: {"tamano": X, "ram": Y, "cpu": Z}

# Funciones internas del sistema
    def espacio_libre(self):
        return self.disco.count(None)

    def crear_archivo(self, nombre, tamano):
        if nombre in self.archivos:
            print(f"Ya existe un archivo llamado '{nombre}'.")
            return

        if tamano > self.espacio_libre():
            print(f"No hay suficiente espacio. Solo quedan {self.espacio_libre()} MB libres.")
            return

# Calcular consumo de RAM y CPU según el tamaño del archivo
        # RAM crece de forma proporcional (ej. 10% del tamaño, con ligera variación)
        consumo_ram = int(tamano * 0.1 + random.uniform(0.5, 2.0))
        # CPU depende más del tamaño, pero con un límite de 100%
        consumo_cpu = min(int(tamano * 1.5 + random.uniform(1, 10)), 100)

# Asignar espacio en el disco
        ocupados = 0
        for i in range(len(self.disco)):
            if self.disco[i] is None:
                self.disco[i] = nombre
                ocupados += 1
                if ocupados == tamano:
                    break

# Guardar la información del archivo
        self.archivos[nombre] = {
            "tamano": tamano,
            "ram": consumo_ram,
            "cpu": consumo_cpu
        }
        self.cola.append(nombre)

        print(f"Archivo '{nombre}' creado ({tamano} MB).")
        print(f"→ Consumo: RAM {consumo_ram} MB | CPU {consumo_cpu}%")
        print(f"Espacio libre: {self.espacio_libre()} MB")

    def eliminar_mas_antiguo(self):
        if not self.cola:
            print("No hay archivos para eliminar.")
            return

        nombre = self.cola.popleft()
        self._liberar_espacio(nombre)
        print(f"Archivo '{nombre}' eliminado (más antiguo). Espacio libre: {self.espacio_libre()} MB")

    def eliminar_por_nombre(self, nombre):
        if nombre not in self.archivos:
            print(f"No existe un archivo llamado '{nombre}'.")
            return

        if nombre in self.cola:
            self.cola.remove(nombre)
        self._liberar_espacio(nombre)
        print(f"Archivo '{nombre}' eliminado correctamente. Espacio libre: {self.espacio_libre()} MB")

    def _liberar_espacio(self, nombre):
        for i in range(len(self.disco)):
            if self.disco[i] == nombre:
                self.disco[i] = None
        self.archivos.pop(nombre)

# Funciones de visualización
    def mostrar_archivos(self):
        print("\nArchivos almacenados:")
        if not self.archivos:
            print("   (No hay archivos guardados)")
        else:
            for i, (nombre, datos) in enumerate(self.archivos.items(), start=1):
                print(f"   {i}. {nombre} - {datos['tamano']} MB | RAM: {datos['ram']} MB | CPU: {datos['cpu']}%")

    def mostrar_estado(self):
        usados = self.tamano_disco - self.espacio_libre()
        print(f"\nEspacio usado: {usados}/{self.tamano_disco} MB  |  Libres: {self.espacio_libre()} MB\n")

# Menu interactivo
    def menu(self):
        print("Simulador de Espacio en Disco\n")
        while True:
            self.mostrar_estado()
            print("1. Crear archivo")
            print("2. Eliminar archivo más antiguo")
            print("3. Eliminar archivo por nombre")
            print("4. Ver archivos guardados")
            print("5. Salir\n")

            opcion = input("Seleccione una opción: ")

            if opcion == "1":
                nombre = input("Nombre del archivo: ")
                try:
                    tamano = int(input("Tamaño en MB: "))
                    self.crear_archivo(nombre, tamano)
                except ValueError:
                    print("Ingrese un número válido.")
            elif opcion == "2":
                self.eliminar_mas_antiguo()
            elif opcion == "3":
                nombre = input("Nombre del archivo a eliminar: ")
                self.eliminar_por_nombre(nombre)
            elif opcion == "4":
                self.mostrar_archivos()
            elif opcion == "5":
                print("Saliendo del sistema...")
                break
            else:
                print("Opción no válida. Intente de nuevo.")

            time.sleep(1)

if __name__ == "__main__":
    sistema = SistemaArchivos()
    sistema.menu()