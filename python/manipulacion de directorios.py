import os 
from pathlib import Path

# Clase 1: Responsable de representar un archivo reporte 
class Reporte:
    def __init__(self, nombre, ruta_carpeta):
        self.nombre = nombre
        self.ruta_archivo = ruta_carpeta / nombre 

    def escribir_informacion(self, contenido):
        with open(self.ruta_archivo, "w") as archivo:
            archivo.write(contenido) 
        print(f"-> Escrito contenido en: {self.nombre}")

    def mostrar_detalles(self):
        if self.ruta_archivo.exists(): 
            print(f"  - Archivo: {self.ruta_archivo.name}") 
            print(f"  - Extensión: {self.ruta_archivo.suffix}") 
            print(f"  - Ruta Absoluta: {self.ruta_archivo.resolve()}") 

   # Clase 2: Administra la carpeta y los reportes 
class GestorDeProyectos:
    def __init__(self, ruta_personalizada):
        self.ruta_base = Path(ruta_personalizada) 
        self.ruta_proyecto = self.ruta_base / "Proyecto_Pathlib"

    def preparar_entorno(self):
        print(f"Directorio de trabajo actual: {os.getcwd()}") 
        
        if not self.ruta_proyecto.exists():
            self.ruta_proyecto.mkdir(parents=True) 
            print(f"Carpeta creada exitosamente.")
        else:
            print(f"La carpeta ya existe.")

    def procesar(self):
        datos = {
            "reporte1.txt": "Actividad 7.",
            "reporte2.txt": "Programacion Orientada a Objetos.",
            "reporte3.txt": "Teams."
        }
        
        print("\n--- Procesando Archivos ---")
        for nom, texto in datos.items():
            rep = Reporte(nom, self.ruta_proyecto)
            rep.escribir_informacion(texto)
            rep.mostrar_detalles() 
            
    def lista_txt(self):
        archivos = list(self.ruta_proyecto.glob("*.txt"))
        for item in archivos:
            print(f"Encontrado: {item.name}")

if __name__ == "__main__":
    mi_ruta = os.getcwd()
    app = GestorDeProyectos(mi_ruta)
    app.preparar_entorno()
    app.procesar()
    app.lista_txt()