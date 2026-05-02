# Función para llenar la matriz
def Matrices(n):
    matriz = []
    lista = []
    for i in range(0, n):
        fila = []
        for j in range(0, n):
            valor = int(input(f"Ingrese el valor de la fila {i} y columna {j}: "))
            fila.append(valor)
            lista.append(valor)
        matriz.append(fila)
    
    # Mostrar matriz original
    print(f"\nOrden de la matriz: {n}x{n}")
    for i in range(0, n):
        for j in range(0, n):
            print(matriz[i][j], end=" ")
        print()
    
    return lista

# Función para ordenar y mostrar la matriz
def ordenar_y_mostrar(lista, n):
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

    # ORDEN INVERSO
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

n = int(input("Ingrese el tamaño del arreglo n x n: "))
datos_lista = Matrices(n)
ordenar_y_mostrar(datos_lista, n)