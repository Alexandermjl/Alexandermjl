
# Crear diccionario vacío
estudiante = {}

# Pedir datos al usuario
estudiante["nombre"] = input("Ingrese el nombre: ")
estudiante["apellido"] = input("Ingrese el apellido: ")
estudiante["matricula"] = input("Ingrese la matrícula: ")
estudiante["edad"] = input("Ingrese la edad: ")

#Crea una variable para manejar los espacios
space = " "

# 4. Mostrar información 
print("\nDatos del Estudiante ")
print(estudiante["nombre"] + space + estudiante["apellido"] + "," + space +  "estudiante con matrícula" + space + estudiante["matricula"] + space +  "y edad de" + space + estudiante["edad"] + space + "años.")