import datetime
from dateutil.relativedelta import relativedelta
from libcalc_methods import *

def __Multiplicar_Tiempo(tiempo:TiempoEn_Años_Meses_Dias, factor:int):    
    
    tiempo.dias *= factor
    tiempo.meses *= factor
    tiempo.años *= factor

    while tiempo.dias > 30:
        tiempo.meses += 1
        tiempo.dias -= 30    
    
    while tiempo.meses >= 12:
        tiempo.años += 1
        tiempo.meses -= 12    

    return tiempo

x = __Multiplicar_Tiempo(TiempoEn_Años_Meses_Dias(3, 4, 11), 3)
print(x)
