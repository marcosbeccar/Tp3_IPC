
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

with open(file_largo_M,'r') as file:
    datos_deuda={}
    inquilinos = []
    
    primer_linea=file.readline()
    primer_linea=primer_linea.rstrip()
    nombres=primer_linea.split(' ')
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
                if len(datos) > index_ñoqui + 1:
                    deudores = []
                    for nombre in inquilinos:
                        if nombre not in datos[index_ñoqui + 1:]:
                            deudores.append(nombre)

                else:
                    deudores = inquilinos.copy()
            else:
                monto = int(datos[2])
                deudores = datos[3:]
                deudores.append(pagador)

        return print(fecha, pagador, monto, deudores)



    for line in file:
        separar_datos(line,inquilinos)