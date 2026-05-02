class GestorCalificaciones:
    
    def __init__(self):
        self.alumnos = []

    # Método para capturar datos
    def capturar_datos(self):
        while True:
            nombre = input("Ingresa el nombre del alumno: ")
            calificacion = float(input("Ingresa la calificacion: "))
            
            self.alumnos.append([nombre, calificacion])
            
            opcion = input("Desea seguir capturando? (si/no): ")
            
            if opcion == "no":
                print("Datos capturados")
                break

    # Método para calcular promedio
    def calcular_promedio(self):
        try:
            suma = 0
            for alumno in self.alumnos:
                suma = suma + alumno[1]
            
            promedio = suma / len(self.alumnos)
            print("El promedio general del grupo es:", promedio)
        
        except ZeroDivisionError:
            print("el promedio no se puede obtener ya que no se puede dividir entre cero")


if __name__ == "__main__":
    
    clase = GestorCalificaciones()
    clase.capturar_datos()
    respuesta = input("desea conocer el promedio general del grupo de clase? (si/no): ")
    if respuesta == "si":
        clase.calcular_promedio()
    
    
    


