

with open(r'C:\Users\Carolina\Documents\1° año Negocios Digitales\2° Semestre ND\IPC\Trabajo practico 3\Tp3_IPC\transacciones_simple.txt','r') as file:
    datos_deuda={}
    lista_nombres = []
    
    primer_linea=file.readline()
    primer_linea=primer_linea.rstrip()
    nombres=primer_linea.split(' ')
    for nombre in nombres:
        lista_nombres.append(nombre)
    
    
    def separacion_datos ():
        
        for line in file:
            datos = line.split()
            fecha = datos[0]
            
            if datos[1] == "*":
                lista_nombres.append(datos[2])
            else:
                if datos[1] in lista_nombres:
                    datos_deuda[datos[1]] += datos[2]
                    
        
                  
                
                
                
        
    separacion_datos()