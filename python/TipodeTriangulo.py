#Se crea el ciclo while -
while True:

    #Se pide las medidas de los lados del triangulo
    ladoX = int(input("Ingrese el primer lado del triangulo: "))
    ladoY = int(input("Ingrese el segundo lado del triangulo: "))
    ladoZ = int(input("Ingrese el tercer lado del triangulo: "))
    
    #Se evaua que los valores no sean 0 
    if ladoX > 0 and ladoY > 0 and ladoZ > 0:
        #Se comprueba que sea un triangulo 
        if((ladoX + ladoY > ladoZ) and (ladoX + ladoZ > ladoY) and  (ladoY + ladoZ > ladoX)):
            # Clasificación del tipo de triangulo
            if ladoX == ladoY and ladoY == ladoZ:
                print("Es un triángulo equilátero")
            elif ladoX == ladoY or ladoX == ladoZ or ladoY == ladoZ:
                print("Es un triángulo isósceles")
            else:
                print("Es un triángulo escaleno")

        else:
            print("No se forma un triángulo")

    else:
        print("Los lados deben ser mayores que cero")
        
        # AL FINAL se pregunta si quiere repetir
    x = input('¿Deseas continuar? Ingrese q para finalizar o c para continuar: ')
    if x == 'q' or x == 'quit':
        print("Saliendo del programa...")
        break  # Rompe el ciclo
    
    elif x == 'c' or x == 'continuar':
        print("Reiniciando...")