def hola():
    with open("C:\Users\Carolina\Documents\1° año Negocios Digitales\2° Semestre ND\IPC\Trabajo practico 3\Tp3_IPC\transacciones_simple.txt") as file:
        listas_para_graficar=[] #una por nombre
        linea1=file.readline()
        lista_de_primeros_nombres=linea1.split('')
        i=0
        primeros_nombres=[]
        for nombre in lista_de_primeros_nombres:
            primeros_nombres.append(nombre)
        
        for line in file:
            
            
            
            #dict={
            #    nombre:{fecha:deuda},
            #    nombre:{fecha:deuda}
            #}

        