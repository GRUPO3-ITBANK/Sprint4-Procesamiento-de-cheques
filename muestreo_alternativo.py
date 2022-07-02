import csv
import argparse
from datetime import datetime

parser = argparse.ArgumentParser()
parser.add_argument("-n", "--nombreArchivo", dest="nombreArchivo", help = "Nombre de archivo a guardar", required=True)
parser.add_argument("-d", "--dniPersona", dest="dniPersona", help = "DNI de la persona", required=True)
grupoSalidas = parser.add_mutually_exclusive_group(required=True)
grupoSalidas.add_argument("-p", "--pantalla", dest="pantalla", action='store_true', help = "Salida en pantalla")
grupoSalidas.add_argument("-c", "--csv", dest="csv", action='store_true', help = "Salida en archivo CSV")
grupoTipos = parser.add_mutually_exclusive_group(required=True)
grupoTipos.add_argument("-em", "--emitido", dest="emitido", action='store_true', help = "Tipo de cheque emitido")
grupoTipos.add_argument("-de", "--depositado", dest="depositado", action='store_true', help = "Tipo de cheque depositado")
grupoEstados = parser.add_mutually_exclusive_group()
grupoEstados.add_argument("-pe", "--pendiente", dest="pendiente", action='store_true', help = "Estado de cheque pendiente")
grupoEstados.add_argument("-ap", "--aprobado", dest="aprobado", action='store_true', help = "Estado de cheque aprobado")
grupoEstados.add_argument("-re", "--rechazado", dest="rechazado", action='store_true', help = "Estado de cheque rechazado")
# parser.add_argument("-r", "--rangoFecha", dest="rangoFecha", help = "Rango de fechas a filtrar")
args = parser.parse_args()

lista=[]
nombreArchivo = args.nombreArchivo
dni = int(args.dniPersona)
salidaPantalla = args.pantalla
chequeEmitido = "EMITIDO" if args.emitido else "DEPOSITADO"
estadoCheque = "PENDIENTE" if args.pendiente else "APROBADO" if args.aprobado else "RECHAZADO" if args.rechazado else None

csv.register_dialect('dialectoCheques', delimiter=',', quoting=csv.QUOTE_ALL)
with open(nombreArchivo, 'r') as file:
    csv_file = csv.DictReader(file, dialect='dialectoCheques')
    for row in csv_file:
        if (int(row["DNI"]) == dni and row["Tipo"] == chequeEmitido and ((estadoCheque != None and row["Estado"] == estadoCheque) or (estadoCheque == None))):
            lista.append(dict(row))
        
file.close()

if salidaPantalla:
    print("----------------  DATOS DE DNI",dni," ----------------")
    for cheque in lista:
        print("Numero de cheque:",cheque["NroCheque"])
        print("Codigo del banco:",cheque["CodigoBanco"])
        print("Codigo de la sucursal:",cheque["CodigoSucursal"])
        print("Nro. cta. destino:",cheque["NumeroCuentaOrigen"])
        print("Nro. cta. origen:",cheque["NumeroCuentaDestino"])
        print("Valor:",cheque["Valor"])
        print("Fecha de origen:",cheque["FechaOrigen"])
        print("Fecha de pago:",cheque["FechaPago"])
        print("DNI:",cheque["DNI"])
        print("Tipo:",cheque["Tipo"])
        print("Estado:",cheque["Estado"])
        print("-------------------------------------------------------")
else:
    with open(f'{dni}{datetime.timestamp(datetime.now())}.csv', 'w', newline='') as fi:
        fieldnames = ['NroCheque','CodigoBanco','CodigoSucursal','NumeroCuentaOrigen','NumeroCuentaDestino','Valor','FechaOrigen','FechaPago','DNI','Tipo','Estado']
        writer = csv.DictWriter(fi, delimiter=",", fieldnames=fieldnames)
        writer.writeheader()

        for cheque in lista:
            writer.writerow({'NroCheque': cheque["NroCheque"],
                            'CodigoBanco':cheque["CodigoBanco"],
                            'CodigoSucursal':cheque["CodigoSucursal"],
                            'NumeroCuentaOrigen':cheque["NumeroCuentaOrigen"],
                            'NumeroCuentaDestino':cheque["NumeroCuentaDestino"], 
                            'Valor':cheque["Valor"],
                            'FechaOrigen':datetime.fromtimestamp(int(cheque["FechaOrigen"])),
                            'FechaPago':datetime.fromtimestamp(int(cheque["FechaPago"])),
                            'DNI':cheque["DNI"],
                            'Tipo':cheque["Tipo"],
                            'Estado':cheque["Estado"]})
        