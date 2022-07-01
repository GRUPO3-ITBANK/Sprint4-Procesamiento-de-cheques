import getopt
import sys
import re # importo para hacer expresiones regex

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


if __name__=='__main__': #Entra en este if cuando apenas se ejecuta el codigo
    #sys.argv es un array donde se guaran los parametros ingresados en consola, (sys.argv[0]) si o si siempre debe ser el nombre del archivo py, por eso en lo que muestro no lo tengo en cuenta
    if len(sys.argv) < 5:# Quiero minimo 4 parametros, la longitud es 5 porque tambien está el sys.argv[0]
         print('Pasaste menos de 4 parametros, recordá que los parametros obligatorios son: nombre de archivo csv, DNI del cliente, formato de salida y tipo de cheque')
         sys.exit(1) 

    elif len(sys.argv) ==5: #cuando se ingresan la cantidad de parametros obligatorios(4), 
        archivo = sys.argv[1]
        dni = sys.argv[2]
        salida = sys.argv[3]
        tipo_cheque = sys.argv[4]

    elif(len(sys.argv)==6):#hay un quinto parametro, el ultimo parametro es opcional
        parametro_opcional_1 = sys.argv[5]
        validacion_parametro_opcional(parametro_opcional_1,5)
    elif(len(sys.argv)==7):#hay un sexto parametro, los dos ultimos parametros son opcionales
        paramOpcional2 = sys.argv[6]

    elif(len(sys.argv)>7):
        print('Ingresaste una cantidad de parametros incorrecta, acordate que podes pasar hasta 6 parametros (4 obligatorios, 2 opcionales')


def filtrado_obligatorio():
    print('Filtrar por DNI')