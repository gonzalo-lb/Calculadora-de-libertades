from asyncio.windows_events import NULL
import datetime
from dateutil.relativedelta import relativedelta

# Dummy dates
detencion1 = {"detencion":datetime.date(2010, 3, 4), "libertad":datetime.date(2010, 3, 27)}
detencion2 = {"detencion":datetime.date(2011, 5, 7), "libertad":datetime.date(2011, 7, 2)}
detencion3 = {"detencion":datetime.date(2012, 8, 25), "libertad":datetime.date(2013, 9, 19)}

class TiempoEnAños_Meses_Dias():
    def __init__(self):
        self.años = 0
        self.meses = 0
        self.dias = 0
    
    def __str__(self):
        return '...{} año(s), {} mes(es) y {} día(s)...'.format(self.años, self.meses, self.dias)

class ComputoDePena():
    def __init__(self, fechaDeDetencion:datetime.date, montoDePena:TiempoEnAños_Meses_Dias, otrosTiemposDeDetencion=NULL):
        self._fecha_de_detencion = fechaDeDetencion
        self._monto_de_pena = montoDePena
        self._vencimiento_de_pena = datetime.date
        self._otros_tiempos_de_detencion = []
        self._computo_libertad_condicional = datetime.date
        self._requisito_libertad_condicional = TiempoEnAños_Meses_Dias()
        self._computo_salidas_transitorias = datetime.date
        self._requisito_salidas_transitorias = TiempoEnAños_Meses_Dias()
        self._computo_libertad_asistida_3meses = datetime.date
        self._requisito_libertad_asistida_3meses = TiempoEnAños_Meses_Dias()
        self._computo_libertad_asistida_6meses = datetime.date
        self._requisito_libertad_asistida_6meses = TiempoEnAños_Meses_Dias()

        # Luego tiene que hacer todos los cálculos
        self._CalcularVencimientoDePena()
        self._CalcularLibertadCondicional()

    def _CalcularVencimientoDePena(self):
        self._vencimiento_de_pena = datetime.date
        self._vencimiento_de_pena = self._fecha_de_detencion        
        self._vencimiento_de_pena += relativedelta(days=self._monto_de_pena.dias)
        self._vencimiento_de_pena += relativedelta(months=self._monto_de_pena.meses)
        self._vencimiento_de_pena += relativedelta(years=self._monto_de_pena.años)
        self._vencimiento_de_pena += relativedelta(days=-1)        
    
    def _CalcularLibertadCondicional(self):
        self._computo_libertad_condicional = self._fecha_de_detencion

        if self._monto_de_pena.años < 3 or (self._monto_de_pena.años == 3 and self._monto_de_pena.meses == 0 and self._monto_de_pena.dias == 0):
            pass # Falta hacer esta parte
        else:
            # Calcula los 2/3 de los días, lo redondea para abajo si da con coma, y los suma
            self._requisito_libertad_condicional.dias = int((self._monto_de_pena.dias * 2) / 3) # Hace los dos tercios y lo redondea para abajo
            self._computo_libertad_condicional +=relativedelta(days=self._requisito_libertad_condicional.dias)

            # Calcula los 2/3 de los meses
            self._requisito_libertad_condicional.meses = self._monto_de_pena.meses
            self._requisito_libertad_condicional.meses = (self._requisito_libertad_condicional.meses * 2) / 3
            dias_resto = 0
            if self._requisito_libertad_condicional.meses.is_integer() is False:
                dias_resto = self._requisito_libertad_condicional.meses - int(self._requisito_libertad_condicional.meses)
                self._requisito_libertad_condicional.meses = int(self._requisito_libertad_condicional.meses)
                if dias_resto > 0.3 and dias_resto < 0.4:
                    dias_resto = int(10)
                elif dias_resto > 0.6 and dias_resto < 0.7:
                    dias_resto = int(20)
                else:
                    print('ERROR: Al calcular los 2/3 de los meses, los decimales no son ni 0.3333 ni 0.6666!')
                self._computo_libertad_condicional +=relativedelta(days=dias_resto)
                self._computo_libertad_condicional +=relativedelta(months=self._requisito_libertad_condicional.meses)
            else:
                self._computo_libertad_condicional +=relativedelta(months=self._requisito_libertad_condicional.meses)

            while dias_resto >= 30:
                self._requisito_libertad_condicional.meses += 1
                dias_resto -= 30
            self._requisito_libertad_condicional.dias += dias_resto

            # 2/3 de los años
            LC_años_en_meses = self._monto_de_pena.años * 12
            LC_años_en_meses = (LC_años_en_meses * 2) / 3
            self._computo_libertad_condicional +=relativedelta(months=LC_años_en_meses)

            self._requisito_libertad_condicional.años = 0
            while LC_años_en_meses >= 12:
                LC_años_en_meses -=12
                self._requisito_libertad_condicional.años +=1
            self._requisito_libertad_condicional.meses += LC_años_en_meses
            if self._requisito_libertad_condicional.meses >= 12:
                self._requisito_libertad_condicional.meses -=12
                self._requisito_libertad_condicional.años +=1
            
            if type(self._requisito_libertad_condicional.años) is not int and self._requisito_libertad_condicional.años.is_integer():
                self._requisito_libertad_condicional.años = int(self._requisito_libertad_condicional.años)
            if type(self._requisito_libertad_condicional.meses) is not int and self._requisito_libertad_condicional.meses.is_integer():
                self._requisito_libertad_condicional.meses = int(self._requisito_libertad_condicional.meses)
            if type(self._requisito_libertad_condicional.dias) is not int and self._requisito_libertad_condicional.dias.is_integer():
                self._requisito_libertad_condicional.dias = int(self._requisito_libertad_condicional.dias)

            self._computo_libertad_condicional += relativedelta(days=-1)

def es_multiplo(numero, multiplo):
    return numero % multiplo == 0

def _DEBUG():    

    # Ingresar fecha de detención
    fechaDeDetencionInput = input('Ingresar fecha de detención en formato año-mes-día (XXXX/XX/XX): ')
    fechaDeDetencionInput_año = fechaDeDetencionInput[0:4]
    fechaDeDetencionInput_mes = fechaDeDetencionInput[5:7]
    fechaDeDetencionInput_dia = fechaDeDetencionInput[8:10]

    fechaDeDetencionInput = datetime.date(int(fechaDeDetencionInput_año), int(fechaDeDetencionInput_mes), int(fechaDeDetencionInput_dia))

    montoDePena = TiempoEnAños_Meses_Dias()
    # Ingresar monto de pena    
    try:
        montoDePena.años = int(input('Ingresar monto de pena (años): '))
    except:
        montoDePena.años = 0        
    try:
        montoDePena.meses = int(input('Ingresar monto de pena (meses): '))        
    except:
        montoDePena.meses = 0        
    try:
        montoDePena.dias = int(input('Ingresar monto de pena (días): '))        
    except:
        montoDePena.dias = 0
    
    computo = ComputoDePena(fechaDeDetencionInput, montoDePena)    

    print(computo._vencimiento_de_pena)
    print(computo._computo_libertad_condicional)
    print(computo._requisito_libertad_condicional)

_DEBUG()


