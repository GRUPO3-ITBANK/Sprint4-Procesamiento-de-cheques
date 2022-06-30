import csv
from datetime import datetime
lista=[] #creo lista donde voy a guardar como elemento cada row(fila) que me llega del archivo
csv.register_dialect('dialectoCheques',delimiter=',',quoting=csv.QUOTE_ALL)#creo un dialecto en el cual digo que el delimitante de cada elemento es una coma

file=open('archivo.csv')#abro el archivo de nombre archivo tipo csv
csvFile=csv.DictReader(file,dialect='dialectoCheques') #creo un lector de diccionario para mi archivo, que tenga en cuenta el "dialecto" para separar con comas

for row in csvFile:  #para cada linea le agrego la linea correspondiente a mi lista 
    lista.append(dict(row))
file.close()#cierro archivo



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
