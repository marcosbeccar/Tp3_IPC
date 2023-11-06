

with open(r'C:\Users\narco\OneDrive\VS Code\Tp3_IPC\transacciones_simple.txt','r') as file:
    datos_deuda={}
    primer_linea=file.readline()
    primer_linea=primer_linea.rstrip()
    nombres=primer_linea.split(' ')
    for nombre in nombres:
        datos_deuda[nombre]=0
    
            
print(datos_deuda)
        