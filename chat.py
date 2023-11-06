import matplotlib.pyplot as plt
from collections import defaultdict
from datetime import datetime
import numpy as np

def leer_archivo_transacciones(nombre_archivo):
    with open(nombre_archivo, 'r') as file:
        lines = file.readlines()
    
    # Obteniendo nombres de inquilinos
    inquilinos = lines[0].split()
    
    # Eliminando el salto de línea de cada línea y dividiéndolas por espacio
    transacciones = [line.strip().split() for line in lines[1:]]
    
    return inquilinos, transacciones

def calcular_deudas(inquilinos, transacciones, fecha_evaluar):
    deudas = defaultdict(int)
    fecha_inicial = datetime.strptime(transacciones[0][0], '%Y-%m-%d')
    
    for fecha, pagador, monto, *deudores in transacciones:
        fecha = datetime.strptime(fecha, '%Y-%m-%d')
        if fecha <= fecha_evaluar:
            if pagador in inquilinos:
                if deudores == ['~']:
                    cantidad_personas = len(inquilinos) - 1
                    monto_individual = int(monto) / cantidad_personas
                    deudas[pagador] -= int(monto)
                    for inquilino in inquilinos:
                        if inquilino != pagador:
                            deudas[inquilino] += monto_individual
                else:
                    cantidad_personas = len(deudores)
                    monto_individual = int(monto) / cantidad_personas
                    deudas[pagador] -= int(monto)
                    for inquilino in deudores:
                        deudas[inquilino] += monto_individual
    
    return deudas

def grafico_deudas(nombre_archivo):
    inquilinos, transacciones = leer_archivo_transacciones(nombre_archivo)
    fechas = [datetime.strptime(fecha, '%Y-%m-%d') for fecha, *_ in transacciones]
    fechas = list(set(fechas))  # Eliminar fechas duplicadas
    fechas.sort()  # Ordenar las fechas
    
    deudas_por_fecha = {}
    for fecha in fechas:
        deudas = calcular_deudas(inquilinos, transacciones, fecha)
        deudas_por_fecha[fecha] = deudas
    
    nombres = list(inquilinos)
    colores = ['b', 'g', 'r', 'c', 'm', 'y', 'k']  # Colores para el gráfico
    
    plt.figure(figsize=(10, 6))
    for i, nombre in enumerate(nombres):
        deuda_por_persona = [deudas_por_fecha[fecha][nombre] for fecha in fechas]
        plt.plot(fechas, deuda_por_persona, label=nombre, color=colores[i % len(colores)])
    
    plt.xlabel('Fechas')
    plt.ylabel('Deuda en Pesos')
    plt.title('Evolución de Deudas')
    plt.legend()
    plt.show()

# Función adicional para gráfico circular de deudas a una fecha específica
def grafico_circular_deudas(nombre_archivo, fecha):
    inquilinos, transacciones = leer_archivo_transacciones(nombre_archivo)
    
    fechas = [datetime.strptime(fecha, '%Y-%m-%d') for fecha, *_ in transacciones]
    fechas = list(set(fechas))  # Eliminar fechas duplicadas
    fechas.sort()  # Ordenar las fechas
    
    fecha_valida = False
    for fecha_transaccion in fechas:
        if fecha_transaccion <= datetime.strptime(fecha, '%Y-%m-%d'):
            fecha_valida = True
            break
    
    if not fecha_valida:
        print("La fecha ingresada no es válida.")
        return
    
    deudas = calcular_deudas(inquilinos, transacciones, datetime.strptime(fecha, '%Y-%m-%d'))
    
    # Crear gráficos circulares
    plt.figure(figsize=(12, 5))
    
    plt.subplot(1, 2, 1)
    plt.pie([deuda for deuda in deudas.values() if deuda > 0], labels=[nombre + ": '" + str(deuda) + "'" for nombre, deuda in deudas.items() if deuda > 0], autopct='%1.1f%%')
    plt.title('Deben Plata')
    
    plt.subplot(1, 2, 2)
    plt.pie([deuda for deuda in deudas.values() if deuda < 0], labels=[nombre + ": '" + str(deuda) + "'" for nombre, deuda in deudas.items() if deuda < 0], autopct='%1.1f%%')
    plt.title('Les Deben')
    
    plt.show()

# Para graficar la evolución de las deudas en el archivo "transacciones_largo.txt"
grafico_deudas('transacciones_simple.txt')
# Para graficar las deudas circulares en una fecha específica en el archivo "transacciones_largo.txt"
#grafico_circular_deudas('transacciones_largo.txt', '2022-02-20')
