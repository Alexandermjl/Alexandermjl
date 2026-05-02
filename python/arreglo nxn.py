n = int(input("Ingrese el tamaño del arreglo n x n: "))

matriz = []
lista = []

# Pedir datos por fila y columna
for i in range(0, n):
    fila = []
    for j in range(0, n):
        valor = int(input(f"Ingrese el valor de la fila {i} y columna {j}: "))
        fila.append(valor)
        lista.append(valor)
    matriz.append(fila)

# ORDEN CRECIENTE 
for i in range(0, len(lista)):
    for j in range(0, len(lista)):
        if lista[i] < lista[j]:
            lista[i], lista[j] = lista[j], lista[i]

print("\nArreglo en orden creciente:")

indice = 0
for i in range(0, n):
    for j in range(0, n):
        print(lista[indice], end=" ")
        indice = indice + 1
    print()

# ORDEN Inverso
for i in range(0, len(lista)):
    for j in range(0, len(lista)):
        if lista[i] > lista[j]:
            lista[i], lista[j] = lista[j], lista[i]

print("\nArreglo en orden inverso:")

indice = 0
for i in range(0, n):
    for j in range(0, n):
        print(lista[indice], end=" ")
        indice = indice + 1
    print()
    
    
    