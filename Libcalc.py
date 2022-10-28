import datetime
from dateutil.relativedelta import relativedelta
from libcalc_methods import *

class ComputoDePena():
    
    def __init__(self, fechaDeDetencion:datetime.date, montoDePena:TiempoEnAños_Meses_Dias, otrosTiemposDeDetencion='NULL'):
        self._fecha_de_detencion = fechaDeDetencion
        self._monto_de_pena = montoDePena
        self._vencimiento_de_pena = datetime.date
        self._vencimiento_de_pena_sinRestarOtrasDetenciones = datetime.date
        self._otros_tiempos_de_detencion = otrosTiemposDeDetencion
        self._computo_libertad_condicional = datetime.date
        self._computo_libertad_condicional_sinRestarOtrasDetenciones = datetime.date
        self._requisito_libertad_condicional = TiempoEnAños_Meses_Dias()
        self._computo_salidas_transitorias = datetime.date
        self._computo_salidas_transitorias_sinRestarOtrasDetenciones = datetime.date
        self._requisito_salidas_transitorias = TiempoEnAños_Meses_Dias()
        self._computo_libertad_asistida_3meses = datetime.date
        self._computo_libertad_asistida_3meses_sinRestarOtrasDetenciones = datetime.date
        self._requisito_libertad_asistida_3meses = TiempoEnAños_Meses_Dias()
        self._computo_libertad_asistida_6meses = datetime.date
        self._computo_libertad_asistida_6meses_sinRestarOtrasDetenciones = datetime.date
        self._requisito_libertad_asistida_6meses = TiempoEnAños_Meses_Dias()        

        # Luego tiene que hacer todos los cálculos
        self.__CalcularVencimientoDePena()
        self.__CalcularLibertadCondicional()
        self.__CalcularSalidasTransitorias()
        self.__CalcularLibertadAsistida_3meses()
        self.__CalcularLibertadAsistida_6meses()                

    def __CalcularVencimientoDePena(self):

        self._vencimiento_de_pena = datetime.date
        self._vencimiento_de_pena = self._fecha_de_detencion        
        self._vencimiento_de_pena += relativedelta(days=self._monto_de_pena.dias)
        self._vencimiento_de_pena += relativedelta(months=self._monto_de_pena.meses)
        self._vencimiento_de_pena += relativedelta(years=self._monto_de_pena.años)
        self._vencimiento_de_pena += relativedelta(days=-1)
        self._vencimiento_de_pena_sinRestarOtrasDetenciones = self._vencimiento_de_pena
        if self._otros_tiempos_de_detencion != "NULL":
            self._vencimiento_de_pena = RestarOtrasDetenciones(self._vencimiento_de_pena, self._otros_tiempos_de_detencion)
    
    def __CalcularLibertadCondicional(self):

        self._computo_libertad_condicional = self._fecha_de_detencion

        if self._monto_de_pena.años < 3 or (self._monto_de_pena.años == 3 and self._monto_de_pena.meses == 0 and self._monto_de_pena.dias == 0):
            self._requisito_libertad_condicional.años = 0
            self._requisito_libertad_condicional.meses = 8
            self._requisito_libertad_condicional.dias = 0
            self._fecha_de_detencion += relativedelta(months=8)
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

            self._computo_libertad_condicional_sinRestarOtrasDetenciones = self._computo_libertad_condicional            
            if self._otros_tiempos_de_detencion != "NULL":
                self._computo_libertad_condicional = RestarOtrasDetenciones(self._computo_libertad_condicional, self._otros_tiempos_de_detencion)

    def __CalcularSalidasTransitorias(self):
        self._computo_salidas_transitorias = self._fecha_de_detencion        

        # Calcula la mitad de los días lo redondea para abajo si da con coma, y los suma
        self._requisito_salidas_transitorias.dias = int(self._monto_de_pena.dias / 2) # Hace la mitad y lo redondea para abajo
        self._computo_salidas_transitorias +=relativedelta(days=self._requisito_salidas_transitorias.dias)

        # Calcula la mitad de los meses
        self._requisito_salidas_transitorias.meses = self._monto_de_pena.meses
        ST_dias_resto = 0
        if self._requisito_salidas_transitorias.meses == 1:
            self._requisito_salidas_transitorias.meses = 0
            ST_dias_resto = int(15)
        elif self._requisito_salidas_transitorias.meses > 1:
            if es_multiplo(self._requisito_salidas_transitorias.meses, 2):
                self._requisito_salidas_transitorias.meses /= 2
            else:
                self._requisito_salidas_transitorias.meses = self._monto_de_pena.meses/2
                self._requisito_salidas_transitorias.meses = int(self._requisito_salidas_transitorias.meses)        
                ST_dias_resto = int(15)

        self._computo_salidas_transitorias += relativedelta(months=self._requisito_salidas_transitorias.meses)
        self._computo_salidas_transitorias += relativedelta(days=ST_dias_resto)

        # Calcula la mitad de los años
        self._requisito_salidas_transitorias.años = self._monto_de_pena.años
        ST_meses_resto = 0
        if self._requisito_salidas_transitorias.años == 1:
            self._requisito_salidas_transitorias.años = 0
            ST_meses_resto = int(6)
        elif self._requisito_salidas_transitorias.años > 1:
            if es_multiplo(self._requisito_salidas_transitorias.años, 2):
                self._requisito_salidas_transitorias.años /= 2
            else:
                self._requisito_salidas_transitorias.años /= 2
                self._requisito_salidas_transitorias.años = int(self._requisito_salidas_transitorias.años)
                ST_meses_resto = int(6)

        self._computo_salidas_transitorias += relativedelta(years=self._requisito_salidas_transitorias.años)
        self._computo_salidas_transitorias += relativedelta(months=ST_meses_resto)

        self._computo_salidas_transitorias += relativedelta(days=-1)

        # Resta las otras detenciones, si hay
        self._computo_salidas_transitorias_sinRestarOtrasDetenciones = self._computo_salidas_transitorias
        if self._otros_tiempos_de_detencion != "NULL":
            self._computo_salidas_transitorias = RestarOtrasDetenciones(self._computo_salidas_transitorias, self._otros_tiempos_de_detencion)

        # Se ajustan los resultados para que no tengan decimales
        if type(self._requisito_salidas_transitorias.años) is not int and self._requisito_salidas_transitorias.años.is_integer():
            self._requisito_salidas_transitorias.años = int(self._requisito_salidas_transitorias.años)
        if type(self._requisito_salidas_transitorias.meses) is not int and self._requisito_salidas_transitorias.meses.is_integer():
            self._requisito_salidas_transitorias.meses = int(self._requisito_salidas_transitorias.meses)
        if type(self._requisito_salidas_transitorias.dias) is not int and self._requisito_salidas_transitorias.dias.is_integer():
            self._requisito_salidas_transitorias.dias = int(self._requisito_salidas_transitorias.dias)

    def __CalcularLibertadAsistida_3meses(self):
        
        self._computo_libertad_asistida_3meses = self._vencimiento_de_pena
        self._computo_libertad_asistida_3meses += relativedelta(months=-3)

        self._computo_libertad_asistida_3meses_sinRestarOtrasDetenciones = self._computo_libertad_asistida_3meses
        if self._otros_tiempos_de_detencion != "NULL":
            self._computo_libertad_asistida_3meses = RestarOtrasDetenciones(self._computo_libertad_asistida_3meses, self._otros_tiempos_de_detencion)
        
    def __CalcularLibertadAsistida_6meses(self):
        self._computo_libertad_asistida_6meses = self._vencimiento_de_pena
        self._computo_libertad_asistida_6meses += relativedelta(months=-6)

        self._computo_libertad_asistida_6meses_sinRestarOtrasDetenciones = self._computo_libertad_asistida_6meses
        if self._otros_tiempos_de_detencion != "NULL":
            self._computo_libertad_asistida_6meses = RestarOtrasDetenciones(self._computo_libertad_asistida_6meses, self._otros_tiempos_de_detencion)

    def _ImprimirResultados(self):
        resultadosFinales = '''
Cómputo de pena
---------------
Fecha de detención: {}
Vencimiento de pena: {}
La libertad condicional se obtiene a los {} año(s), {} mes(es) y {} día(s) de detención.
Libertad condicional: {}
Las salidas transitorias se obtienen a los {} año(s), {} mes(es) y {} día(s) de detención.
Salidas transitorias: {}
Libertad asistida -3 meses-: {}
Libertad asistida -6 meses-: {}
'''.format(self._fecha_de_detencion,
        self._vencimiento_de_pena,
        self._requisito_libertad_condicional.años, self._requisito_libertad_condicional.meses, self._requisito_libertad_condicional.dias,
        self._computo_libertad_condicional,
        self._requisito_salidas_transitorias.años, self._requisito_salidas_transitorias.meses, self._requisito_salidas_transitorias.dias,
        self._computo_salidas_transitorias,
        self._computo_libertad_asistida_3meses,
        self._computo_libertad_asistida_6meses)

        resultadosSinRestarOtrasDetenciones = '''
Resultados sin restar otras detenciones
---------------------------------------
Fecha de detención: {}
Vencimiento de pena: {}
Libertad condicional: {}
Salidas transitorias: {}
Libertad asistida -3 meses-: {}
Libertad asistida -6 meses-: {}
'''.format(self._fecha_de_detencion, 
        self._vencimiento_de_pena_sinRestarOtrasDetenciones,        
        self._computo_libertad_condicional_sinRestarOtrasDetenciones,        
        self._computo_salidas_transitorias_sinRestarOtrasDetenciones,
        self._computo_libertad_asistida_3meses_sinRestarOtrasDetenciones,
        self._computo_libertad_asistida_6meses_sinRestarOtrasDetenciones)

        print(resultadosFinales)
        print(resultadosSinRestarOtrasDetenciones)

def _DEBUG():    
    
    fechaDeDetencionInput = GetConsoleInput_Fecha('Ingresar fecha de detención en formato año-mes-día (XXXX/XX/XX): ')
    montoDePena = GetConsoleInput_MontoDePena()
    otrasDetenciones = GetConsoleInput_OtrosTiemposDeDetencion()
    
    computo = ComputoDePena(fechaDeDetencionInput, montoDePena, otrasDetenciones)    
    computo._ImprimirResultados()    

if __name__ == '__main__':
    _DEBUG()