import datetime
from dateutil.relativedelta import relativedelta
from libcalc_methods import *

def __Calcular_dos_tercios(_montoDePena:MontoDePena):

        if _montoDePena.perpetua:
            return _montoDePena
        
        TR_dos_tercios = MontoDePena()

        # Calcula 1/3 de los días, lo redondea para abajo si da con coma, y los suma
        TR_dos_tercios.dias = int(_montoDePena.dias / 3) # Hace los dos tercios y lo redondea para abajo        

        # Calcula los 1/3 de los meses
        TR_dos_tercios.meses = _montoDePena.meses
        TR_dos_tercios.meses = TR_dos_tercios.meses / 3
        LC_dias_resto = 0
        if TR_dos_tercios.meses.is_integer() is False:
            LC_dias_resto = TR_dos_tercios.meses - int(TR_dos_tercios.meses)
            TR_dos_tercios.meses = int(TR_dos_tercios.meses)
            if LC_dias_resto > 0.3 and LC_dias_resto < 0.4:
                LC_dias_resto = int(10)
            elif LC_dias_resto > 0.6 and LC_dias_resto < 0.7:
                LC_dias_resto = int(20)
            else:
                print('ERROR: Al calcular los 2/3 de los meses, los decimales no son ni 0.3333 ni 0.6666!')                    

        while LC_dias_resto >= 30:
            TR_dos_tercios.meses += 1
            LC_dias_resto -= 30
        TR_dos_tercios.dias += LC_dias_resto

        # 1/3 de los años
        LC_años_en_meses = _montoDePena.años * 12
        LC_años_en_meses = LC_años_en_meses  / 3        

        TR_dos_tercios.años = 0
        while LC_años_en_meses >= 12:
            LC_años_en_meses -=12
            TR_dos_tercios.años +=1
        TR_dos_tercios.meses += LC_años_en_meses
        if TR_dos_tercios.meses >= 12:
            TR_dos_tercios.meses -=12
            TR_dos_tercios.años +=1
        
        if type(TR_dos_tercios.años) is not int and TR_dos_tercios.años.is_integer():
            TR_dos_tercios.años = int(TR_dos_tercios.años)
        if type(TR_dos_tercios.meses) is not int and TR_dos_tercios.meses.is_integer():
            TR_dos_tercios.meses = int(TR_dos_tercios.meses)
        if type(TR_dos_tercios.dias) is not int and TR_dos_tercios.dias.is_integer():
            TR_dos_tercios.dias = int(TR_dos_tercios.dias)        

        return TR_dos_tercios # MontoDePena()

mpena = MontoDePena(_años=4)
print(__Calcular_dos_tercios(mpena))