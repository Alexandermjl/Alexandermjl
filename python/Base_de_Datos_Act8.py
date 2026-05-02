from openpyxl import Workbook

class GestorCalificaciones:
    def __init__(self):
        self.alumnos = []

    def capturar_datos(self):
        while True:
            opcion = input("¿Desea capturar un alumno? (si/no): ")
            
            if opcion == "no":
                print("Datos capturados")
                break
                
            if opcion == "si":
                nombre = input("Nombre del alumno: ")
                calificacion = float(input("Calificacion: "))
                self.alumnos.append([nombre, calificacion])

    def calcular_promedio(self):
        try:
            suma = 0
            for alumno in self.alumnos:
                # alumno[1] es la calificacion, porque alumno[0] es el nombre
                suma = suma + alumno[1] 
                
            promedio = suma / len(self.alumnos)
            return promedio
            
        except ZeroDivisionError:
            print("el promedio no se puede obtener ya que no se puede dividir entre cero")
            return -1

    # Metodo accion dentro de la clase
    def accion(self):
        wb = Workbook()
        hoja = wb.active
        hoja.append(["Nombre", "Calificacion"])
        for alumno in self.alumnos:
            hoja.append([alumno[0], alumno[1]])
            
        wb.save("Actividad8_Excel.xlsx")
        print("Archivo Excel creado con exito.")

if __name__ == "__main__":
    clase = GestorCalificaciones()
    clase.capturar_datos()
    
    respuesta = input("desea conocer el promedio general del grupo de clase? ")
    if respuesta == "si":
        promedio_final = clase.calcular_promedio()
        # Si el promedio no es -1 (es decir, no hubo error de division por cero)
        if promedio_final != -1:
            print("El promedio general del grupo es: " + str(promedio_final))
            
    guardar = input("Desea guardar la lista en el archivo de excel? (si/no): ")
    if guardar == "si":
        clase.accion()