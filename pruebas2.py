import matplotlib.pyplot as plt
from datetime import datetime as dt


#--provisional--#
file_simple_M=r'C:\Users\narco\OneDrive\VS Code\Tp3_IPC\transacciones_simple.txt'
file_largo_M=r'C:\Users\narco\OneDrive\VS Code\Tp3_IPC\transacciones_largo.txt'
file_simple_C=r'C:\Users\Carolina\Documents\1° año Negocios Digitales\2° Semestre ND\IPC\Trabajo practico 3\Tp3_IPC\transacciones_simple.txt'
file_largo_C=r''

'''
|^^^^^^^^^^^^^^^^^\||__|____
|    Camioncito    ||""'|""\__,_
| _____________    l||__|__|__| )
...|(@)@)"""""""**|(@)(@) ** |(@)

'''

with open(file_simple_M,'r') as file:
    inquilinos = []
    
    primer_linea=file.readline()
    primer_linea=primer_linea.rstrip()
    nombres=primer_linea.split()
    for nombre in nombres:
        inquilinos.append(nombre)
    
    
    def separar_datos(line, inquilinos):
        datos = line.split()
        fecha = datos[0]
        pagador = datos[1]

        if pagador == "*":
            inquilinos.append(datos[2])
            deudores = None
            monto = None
        else:
            if '~' in datos:
                index_ñoqui = datos.index('~')
                monto = int(datos[2])
                if len(datos) > index_ñoqui + 1:  #Identifica si hay algo después del ñoqui, viendo el largo de la línea
                    deudores = []
                    for nombre in inquilinos:
                        if nombre not in datos[index_ñoqui + 1:]: #[1:] (desde ese índice/elemento en adelante)
                            deudores.append(nombre)

                else:
                    deudores = inquilinos.copy()
            else:
                monto = int(datos[2])
                deudores = datos[3:]
                deudores.append(pagador)

        return fecha, pagador, monto, deudores
    
    
    def calculo_deuda():
        lista_fechas=[]
        deudas={}
        historial_deudas = [] #para guardar la evolución de las deudas
        for line in file:
            fecha, pagador, monto, deudores=separar_datos(line, inquilinos)
            deudas_iteracion = {}
            for nombre in inquilinos:
                if nombre not in deudas:
                    deudas[nombre]=0
            if pagador != '*':
                if fecha not in lista_fechas: 
                    lista_fechas.append(fecha)
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
            
            

    
    
    
    
            

        