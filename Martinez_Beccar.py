import matplotlib.pyplot as plt

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


    lista_fechas=[]
    deudas={}
    
    
    def calculo_deuda():
        for line in file:
            fecha, pagador, monto, deudores=separar_datos(line, inquilinos)
            for nombre in inquilinos:
                if nombre not in deudas:
                    deudas[nombre]=0
            if fecha not in lista_fechas:
                lista_fechas.append(fecha)
            if pagador != '*':
                deudas[pagador]-=round(monto)
                deuda=monto/len(deudores)
                for persona in deudores:
                    deudas[persona]+=round(deuda)
            
            
        

    calculo_deuda()
    print(deudas)

        