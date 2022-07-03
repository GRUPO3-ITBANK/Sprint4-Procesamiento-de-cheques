import sys
import re
import csv
from datetime import datetime

expresion_regex_fecha= '\d{2}-\d{2}-\d{4}:\d{2}-\d{2}-\d{4}'#expresion regex de rango de fechas recibidas



def comparacion_regex(expresion,txt):#funcion que sirve para saber si un texto matchea con una expresion regex
    comparacion= re.search(expresion, txt)
    coincide= True if comparacion else False
    return coincide

def comprobar_parametro(posicion): #funcion que me sirve para saber si en un parametro me pasaron rango de fechas o si me pasaron estado de cheque
    global estado,fecha #para que permita modificar variables globales
    
    if(sys.argv[posicion].lower() == 'pendiente' or sys.argv[posicion].lower() == 'aprobado' or sys.argv[posicion].lower() == 'rechazado'):
        estado = sys.argv[posicion]
    elif(comparacion_regex(expresion_regex_fecha,sys.argv[posicion])):
        fecha = sys.argv[posicion]
    else:
        print(f'no se ingresó ningún valor válido para el prametro n° {posicion}')

def validacion_parametro_opcional():  #funcion que me sirve para saber  si hay uno o dos parametros opcionales
    if (len(sys.argv)==6):
        comprobar_parametro(5)
    elif (len(sys.argv)==7): 
        comprobar_parametro(5)
        comprobar_parametro(6)

def procesar_datos(archivo,dni,salida,tipo,estado,fecha):
    lista=[] #creo lista donde voy a guardar como elemento cada row(fila) que me llega del archivo
    csv.register_dialect('dialectoCheques',delimiter=',',quoting=csv.QUOTE_ALL)#creo un dialecto en el cual digo que el delimitante de cada elemento es una coma
    archivo=open(f'{archivo}')#abro el archivo de nombre archivo 
    csvFile=csv.DictReader(archivo,dialect='dialectoCheques') #creo un lector de diccionario para mi archivo, que tenga en cuenta el "dialecto" para separar con comas

    for row in csvFile:  #para cada linea le agrego la linea correspondiente a mi lista si cumple con los filtros
        if(row['DNI']==dni and row['Tipo'].lower()==tipo and ((estado != None and row["Estado"].lower() == estado) or estado == None)):
            lista.append(dict(row))
    archivo.close()

    if salida == "pantalla":
        print(lista)
        for cheque in lista: #muestreo de datos segun la key 
            print(f"N° de cuenta de origen del cheque: {cheque['NumeroCuentaOrigen']}")
            print(f"Valor de cheque: {cheque['Valor']}")
            print(f"Fecha de emisión: {datetime.fromtimestamp(int(cheque['FechaOrigen']))}") #paso el timestamp a fecha
            print(f"Fecha de cobro de cheque: {datetime.fromtimestamp(int(cheque['FechaPago']))}")
    elif salida == "csv":
       with open(f'{dni}{datetime.timestamp(datetime.now())}.csv','w', newline='') as fi:
        fieldnames = ['NroCheque','CodigoBanco','CodigoSucursal','NumeroCuentaOrigen','NumeroCuentaDestino','Valor','FechaOrigen','FechaPago','DNI','Tipo','Estado']
        writer = csv.DictWriter(fi, delimiter=",", fieldnames=fieldnames)
        writer.writeheader()

        for cheque  in lista:
            writer.writerow ({'NumeroCuentaOrigen':cheque["NumeroCuentaOrigen"],
                           'Valor':cheque["Valor"],
                           'FechaOrigen':datetime.fromtimestamp(int(cheque['FechaOrigen'])),
                           'FechaPago':datetime.fromtimestamp(int(cheque['FechaPago']))})


if __name__=='__main__': #Entra en este if cuando apenas se ejecuta el codigo

    #sys.argv es un array donde se guaran los parametros ingresados
    if (len(sys.argv) < 5):#Si la longitud es menor a 5, significa que pasó menos de 4 parametros (sin contar sys.argv[0] que es el param con nombre del archivo py)
         print('Pasaste menos de 4 parametros, recordá que los parametros obligatorios son: nombre de archivo csv, DNI del cliente, formato de salida y tipo de cheque') 
         sys.exit(1)   
    #declaro variables estado y fecha para los parametros opcionales     
    estado = None
    fecha = None
    validacion_parametro_opcional() #me fijo si hay parametros opcionales y la función ejecutará una función para ver qué contienen
    if (len(sys.argv)>7):
        print('Ingresaste una cantidad de parametros incorrecta, acordate que podes pasar hasta 6 parametros (4 obligatorios, 2 opcionales')
    procesar_datos(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4],estado,fecha) #proceso todo lo recibido

