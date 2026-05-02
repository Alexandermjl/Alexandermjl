# Crear 3 listas
nombreEquipo= []
ipAddress = []
location = []

# Abrir archivo en modo escritura (w)
file = open("Equipos.txt", "w")

while True:
    
    Equipo = input("Ingrese el nombre del equipo (o escriba exit  para terminar): ")
    
    if Equipo == "exit":
        print("¡Proceso finalizado!")
        break
    
    ip = input("Ingrese la direccion IP: ")
    ciudad = input("Ingrese la ciudad: ")
    
    # Guardar en listas
    nombreEquipo.append(Equipo)
    ipAddress.append(ip)
    location.append(ciudad)

for index, item in enumerate(nombreEquipo):
    
    linea = str(index) + " Equipo " + nombreEquipo[index] + ", Direccion IP: " + ipAddress[index] + ", Ciudad: " + location[index]
    
    file.write(linea.strip() + "\n")

file.close()

