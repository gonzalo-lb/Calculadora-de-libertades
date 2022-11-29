import datetime
from libcalc_methods import *

def Comparar_fechas_y_devolver_la_mayor(*fechas):
    TRET = True
    for fecha in fechas:
        if type(fecha) is datetime.date:
            TRET = fecha
            break
    if TRET == True:
        print('Comparar_fechas_y_devolver_la_mayor: NINGUNA DE LOS PARÁMETROS INGRESADOS ES UNA FECHA. NO SE REALIZÓ LA COMPARACIÓN.')
        return
    
    for fecha in fechas:
        if type(fecha) is datetime.date:
            if FechaA_es_Mayor_Que_FechaB(fecha, TRET):
                TRET = fecha
    return TRET


# a = datetime.date(2050, 1, 1)
# b = datetime.date(2040, 1, 1)
# c = datetime.date(2030, 1, 1)

a = 'datetime.date(2050, 1, 1)'
b = 'datetime.date(2040, 1, 1)'
c = datetime.date(2080, 1, 1)
d = datetime.date(2060, 1, 1)
e = datetime.date(2030, 1, 1)

# a = 12
# b = 'sdhjbf'
# c = False

print(Comparar_fechas_y_devolver_la_mayor(a, b, c, d, e))