from asyncio.windows_events import NULL
import datetime
from dateutil.relativedelta import relativedelta

# Dummy dates
detencion1 = {"detencion":datetime.date(2010, 3, 4), "libertad":datetime.date(2010, 3, 27)}
detencion2 = {"detencion":datetime.date(2011, 5, 7), "libertad":datetime.date(2011, 7, 2)}
detencion3 = {"detencion":datetime.date(2012, 8, 25), "libertad":datetime.date(2013, 9, 19)}

class ComputoDePena():
    def __init__(self, fechaDeDetencion:datetime.date, montoDePena:dict, otrosTiemposDeDetencion=NULL):
        self._fecha_de_detencion = fechaDeDetencion
        self._monto_de_pena = montoDePena
        self._vencimiento_de_pena = datetime.date
        self._otros_tiempos_de_detencion = []
        self._computo_libertad_condicional = datetime.date
        self._requisito_libertad_condicional = {"Años":0, "Meses":0, "Días":0}
        self._computo_salidas_transitorias = datetime.date
        self._requisito_salidas_transitorias = {"Años":0, "Meses":0, "Días":0}
        self._computo_libertad_asistida_3meses = datetime.date
        self._requisito_libertad_asistida_3meses = {"Años":0, "Meses":0, "Días":0}
        self._computo_libertad_asistida_6meses = datetime.date
        self._requisito_libertad_asistida_6meses = {"Años":0, "Meses":0, "Días":0}

    def _CalcularVencimientoDePena(self):
        resultado = datetime.date
        resultado = self._fecha_de_detencion        
        resultado += relativedelta(days=self._monto_de_pena['Días'])
        resultado += relativedelta(months=self._monto_de_pena['Meses'])
        resultado += relativedelta(years=self._monto_de_pena['Años'])
        resultado += relativedelta(days=-1)
        return resultado
    
    def _CalcularLibertadCondicional(self):
        resultado_LC = self._fecha_de_detencion

        if self._monto_de_pena['Años'] < 3 or (self._monto_de_pena['Años'] == 3 and self._monto_de_pena['Meses'] == 0 and self._monto_de_pena['Días'] == 0):
            pass
        else:
            # Calcula los 2/3 de los días, lo redondea para abajo si da con coma, y los suma
            LC_dias = int((self._monto_de_pena['Días'] * 2) / 3) # Hace los dos tercios y lo redondea para abajo
            resultado_LC +=relativedelta(days=LC_dias)

            # Calcula los 2/3 de los meses
            LC_meses = self._monto_de_pena['Meses']
            LC_meses = (LC_meses * 2) / 3
            dias_resto = 0
            if LC_meses.is_integer() is False:
                dias_resto = LC_meses - int(LC_meses)
                LC_meses = int(LC_meses)
                if dias_resto > 0.3 and dias_resto < 0.4:
                    dias_resto = int(10)
                elif dias_resto > 0.6 and dias_resto < 0.7:
                    dias_resto = int(20)
                else:
                    print('ERROR: Al calcular los 2/3 de los meses, los decimales no son ni 0.3333 ni 0.6666!')
                resultado_LC +=relativedelta(days=dias_resto)
                resultado_LC +=relativedelta(months=LC_meses)
            else:
                resultado_LC +=relativedelta(months=LC_meses)

            while dias_resto >= 30:
                LC_meses += 1
                dias_resto -= 30
            LC_dias += dias_resto

            # 2/3 de los años
            LC_años_en_meses = self._monto_de_pena['Años'] * 12
            LC_años_en_meses = (LC_años_en_meses * 2) / 3
            resultado_LC +=relativedelta(months=LC_años_en_meses)

            LC_años = 0
            while LC_años_en_meses >= 12:
                LC_años_en_meses -=12
                LC_años +=1
            LC_meses += LC_años_en_meses
            if LC_meses >= 12:
                LC_meses -=12
                LC_años +=1
            
            if type(LC_años) is not int and LC_años.is_integer():
                LC_años = int(LC_años)
            if type(LC_meses) is not int and LC_meses.is_integer():
                LC_meses = int(LC_meses)
            if type(LC_dias) is not int and LC_dias.is_integer():
                LC_dias = int(LC_dias)

            resultado_LC += relativedelta(days=-1)
        return resultado_LC, {'Años': LC_años, 'Meses':LC_meses, 'Días':LC_dias}


def es_multiplo(numero, multiplo):
    return numero % multiplo == 0

def _DEBUG():    

    # Ingresar fecha de detención
    fechaDeDetencionInput = input('Ingresar fecha de detención en formato año-mes-día (XXXX/XX/XX): ')
    fechaDeDetencionInput_año = fechaDeDetencionInput[0:4]
    fechaDeDetencionInput_mes = fechaDeDetencionInput[5:7]
    fechaDeDetencionInput_dia = fechaDeDetencionInput[8:10]

    fechaDeDetencionInput = datetime.date(int(fechaDeDetencionInput_año), int(fechaDeDetencionInput_mes), int(fechaDeDetencionInput_dia))

    montoDePena = {"Años":0, "Meses":0, "Días":0}
    # Ingresar monto de pena    
    try:
        montoDePena['Años'] = int(input('Ingresar monto de pena (años): '))
    except:
        montoDePena['Años'] = 0        
    try:
        montoDePena['Meses'] = int(input('Ingresar monto de pena (meses): '))        
    except:
        montoDePena['Meses'] = 0        
    try:
        montoDePena['Días'] = int(input('Ingresar monto de pena (días): '))        
    except:
        montoDePena['Días'] = 0
    
    computo = ComputoDePena(fechaDeDetencionInput, montoDePena)

    print(computo._CalcularVencimientoDePena())
    print(computo._CalcularLibertadCondicional())

_DEBUG()


