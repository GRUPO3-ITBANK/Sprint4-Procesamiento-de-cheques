import sys
import re #libreria para trabajar con regex
import csv
from datetime import datetime

#Funcion para saber si un texto matchea con una expresion regex
def comparacion_regex(expresion,txt):
    comparacion= re.search(expresion, txt)
    coincide= True if comparacion else False
    return coincide

def convertir_mis_fechas(fecha):
    dia= int(fecha[0:2])
    mes= int(fecha[3:5])
    año= int(fecha[6:10])
    return datetime(año,mes,dia)

#Compruebo si el parametro tiene un rango de fechas o un estado de cheque
def comprobar_parametro(posicion): 
    global estado,fecha_inicio,fecha_final #Para modificar variables globales
    if(sys.argv[posicion].lower() == 'pendiente' or sys.argv[posicion].lower() == 'aprobado' or sys.argv[posicion].lower() == 'rechazado'):
        estado = sys.argv[posicion]
    elif(comparacion_regex('\d{2}-\d{2}-\d{4}:\d{2}-\d{2}-\d{4}',sys.argv[posicion])):
        fecha_inicio= convertir_mis_fechas(sys.argv[posicion][0:10])
        fecha_final = convertir_mis_fechas(sys.argv[posicion][-10:])
    else:
        print(f'No se ingresó ningún valor válido para el prametro n° {posicion}. Se omitirá este filtro. \n')
        
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
    try:
        archivo=open(f'{archivo}') 
    except:
        print("No existe el archivo solicitado")
        sys.exit()
    csvFile=csv.DictReader(archivo,dialect='dialectoCheques') #creo un lector de diccionario para mi archivo, que tenga en cuenta el "dialecto" para separar con comas

#Para cada linea hago append a lista si cumple con los filtros
    for row in csvFile:
        if (row['DNI']==dni and row['Tipo'].lower()==tipo.lower() 
        and ((estado != None and row["Estado"].lower() == estado.lower()) or estado == None) 
        and (((fecha_inicial != None and fecha_final != None) 
        and fecha_inicial < (datetime.fromtimestamp(int(row["FechaOrigen"]))) <  fecha_final) or (fecha_inicial == None and fecha_final == None))):
            if (any(r['NroCheque'] == row['NroCheque'] for r in lista)):
                print(f"Error: Número de cheque {row['NroCheque']} repetido para el DNI {dni}")
                sys.exit()
            else:
                lista.append(dict(row))
                
    archivo.close()
    if lista == []:
        print('No hay datos para los filtros seleccionados')
    else:    
        if salida.lower() == "pantalla":
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

        elif salida.lower() == "csv":
            nuevo_archivo= open(f'{dni}{datetime.timestamp(datetime.now())}.csv','w', newline='')
            campos_header = ['Numero de cuenta de origen','Valor','Fecha de origen','Fecha de pago']
            escribir = csv.DictWriter(nuevo_archivo, delimiter=":", fieldnames=campos_header)
            escribir.writeheader()

            for cheque  in lista:
                escribir.writerow ({'Numero de cuenta de origen':cheque["NumeroCuentaOrigen"],
                            'Valor':cheque["Valor"],
                            'Fecha de origen':datetime.fromtimestamp(int(cheque['FechaOrigen'])),
                            'Fecha de pago':datetime.fromtimestamp(int(cheque['FechaPago']))})
            nuevo_archivo.close()
        
#Entra en este if apenas se ejecuta el codigo
if __name__=='__main__': 

    #sys.argv es array que guara parametros ingresados por usuario
    if (len(sys.argv) < 5):
         #Si la longitud es menor a 5, significa que pasó menos de 4 parametros (sin contar sys.argv[0] que es el param con nombre del archivo py)
         print('Pasaste menos de 4 parametros, recordá que los parametros obligatorios son: nombre de archivo csv, DNI del cliente, formato de salida y tipo de cheque') 
         sys.exit(1)   
    #declaro variables estado y fecha para los parametros opcionales     
    estado = None
    fecha_inicio = None
    fecha_final = None
    validacion_parametro_opcional() 
    if (len(sys.argv)>7):
        print('Ingresaste una cantidad de parametros incorrecta, acordate que podes pasar hasta 6 parametros (4 obligatorios, 2 opcionales)')
    procesar_datos(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4],estado,fecha_inicio,fecha_final) #Proceso todo lo recibido


