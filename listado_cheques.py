import sys
import re #libreria para trabajar con regex
import csv
from datetime import datetime

#Funcion para saber si un texto matchea con una expresion regex
def comparacion_regex(expresion,txt):
    comparacion= re.search(expresion, txt)
    coincide= True if comparacion else False
    return coincide

#Funcion para convertir una fecha ingresada
def convertir_mis_fechas(fecha):
    dia= int(fecha[0:2])
    mes= int(fecha[3:5])
    año= int(fecha[6:10])
    return datetime(año,mes,dia)

#Funcion para comprobar si un parametro es una fecha o un estado de cheque
def comprobar_parametro(posicion): 
    global estado,fecha_inicio,fecha_final #Para modificar variables globales
    if(sys.argv[posicion].lower() == 'pendiente' or sys.argv[posicion].lower() == 'aprobado' or sys.argv[posicion].lower() == 'rechazado'):
        estado = sys.argv[posicion]
    elif(comparacion_regex('\d{2}-\d{2}-\d{4}:\d{2}-\d{2}-\d{4}',sys.argv[posicion])):
        fecha_inicio= convertir_mis_fechas(sys.argv[posicion][0:10])
        fecha_final = convertir_mis_fechas(sys.argv[posicion][-10:])
    else:
        print(f'No se ingresó ningún valor válido para el prametro n° {posicion}. Se omitirá este filtro. \n')


#INICIO

#CORROBORO TENER LA CANTIDAD DE PARAMETROS CORRECTA
if (len(sys.argv) < 5):
    #Si longitud es menor a 5, pasó menos de 4 parametros (sin contar sys.argv[0] que es el param con nombre del archivo py)
    print('Pasaste menos de 4 parametros, recordá que los parametros obligatorios son: nombre de archivo csv, DNI del cliente, formato de salida y tipo de cheque') 
    sys.exit()   
if (len(sys.argv)>7):
    print('Ingresaste una cantidad de parametros incorrecta, acordate que podes pasar hasta 6 parametros (4 obligatorios, 2 opcionales)')
    sys.exit()

#PARAMETROS OPCIONALES
    
estado = None
fecha_inicio = None
fecha_final = None

if (len(sys.argv)==6):
    comprobar_parametro(5)
elif (len(sys.argv)==7): 
    comprobar_parametro(5)
    comprobar_parametro(6)

#EMPIEZO A PROCESAR LOS PARAMETROS

lista=[] 
csv.register_dialect('dialectoCheques',delimiter=',',quoting=csv.QUOTE_ALL) #El delimitante de cada elemento es una coma
try:
    archivo=open(f'{sys.argv[1]}') 
except:
    print("No existe el archivo solicitado")
    sys.exit()
csvFile=csv.DictReader(archivo,dialect='dialectoCheques') #creo un lector de diccionario para mi archivo, que tenga en cuenta el "dialecto" para separar con comas

#FILTRO LOS DATOS 

for row in csvFile:
    if (row['DNI']==sys.argv[2] and row['Tipo'].lower()==sys.argv[4].lower() 
    and ((estado != None and row["Estado"].lower() == estado.lower()) or estado == None) 
    and (((fecha_inicio != None and fecha_final != None) 
    and fecha_inicio < (datetime.fromtimestamp(int(row["FechaOrigen"]))) <  fecha_final) or (fecha_inicio == None and fecha_final == None))):
        if (any(r['NroCheque'] == row['NroCheque'] for r in lista)):
            print(f"Error: Número de cheque {row['NroCheque']} repetido para el DNI {sys.argv[2]}")
            sys.exit()
        else:
            lista.append(dict(row))            
archivo.close()

 # MUESTREO DE DATOS

if lista == []:
    print('No hay datos para los filtros seleccionados')
else:              
    if sys.argv[3].lower() == "pantalla":
        for cheque in lista: #Muestreo de datos segun la key 
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

    elif sys.argv[3].lower() == "csv":
        nuevo_archivo= open(f'{sys.argv[2]}{datetime.timestamp(datetime.now())}.csv','w', newline='')
        campos_header = ['Num. Cta. Origen','Valor','Fecha de origen','Fecha de pago']
        escribir = csv.DictWriter(nuevo_archivo, delimiter=",", fieldnames=campos_header)
        escribir.writeheader()
        for cheque  in lista:
            escribir.writerow ({'Num. Cta. Origen':cheque["NumeroCuentaOrigen"],
                        'Valor':cheque["Valor"],
                        'Fecha de origen':datetime.fromtimestamp(int(cheque['FechaOrigen'])),
                        'Fecha de pago':datetime.fromtimestamp(int(cheque['FechaPago']))})
        nuevo_archivo.close()