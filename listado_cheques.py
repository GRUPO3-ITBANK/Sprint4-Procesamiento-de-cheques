import sys
import re
import csv
from datetime import datetime


#Expresion regex de rango de fechas recibidas
expresion_regex_fecha= '\d{2}-\d{2}-\d{4}:\d{2}-\d{2}-\d{4}'

#Funcion para saber si un texto matchea con una expresion regex
def comparacion_regex(expresion,txt):
    comparacion= re.search(expresion, txt)
    coincide= True if comparacion else False
    return coincide

#Funcion para saber si el parametro tiene un rango de fechas o un estado de cheque
def comprobar_parametro(posicion): 
    global estado,fecha_inicio,fecha_final #Para modificar variables globales
    if(sys.argv[posicion].lower() == 'pendiente' or sys.argv[posicion].lower() == 'aprobado' or sys.argv[posicion].lower() == 'rechazado'):
        estado = sys.argv[posicion]
    elif(comparacion_regex(expresion_regex_fecha,sys.argv[posicion])):
        mi_formato_fecha = "%d-%m-%y"
        fecha_final = datetime.strptime(sys.argv[posicion][-10:], mi_formato_fecha)
        fecha_inicio = datetime.timestamp(datetime.strptime(sys.argv[posicion][0:10], mi_formato_fecha))
        print(fecha_final)
    else:
        print(f'no se ingresó ningún valor válido para el prametro n° {posicion}')
        
#Funcion para saber si hay uno o dos parametros opcionales
def validacion_parametro_opcional():  
    if (len(sys.argv)==6):
        comprobar_parametro(5)
    elif (len(sys.argv)==7): 
        comprobar_parametro(5)
        comprobar_parametro(6)

#Lista donde voy a guardar cada row(fila) que me llega del archivo
def procesar_datos(archivo,dni,salida,tipo,estado,fecha_inicial,fecha_final):
    lista=[] 
    csv.register_dialect('dialectoCheques',delimiter=',',quoting=csv.QUOTE_ALL) #El delimitante de cada elemento es una coma
    archivo=open(f'{archivo}') #abro el archivo de nombre archivo 
    csvFile=csv.DictReader(archivo,dialect='dialectoCheques') #creo un lector de diccionario para mi archivo, que tenga en cuenta el "dialecto" para separar con comas

#Para cada linea le agrego la linea correspondiente a mi lista si cumple con los filtros
    for row in csvFile:
        if (row['DNI']==dni and row['Tipo'].lower()==tipo 
        and ((estado != None and row["Estado"].lower() == estado) or estado == None) 
        and (((fecha_inicial != None and fecha_final != None) 
        and fecha_inicial < datetime.fromtimestamp(int(row["FechaOrigen"]).date() <  fecha_final) or (fecha_inicial == None and fecha_final != None)))):
            lista.append(dict(row))

    archivo.close()

    if salida == "pantalla":
        for cheque in lista: #Muestreo de datos segun la key 
            print(f"N° de cuenta de origen del cheque: {cheque['NumeroCuentaOrigen']}")
            print(f"Valor de cheque: {cheque['Valor']}")
            print(f"Fecha de emisión: {datetime.fromtimestamp(int(cheque['FechaOrigen']))}") #Paso el timestamp a fecha
            print(f"Fecha de cobro de cheque: {datetime.fromtimestamp(int(cheque['FechaPago']))}")

    elif salida == "csv":
        nuevo_archivo= open(f'{dni}{datetime.timestamp(datetime.now())}.csv','w', newline='')
        campos_header = ['NumeroCuentaOrigen','Valor','FechaOrigen','FechaPago']
        escribir = csv.DictWriter(nuevo_archivo, delimiter=",", fieldnames=campos_header)
        escribir.writeheader()

        for cheque  in lista:
            escribir.writerow ({'NumeroCuentaOrigen':cheque["NumeroCuentaOrigen"],
                           'Valor':cheque["Valor"],
                           'FechaOrigen':datetime.fromtimestamp(int(cheque['FechaOrigen'])),
                           'FechaPago':datetime.fromtimestamp(int(cheque['FechaPago']))})
        nuevo_archivo.close()
        
#Entra en este if cuando apenas se ejecuta el codigo
if __name__=='__main__': 

    #sys.argv es un array donde se guaran los parametros ingresados
    if (len(sys.argv) < 5):
         #Si la longitud es menor a 5, significa que pasó menos de 4 parametros (sin contar sys.argv[0] que es el param con nombre del archivo py)
         print('Pasaste menos de 4 parametros, recordá que los parametros obligatorios son: nombre de archivo csv, DNI del cliente, formato de salida y tipo de cheque') 
         sys.exit(1)   
    #declaro variables estado y fecha para los parametros opcionales     
    estado = None
    fecha_inicio = None
    fecha_final = None

    #funcion para saber si hay parametros opcionales y se ejecutará una función para ver qué contienen
    validacion_parametro_opcional() 
    if (len(sys.argv)>7):
        print('Ingresaste una cantidad de parametros incorrecta, acordate que podes pasar hasta 6 parametros (4 obligatorios, 2 opcionales')
    procesar_datos(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4],estado,fecha_inicio,fecha_final) #Proceso todo lo recibido


