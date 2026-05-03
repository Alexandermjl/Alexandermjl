import math

# Entradas (Inputs)
radio = float(input("Ingresa el radio del circulo: "))
cateto_a = float(input("Ingresa el cateto a: "))
cateto_b = float(input("Ingresa el cateto b: "))
celsius = float(input("Ingresa la temperatura en grados Celsius: "))

#Procesos (Cálculos)
area = math.pi * (radio ** 2)
hipotenusa =  math.sqrt((cateto_a ** 2) + (cateto_b ** 2))
fahrenheit = (celsius * (9 / 5)) + 32

# Salidas (Outputs)
print(f"El area del circulo es: {area:.2f}")
print(f"El valor de la hipotenusa es: {hipotenusa:.2f}" )
print(f"La temperatura en Fahrenheit es: {fahrenheit:.2f}")