import sys
import re # importo para hacer expresiones regex
import csv
from datetime import datetime
from csv import writer


expresion_regex_fecha= '\d{2}-\d{2}-\d{4}:\d{2}-\d{2}-\d{4}'#expresion regex de fecha

def comparacion_regex(expresion,txt):#funcion que sirve para saber si un texto matchea con el regex
    comparacion= re.search(expresion, txt)
    coincide= True if comparacion else False
    return coincide

def validacion_parametro_opcional(parametro,posicion):
        if(parametro.lower() == 'pendiente' or parametro.lower() == 'aprobado' or parametro.lower() == 'rechazado'):
            print('se trata de un cheque')
        elif(comparacion_regex(expresion_regex_fecha,parametro)):
            print('es una fecha')   
        else:
            print(f'no se ingresó ningún parametro válido para el prametro n° {posicion}')

def procesar_datos(dni,salida,tipo):
    lista=[] #creo lista donde voy a guardar como elemento cada row(fila) que me llega del archivo
    csv.register_dialect('dialectoCheques',delimiter=',',quoting=csv.QUOTE_ALL)#creo un dialecto en el cual digo que el delimitante de cada elemento es una coma
    file=open('archivo.csv')#abro el archivo de nombre archivo tipo csv
    csvFile=csv.DictReader(file,dialect='dialectoCheques') #creo un lector de diccionario para mi archivo, que tenga en cuenta el "dialecto" para separar con comas

    for row in csvFile:  #para cada linea le agrego la linea correspondiente a mi lista 
            if(row['DNI']==dni and (row['Tipo']).lower()==tipo):
                lista.append(dict(row))
    file.close()#cierro archivo

    if salida == "pantalla":
        print(lista)
        for cheque in lista: #muestreo de datos segun la key 
            print(f"--------DNI: {cheque['DNI']}-------- ")
            print(f"N° de cheque: {cheque['NroCheque']}")
            print(f"Código de banco: {cheque['CodigoBanco']}")
            print(f"N° de cuenta de origen del cheque: {cheque['NumeroCuentaOrigen']}")
            print(f"N° de cuenta de destino: {cheque['NumeroCuentaDestino']}")
            print(f"Valor de cheque: {cheque['Valor']}")
            print(f"Fecha de emisión: {datetime.fromtimestamp(int(cheque['FechaOrigen']))}") #paso el timestamp a fecha
            print(f"Fecha de cobro de cheque: {datetime.fromtimestamp(int(cheque['FechaPago']))}")
            print(f"Tipo de cheque: {cheque['Tipo']}")
            print(f"Estado de cheque:{ cheque['Estado']}")
    elif salida == "csv":
       with open(f'{dni}{datetime.timestamp(datetime.now())}.csv','w', newline='') as fi:
        fieldnames = ['NroCheque','CodigoBanco','CodigoSucursal','NumeroCuentaOrigen','NumeroCuentaDestino','Valor','FechaOrigen','FechaPago','DNI','Tipo','Estado']
        writer = csv.DictWriter(fi, delimiter=",", fieldnames=fieldnames)
        writer.writeheader()

        for cheque  in lista:
            writer.writerow ({'NroCheque':cheque["NroCheque"],
                            'CodigoBanco':cheque["CodigoBanco"],
                            'CodigoSucursal':cheque["CodigoSucursal"],
                            'NumeroCuentaOrigen':cheque["NumeroCuentaOrigen"],
                            'NumeroCuentaDestino':cheque["NumeroCuentaDestino"],
                            'Valor':cheque["Valor"],
                            'FechaOrigen':datetime.fromtimestamp(int(cheque['FechaOrigen'])),
                            'FechaPago':datetime.fromtimestamp(int(cheque['FechaPago'])),
                            'DNI':cheque["DNI"],
                            'Tipo':cheque["Tipo"],
                            'Estado':cheque["Estado"]})


if __name__=='__main__': #Entra en este if cuando apenas se ejecuta el codigo
    #sys.argv es un array donde se guaran los parametros ingresados en consola, (sys.argv[0]) si o si siempre debe ser el nombre del archivo py, por eso en lo que muestro no lo tengo en cuenta
    if (len(sys.argv) < 5):# Quiero minimo 4 parametros, la longitud es 5 porque tambien está el sys.argv[0]
         print('Pasaste menos de 4 parametros, recordá que los parametros obligatorios son: nombre de archivo csv, DNI del cliente, formato de salida y tipo de cheque') 
         sys.exit(1)   
    archivo = sys.argv[1]
    dni = sys.argv[2]
    salida = sys.argv[3]
    tipo_cheque = sys.argv[4]

    
    if (len(sys.argv) ==5): #cuando se ingresan la cantidad de parametros obligatorios(4), 
        print("Están bien los parámetros")
        procesar_datos(dni,salida,tipo_cheque)
    elif len(sys.argv)==6:#hay un quinto parametro, el ultimo parametro es opcional
        parametro_opcional_1 = sys.argv[5]
        validacion_parametro_opcional(parametro_opcional_1,5)    
    elif(len(sys.argv)==7):#hay un sexto parametro, los dos ultimos parametros son opcionales
        parametro_opcional_1 = sys.argv[5]
        parametro_opcional_2 = sys.argv[6]   
        validacion_parametro_opcional(parametro_opcional_1,5)
        validacion_parametro_opcional(parametro_opcional_2,6)
        
    elif(len(sys.argv)>7):
        print('Ingresaste una cantidad de parametros incorrecta, acordate que podes pasar hasta 6 parametros (4 obligatorios, 2 opcionales')
