import matplotlib.pyplot as plt
from datetime import datetime as dt


#--provisional--#
file_simple_M=r'C:\Users\narco\OneDrive\VS Code\Tp3_IPC\transacciones_simple.txt'
file_largo_M=r'C:\Users\narco\OneDrive\VS Code\Tp3_IPC\transacciones_largo.txt'
file_simple_C=r'C:\Users\Carolina\Documents\1° año Negocios Digitales\2° Semestre ND\IPC\Trabajo practico 3\Tp3_IPC\transacciones_simple.txt'
file_largo_C=r'C:\Users\Carolina\Documents\1° año Negocios Digitales\2° Semestre ND\IPC\Trabajo practico 3\Tp3_IPC\transacciones_largo.txt'

'''
|^^^^^^^^^^^^^^^^^\||__|____
|    Camioncito    ||""'|""\__,_
| _____________    l||__|__|__| )
...|(@)@)"""""""**|(@)(@) ** |(@)

'''

with open(file_largo_C,'r') as file: #Abrimos el archivo con el método with open para que al finalizar la ejecución del bloque de codigo, Python automáticamente cierre el archivo
    inquilinos = [] #Lista en la que, mediante ir leyendo cada linea con el for, iremos guardando los inquilinos
    
    primer_linea=file.readline() #Escribimos readline() para que lea la primer linea que contiene los nombres de los inquilinos que están desde el comienzo
    primer_linea=primer_linea.rstrip() #Eliminamos el salto de linea "/n"
    nombres=primer_linea.split() #Convertimos los nombres de la primera linea en una lista
    for nombre in nombres: #Por cada nombre en la lista de nombres..
        inquilinos.append(nombre) #Lo agregamos a la lista de inquilinos
    
    
    def separar_datos(line, inquilinos):
        #ENTRADA: 2 argumentos -->  la linea a analizar y el inquilino (ambos strings)
        #SALIDA: Por cada línea, la fecha (string), quien es el pagador (string), el monto(string) y los deudores (string)
        
        datos = line.split() #Creamos una lista con cada dato de la línea separado por espacios
        fecha = datos[0] #La fecha corresponde al elemento 0 de la lista
        pagador = datos[1] #El pagador corresponde al elemento 1 de la lista

        if pagador == "*": #Si el elemento 1 de la lista es " * " significa que se incorpora un nuevo inquilino
            inquilinos.append(datos[2]) #El nuevo inquilino se encuentra en el elemento 2 de la lista datos, después del "*"
            #A las variables deudores y monto aún no le asignamos un valor, sino más adelante
            deudores = None
            monto = None
        
        else:
            if '~' in datos: #Si se encuentra el caracter "~"...
                monto = int(datos[2])
                
                index_ñoqui = datos.index('~') #Buscamos en que posición se encuentra el caracter
                if len(datos) > index_ñoqui + 1:  #Identificamos si hay algo después del ñoqui, viendo el largo de la línea
                    deudores = []
                    for nombre in inquilinos:
                        if nombre not in datos[index_ñoqui + 1:]: #[1:] (desde ese índice/elemento en adelante)
                            deudores.append(nombre)

                else:
                    deudores = inquilinos.copy() #Creamos una copia de la lista inquilinos y asignándola a la variable deudores
            else:
                monto = int(datos[2])
                deudores = datos[3:]
                deudores.append(pagador)

        return fecha, pagador, monto, deudores
    
    
    def calculo_deuda():
        # Función que realiza un seguimiento y cálculo de las deudas entre inquilinos en función de datos proporcionados el archivo
        #SALIDAS:
        # - deudas --> Diccionario que contiene las deudas finales de cada inquilino
        # - lista_fechas --> Lista de fechas encontradas en los datos.
        # - historial_deudas --> Lista que contiene el estado de las deudas en cada iteración.
        
        #Inicialización de variables:  
        lista_fechas=[] #Lista en la que se irán guardando las fechas
        deudas={} #Diccionario en el que se guardarán las deudas totales de cada uno de los inquilinos
        historial_deudas = [] #Lista para guardar la evolución de las deudas
        
        #Iteración a través de las líneas del archivo:
        for line in file:
            fecha, pagador, monto, deudores=separar_datos(line, inquilinos) #LLamamos a la función que cramos previamente que devolvia la fecha, el pagador, el monto y los deudores
            deudas_iteracion = {}
            
            for nombre in inquilinos: 
                if nombre not in deudas: #Si el inquilino no está en el diccionario.. 
                    deudas[nombre]=0 #Lo agregamos como clave con el valor 0
            
            if pagador != '*': #Siempre que haya un nombre y no el caracter "*"...
                if fecha not in lista_fechas: #Si la fecha no está en la lista de las fechas...
                    lista_fechas.append(fecha) #Agregamos la fecha
                    deudas[pagador]-=round(monto)
                    deuda=monto/len(deudores)
                    
                    for persona in deudores:
                        deudas[persona]+=round(deuda)
                    deudas_iteracion = deudas.copy()  # Agregar una copia independiente
                    historial_deudas.append(deudas_iteracion)  # Guarda esta copia en la lista
                    
                else:
                    deudas[pagador]-=round(monto)
                    deuda=monto/len(deudores)
                    for persona in deudores:
                        deudas[persona]+=round(deuda)
                                    
        return deudas, lista_fechas, historial_deudas
    
    
    def grafico_evolucion(historial_deudas, lista_fechas, inquilinos):
        for nombre in inquilinos:
            deuda_por_persona = []
            for deuda in historial_deudas:
                deuda_por_persona.append(deuda.get(nombre)) #busca el nombre en cada diccionario de deudas
            plt.plot(lista_fechas, deuda_por_persona, label=nombre)

        plt.xlabel('Fechas')
        plt.ylabel('Deuda')
        plt.title('Evolución de las deudas por persona')
        plt.legend()
        plt.xticks(rotation=60)
        plt.tight_layout()
        #plt.show()
    
    def proceder(datos_buscados):
        deuda_fecha=[]
        for nombre in inquilinos:
            monto_fecha=datos_buscados.get(nombre)
            if monto_fecha == None:
                deuda_fecha.append(0)
            else:
                deuda_fecha.append(monto_fecha)
        i=0
        deben=[]
        les_deben=[]
        deben_nombres=[]
        les_deben_nombres=[]
        for deuda in deuda_fecha:
            if deuda >0:
                deben.append(deuda)
                deben_nombres.append(inquilinos[i]+f'\n${deuda}')
            elif deuda==0:
                pass
            else:
                les_deben.append(-deuda)
                les_deben_nombres.append(inquilinos[i]+f'\n${deuda}')
            i+=1    
        
        plt.figure()
        plt.subplot(1,2,1)
        plt.pie(deben, labels=deben_nombres)
        plt.title('Esta gente debe plata')
        plt.subplot(1,2,2)
        plt.pie(les_deben, labels=les_deben_nombres)
        plt.title('A esta gente le deben plata')
        plt.show()
        
    def grafico_torta(deudas,fecha_usuario):
        fechas = [] 
        for fecha in lista_fechas:  
            fecha_convertida = dt.strptime(fecha, '%Y-%m-%d')  # Convertir cada fecha a un objeto datetime
            fechas.append(fecha_convertida)
        primera_fecha = min(fechas)
        ultima_fecha = max(fechas)  
        fecha_usuario_dt= dt.strptime(fecha_usuario, '%Y-%m-%d')
        
        if primera_fecha <= fecha_usuario_dt <= ultima_fecha:
            if fecha_usuario in lista_fechas:
                indice=lista_fechas.index(fecha_usuario)
                datos_buscados=historial_deudas[indice]
                proceder(datos_buscados)
            else:
                ultima_fecha_registrada = None
                for fecha in lista_fechas:
                    fecha=dt.strptime(fecha, '%Y-%m-%d')
                    if fecha < fecha_usuario_dt:
                        ultima_fecha_registrada = fecha
                    else:
                        break
                ultima_fecha_registrada=ultima_fecha_registrada.strftime('%Y-%m-%d')
                indice=lista_fechas.index(ultima_fecha_registrada)
                datos_buscados=historial_deudas[indice]
                proceder(datos_buscados)
            
        else:
            print("--Fecha inválida--")
    
    
    fecha_usuario= '2022-02-21'   
    deudas, lista_fechas, historial_deudas=calculo_deuda()
    grafico_evolucion(historial_deudas, lista_fechas, inquilinos)
    grafico_torta(deudas,fecha_usuario)
            
            

    
    
    
    
            

        