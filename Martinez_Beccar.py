import matplotlib.pyplot as plt
from datetime import datetime as dt

#--provisional--#
file_simple_M=r'C:\Users\narco\OneDrive\VS Code\Tp3_IPC\transacciones_simple.txt'
file_largo_M=r'C:\Users\narco\OneDrive\VS Code\Tp3_IPC\transacciones_largo.txt'
file_simple_C=r'C:\Users\Carolina\Documents\1° año Negocios Digitales\2° Semestre ND\IPC\Trabajo practico 3\Tp3_IPC\transacciones_simple.txt'
file_largo_C=r'C:\Users\Carolina\Documents\1° año Negocios Digitales\2° Semestre ND\IPC\Trabajo practico 3\Tp3_IPC\transacciones_largo.txt'

### --INPUTS-- ###
archivo=file_largo_M
fecha_usuario= '2028-11-20'  
'2022-02-21' 'última fecha simple'
'2028-11-20' 'ultima fecha transacciones largo' 


with open(archivo,'r') as file: #Abrimos el archivo con el método with open para que al finalizar la ejecución del bloque de codigo, Python automáticamente cierre el archivo
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
                    deudas[nombre]=0 #Lo agregamos como clave con el valor 0 (deuda 0)
            
            if pagador != '*': #Siempre que haya un nombre y no el caracter "*"...
                if fecha not in lista_fechas:  # Si la fecha no está en la lista de fechas...
                    lista_fechas.append(fecha)  # Agregamos la fecha
                    deudas[pagador] -= round(monto)  # Se descuenta el monto para quien pagó la deuda
                    deuda = monto / len(deudores)  # Hacemos el cálculo de cuánto es el monto que tiene que pagar cada uno

                    for persona in deudores:  # Para cada uno de los que tienen que pagar la deuda...
                        deudas[persona] += round(deuda)  # Les sumamos el monto

                    # Agregamos el estado actual de las deudas a historial_deudas
                    deudas_iteracion = deudas.copy()
                    historial_deudas.append(deudas_iteracion)
                   
                    
                else: #Si la fecha ya estaba en la lista de las fechas...
                    deudas[pagador]-=round(monto)#Se descuenta el monto para quien pago la deuda
                    deuda=monto/len(deudores)
                    for persona in deudores:
                        deudas[persona]+=round(deuda)
                                    
        return deudas, lista_fechas, historial_deudas
    
    
    def grafico_evolucion(historial_deudas, lista_fechas, inquilinos):
        #Función para generar un gráfico de línea que muestra la evolución de las deudas de cada persona a lo largo del tiempo. 
        #ENTRADAS: 
            # - historial_deudas: lista de diccionarios que contiene información sobre las deudas de cada persona a lo largo del tiempo.
            # - lista_fechas: lista que contiene las fechas correspondientes a las deudas en el historial.
            # - inquilinos: lista que contiene los nombres de los inquilinos.
        #SALIDAS:
        
        for nombre in inquilinos: #Recorremos cada inquilino
            deuda_por_persona = []
            for deuda in historial_deudas: #Recorremos el historial de deudas para obtener la deuda de esa persona en cada fecha
                deuda_por_persona.append(deuda.get(nombre)) #Buscamos el nombre en cada diccionario de deudas
                
            plt.plot(lista_fechas, deuda_por_persona, label=nombre)

        plt.xlabel('Fechas') #El eje x representa las fechas
        plt.ylabel('Deuda') # El eje y representa las deudas
        plt.title('Evolución de las deudas por persona') #Establecemos el título
        plt.legend()
        plt.xticks([lista_fechas[0],lista_fechas[-1]],visible=True,rotation=60) #Hace que solo se vea la primer y última fecha usando xticks
        plt.tight_layout()
        #plt.show() #mejor no, asi aparecen ambos gráficos a la vez cuando se ejecuta el programa
        
    
    def proceder(datos_buscados):
        #Función que genera un gráfico que muestra quién debe dinero y a quién le deben dinero en una fecha específica
        #ENTRADA: el diccionario "datos_buscados" que contiene la información de las deudas en una fecha específica.
        
        deuda_fecha=[] #Lista que almacenará la información sobre las deudas hasta una fecha específica
        for nombre in inquilinos: #Para cada inquilino...
            monto_fecha=datos_buscados.get(nombre) #Se obtiene el monto de la deuda en la fecha específica desde el diccionario datos_buscados. 
            if monto_fecha == None: #Si el monto es none...
                deuda_fecha.append(0) #Se asume que la deuda es 0.
            else: 
                deuda_fecha.append(monto_fecha) 
        
        i=0
        #Generación de listas para el gráfico
        deben=[] #Lista para las deudas positivas 
        les_deben=[] #Lista para las deudas negativas
        deben_nombres=[] #Lista para almacenar los nombres de quienes tienen las deudas positivas 
        les_deben_nombres=[]#Lista para almacenar los nombres de quienes tienen las deudas negativas
         
        for deuda in deuda_fecha:
            if deuda >0: #Si la deuda es positiva....
                deben.append(deuda) #Se agrega a la lista "deben"
                deben_nombres.append(inquilinos[i]+f'\n${deuda}') #Utilizamos una cadena formateada para agregar la deuda a la etiqueta, precedida por un salto de línea (\n) y el símbolo del dólar ($). Esto hace que el nombre del inquilino y la cantidad de deuda se muestran en líneas separadas.
            elif deuda==0:
                pass
            else: #Si la deuda es negativa...
                les_deben.append(-deuda) #Se agrega a la lista "les_deben" con la deuda en negativo
                les_deben_nombres.append(inquilinos[i]+f'\n${deuda}')
            i+=1    
        
        #Creamos una figura con dos subgráficos (subplots), cada uno representando una parte 
        
        #El primer subgráfico muestra las deudas (deben)
        plt.figure()
        plt.subplot(1,2,1)
        plt.pie(deben, labels=deben_nombres)
        plt.title('Esta gente debe plata')
        
        #El segundo subgráfico muestra las deudas negativas (les_deben)
        plt.subplot(1,2,2)
        plt.pie(les_deben, labels=les_deben_nombres)
        plt.title('A esta gente le deben plata')
        plt.show()
      
      
        
    def grafico_torta(deudas, fecha_usuario):
        # La función genera un gráfico de torta que muestra quién debe dinero y a quién le deben dinero en una fecha específica o en la fecha más reciente antes de la fecha proporcionada por el usuario.
       
        fechas = [] 
        for fecha in lista_fechas:  
            fecha_convertida = dt.strptime(fecha, '%Y-%m-%d')  # Convertimos cada fecha a un objeto datetime
            fechas.append(fecha_convertida)
        primera_fecha = min(fechas) #Recuperamos la primer fecha
        ultima_fecha = max(fechas)  #Recuperamos la última fecha
        fecha_usuario_dt= dt.strptime(fecha_usuario, '%Y-%m-%d') #La fecha proporcionada por el usuario también la conviertimos a un objeto datetime
        
        if primera_fecha <= fecha_usuario_dt <= ultima_fecha: #Verificamos si la fecha proporcionada por el usuario está dentro del rango de fechas existentes
            
            if fecha_usuario in lista_fechas:
                #Si la fecha proporcionada por el usuario está en la lista de fechas,.
                indice=lista_fechas.index(fecha_usuario) #Buscamos el indice
                datos_buscados=historial_deudas[indice] 
                proceder(datos_buscados) #Se extraen los datos de deuda para esa fecha específica utilizando la función proceder
            
            else: #Si la fecha proporcionada por el usuario no está en la lista de fechas....
                ultima_fecha_registrada = None
                #Buscamos la fecha más reciente antes de la fecha del usuario 
                for fecha in lista_fechas:
                    fecha=dt.strptime(fecha, '%Y-%m-%d')
                    if fecha < fecha_usuario_dt:
                        ultima_fecha_registrada = fecha
                    else:
                        break
                ultima_fecha_registrada=ultima_fecha_registrada.strftime('%Y-%m-%d')
                indice=lista_fechas.index(ultima_fecha_registrada)
                datos_buscados=historial_deudas[indice]
                proceder(datos_buscados) #extraemos los datos de deuda para esa fecha utilizando la función proceder
            
        else:
            print("--Fecha inválida--")

    
    ### --FUNCIONES-- ###
    deudas, lista_fechas, historial_deudas=calculo_deuda()
    grafico_evolucion(historial_deudas, lista_fechas, inquilinos)
    grafico_torta(deudas,fecha_usuario)
            

    ### --EXTRAS-- ###

    def generar_informe(archivo, deudas, lista_fechas, historial_deudas):
        #Creo el informe al último día analizado
        ultima_fecha = lista_fechas[-1]

        #junta los datos de deuda para la última fecha
        indice_ultima_fecha = lista_fechas.index(ultima_fecha)
        datos_ultima_fecha = historial_deudas[indice_ultima_fecha]

        deudores = []
        acreedores = []

        #Clasificación de inquilinos como deudores o acreedores
        for nombre, monto_deuda in datos_ultima_fecha.items():
            if monto_deuda < 0:
                acreedores.append((nombre, abs(monto_deuda)))
            elif monto_deuda > 0:
                deudores.append((nombre, monto_deuda))

        #Empiezo a armar el reporte con \n=salto de línea
        report = f"Registro de deudas al {ultima_fecha}\n\nDeudores:\n\n"

        for nombre, monto_deuda in deudores:
            report += f" {nombre} debe dar ${monto_deuda:,.2f}\n"
        '''
        ':,.2f' indica el formato para que se lea mejor. La coma indica que se debe separar 
        con comas, y '2f' indica que debe ser un float limitado a 2 decimales. 
        '''
        
        report += "\nAcreedores:\n\n"

        for nombre, monto_acreencia in acreedores:
            report += f" {nombre} debe recibir ${monto_acreencia:,.2f}\n" 

        report += "\nIntercambios:\n\n"

        while True:
            #Busca al inquilino con más deuda para ordenarlo
            deudor = None
            for nombre, _ in deudores: #el '_' se usa para ignorar el segundo dato de deudores (el monto)
                deudor = nombre
                break #corta para conseguir el primer deudor
            if deudor is None:
                break  #Corta si no hay deudores

            # Buscar el acreedor con la acreencia más grande
            acreedor = None
            for nombre, _ in acreedores:
                acreedor = nombre
                break 
            if acreedor is None:
                break  #Corta si no hay acreedores

            #Calculo del monto de intercambio
            monto_intercambio = min(deudores[0][1], acreedores[0][1])

            #Actualiza las listas de deudores y acreedores y agrega el intercambio al report
            deudores[0] = (deudores[0][0], deudores[0][1] - monto_intercambio)
            acreedores[0] = (acreedores[0][0], acreedores[0][1] - monto_intercambio)
            report += f" {deudor} debe pagarle a {acreedor} ${monto_intercambio:,.2f}\n"

            #En el caso que la deuda de alguin sea 0, lo elimina.
            if deudores[0][1] == 0:
                deudores.pop(0)
            
            if acreedores[0][1] == 0:
                acreedores.pop(0) #elimina al acreedor si ya no debe recibir plata

        #Guarda el report en un archivo
        archivo_nuevo = "reporte.txt"
        with open(archivo_nuevo, "w") as archivo_informe: # 'w' de write
            archivo_informe.write(report)

        print(f"Reporte ubicado en: {archivo_nuevo}")

    generar_informe(archivo, deudas, lista_fechas, historial_deudas)



