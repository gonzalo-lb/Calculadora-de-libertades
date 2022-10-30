import datetime
from dateutil.relativedelta import relativedelta
from libcalc_methods import *

class ComputoDePena():
    
    def __init__(self, fechaDelHecho:datetime.date, fechaDeDetencion:datetime.date, montoDePena:TiempoEnAños_Meses_Dias, otrosTiemposDeDetencion='NULL'):
        
        # DEFINE LAS VARIABLES QUE DEPENDEN DE LOS PARÁMETROS INGRESADOS
        self._fecha_del_hecho = fechaDelHecho
        self._fecha_de_detencion = fechaDeDetencion
        self._monto_de_pena = montoDePena
        self._otros_tiempos_de_detencion = otrosTiemposDeDetencion
        
        # DETERMINA EL REGIMEN NORMATIVO A UTILIZAR
        regimenNormativoAplicable = RegimenNormativoAplicable(self._fecha_del_hecho)
        print(regimenNormativoAplicable)

        # CALCULA LAS LIBERTADES

        self._vencimiento_de_pena, self._vencimiento_de_pena_sinRestarOtrasDetenciones, self._caducidad_de_la_pena, self._caducidad_de_la_pena_sinRestarOtrasDetenciones = self.__CalcularVencimientoYCaducidadDePena(self._fecha_de_detencion, self._monto_de_pena, self._otros_tiempos_de_detencion)                
        self._computo_libertad_condicional, self._computo_libertad_condicional_sinRestarOtrasDetenciones, self._requisito_libertad_condicional = self.__CalcularLibertadCondicional(self._fecha_de_detencion, self._monto_de_pena, self._otros_tiempos_de_detencion)
        self._computo_salidas_transitorias, self._computo_salidas_transitorias_sinRestarOtrasDetenciones, self._requisito_salidas_transitorias = self.__CalcularSalidasTransitorias(self._fecha_de_detencion, self._monto_de_pena, self._otros_tiempos_de_detencion)
        self._computo_libertad_asistida_3meses, self._computo_libertad_asistida_3meses_sinRestarOtrasDetenciones = self.__CalcularLibertadAsistida_3meses(self._vencimiento_de_pena, self._otros_tiempos_de_detencion)
        self._computo_libertad_asistida_6meses, self._computo_libertad_asistida_6meses_sinRestarOtrasDetenciones = self.__CalcularLibertadAsistida_6meses(self._vencimiento_de_pena, self._otros_tiempos_de_detencion)
            
    def __CalcularVencimientoYCaducidadDePena(self, _fechaDeDetencion:datetime.date, _montoDePena:TiempoEnAños_Meses_Dias, _otrosTiemposDeDetencion="NULL"):

        TR_vencimientoDePena = _fechaDeDetencion        
        TR_vencimientoDePena += relativedelta(days=_montoDePena.dias)
        TR_vencimientoDePena += relativedelta(months=_montoDePena.meses)
        TR_vencimientoDePena += relativedelta(years=_montoDePena.años)
        TR_vencimientoDePena += relativedelta(days=-1)
        TR_vencimientoDePena_sinRestarOtrasDetenciones = TR_vencimientoDePena
        if _otrosTiemposDeDetencion != "NULL":
            TR_vencimientoDePena = RestarOtrasDetenciones(TR_vencimientoDePena, _otrosTiemposDeDetencion)
        TR_caducidad_de_la_pena = TR_vencimientoDePena + relativedelta(years=10)
        TR_caducidad_de_la_pena_sinRestarOtrasDetenciones = TR_vencimientoDePena_sinRestarOtrasDetenciones + relativedelta(years=10)
        return TR_vencimientoDePena, TR_vencimientoDePena_sinRestarOtrasDetenciones, TR_caducidad_de_la_pena, TR_caducidad_de_la_pena_sinRestarOtrasDetenciones
        
    def __CalcularLibertadCondicional(self, _fechaDeDetencion:datetime.date, _montoDePena:TiempoEnAños_Meses_Dias, _otrosTiemposDeDetencion="NULL"):

        TR_computo_libertad_condicional = _fechaDeDetencion
        TR_requisito_libertad_condicional = TiempoEnAños_Meses_Dias()        

        if _montoDePena.años < 3 or (_montoDePena.años == 3 and _montoDePena.meses == 0 and _montoDePena.dias == 0):
            TR_requisito_libertad_condicional.años = 0
            TR_requisito_libertad_condicional.meses = 8
            TR_requisito_libertad_condicional.dias = 0
            TR_computo_libertad_condicional += relativedelta(months=8)
        else:
            # Calcula los 2/3 de los días, lo redondea para abajo si da con coma, y los suma
            TR_requisito_libertad_condicional.dias = int((_montoDePena.dias * 2) / 3) # Hace los dos tercios y lo redondea para abajo
            TR_computo_libertad_condicional +=relativedelta(days=TR_requisito_libertad_condicional.dias)

            # Calcula los 2/3 de los meses
            TR_requisito_libertad_condicional.meses = _montoDePena.meses
            TR_requisito_libertad_condicional.meses = (TR_requisito_libertad_condicional.meses * 2) / 3
            LC_dias_resto = 0
            if TR_requisito_libertad_condicional.meses.is_integer() is False:
                LC_dias_resto = TR_requisito_libertad_condicional.meses - int(TR_requisito_libertad_condicional.meses)
                TR_requisito_libertad_condicional.meses = int(TR_requisito_libertad_condicional.meses)
                if LC_dias_resto > 0.3 and LC_dias_resto < 0.4:
                    LC_dias_resto = int(10)
                elif LC_dias_resto > 0.6 and LC_dias_resto < 0.7:
                    LC_dias_resto = int(20)
                else:
                    print('ERROR: Al calcular los 2/3 de los meses, los decimales no son ni 0.3333 ni 0.6666!')
                TR_computo_libertad_condicional +=relativedelta(days=LC_dias_resto)
                TR_computo_libertad_condicional +=relativedelta(months=TR_requisito_libertad_condicional.meses)
            else:
                TR_computo_libertad_condicional +=relativedelta(months=TR_requisito_libertad_condicional.meses)

            while LC_dias_resto >= 30:
                TR_requisito_libertad_condicional.meses += 1
                LC_dias_resto -= 30
            TR_requisito_libertad_condicional.dias += LC_dias_resto

            # 2/3 de los años
            LC_años_en_meses = _montoDePena.años * 12
            LC_años_en_meses = (LC_años_en_meses * 2) / 3
            TR_computo_libertad_condicional +=relativedelta(months=LC_años_en_meses)

            TR_requisito_libertad_condicional.años = 0
            while LC_años_en_meses >= 12:
                LC_años_en_meses -=12
                TR_requisito_libertad_condicional.años +=1
            TR_requisito_libertad_condicional.meses += LC_años_en_meses
            if TR_requisito_libertad_condicional.meses >= 12:
                TR_requisito_libertad_condicional.meses -=12
                TR_requisito_libertad_condicional.años +=1
            
            if type(TR_requisito_libertad_condicional.años) is not int and TR_requisito_libertad_condicional.años.is_integer():
                TR_requisito_libertad_condicional.años = int(TR_requisito_libertad_condicional.años)
            if type(TR_requisito_libertad_condicional.meses) is not int and TR_requisito_libertad_condicional.meses.is_integer():
                TR_requisito_libertad_condicional.meses = int(TR_requisito_libertad_condicional.meses)
            if type(TR_requisito_libertad_condicional.dias) is not int and TR_requisito_libertad_condicional.dias.is_integer():
                TR_requisito_libertad_condicional.dias = int(TR_requisito_libertad_condicional.dias)

            TR_computo_libertad_condicional += relativedelta(days=-1)

            TR_computo_libertad_condicional_sinRestarOtrasDetenciones = TR_computo_libertad_condicional            
            if _otrosTiemposDeDetencion != "NULL":
                TR_computo_libertad_condicional = RestarOtrasDetenciones(TR_computo_libertad_condicional, _otrosTiemposDeDetencion)
            
            return TR_computo_libertad_condicional, TR_computo_libertad_condicional_sinRestarOtrasDetenciones, TR_requisito_libertad_condicional

    def __CalcularSalidasTransitorias(self, _fechaDeDetencion:datetime.date, _montoDePena:TiempoEnAños_Meses_Dias, _otrosTiemposDeDetencion="NULL"):
        TR_computo_salidas_transitorias = datetime.date
        TR_computo_salidas_transitorias_sinRestarOtrasDetenciones = datetime.date
        TR_requisito_salidas_transitorias = TiempoEnAños_Meses_Dias()
        
        TR_computo_salidas_transitorias = _fechaDeDetencion        

        # Calcula la mitad de los días lo redondea para abajo si da con coma, y los suma
        TR_requisito_salidas_transitorias.dias = int(_montoDePena.dias / 2) # Hace la mitad y lo redondea para abajo
        TR_computo_salidas_transitorias +=relativedelta(days=TR_requisito_salidas_transitorias.dias)

        # Calcula la mitad de los meses
        TR_requisito_salidas_transitorias.meses = _montoDePena.meses
        ST_dias_resto = 0
        if TR_requisito_salidas_transitorias.meses == 1:
            TR_requisito_salidas_transitorias.meses = 0
            ST_dias_resto = int(15)
        elif TR_requisito_salidas_transitorias.meses > 1:
            if es_multiplo(TR_requisito_salidas_transitorias.meses, 2):
                TR_requisito_salidas_transitorias.meses /= 2
            else:
                TR_requisito_salidas_transitorias.meses = _montoDePena.meses/2
                TR_requisito_salidas_transitorias.meses = int(TR_requisito_salidas_transitorias.meses)        
                ST_dias_resto = int(15)

        TR_computo_salidas_transitorias += relativedelta(months=TR_requisito_salidas_transitorias.meses)
        TR_computo_salidas_transitorias += relativedelta(days=ST_dias_resto)

        while ST_dias_resto >= 30:
            TR_requisito_salidas_transitorias.meses += 1
            ST_dias_resto -= 30
        TR_requisito_salidas_transitorias.dias += ST_dias_resto

        # Calcula la mitad de los años
        TR_requisito_salidas_transitorias.años = _montoDePena.años
        ST_meses_resto = 0
        if TR_requisito_salidas_transitorias.años == 1:
            TR_requisito_salidas_transitorias.años = 0
            ST_meses_resto = int(6)
        elif TR_requisito_salidas_transitorias.años > 1:
            if es_multiplo(TR_requisito_salidas_transitorias.años, 2):
                TR_requisito_salidas_transitorias.años /= 2
            else:
                TR_requisito_salidas_transitorias.años /= 2
                TR_requisito_salidas_transitorias.años = int(TR_requisito_salidas_transitorias.años)
                ST_meses_resto = int(6)

        TR_computo_salidas_transitorias += relativedelta(years=TR_requisito_salidas_transitorias.años)
        TR_computo_salidas_transitorias += relativedelta(months=ST_meses_resto)

        while ST_meses_resto >= 12:
            TR_requisito_salidas_transitorias.años += 1
            ST_meses_resto -= 12
        TR_requisito_salidas_transitorias.meses += ST_meses_resto

        TR_computo_salidas_transitorias += relativedelta(days=-1)

        # Resta las otras detenciones, si hay
        TR_computo_salidas_transitorias_sinRestarOtrasDetenciones = TR_computo_salidas_transitorias
        if _otrosTiemposDeDetencion != "NULL":
            TR_computo_salidas_transitorias = RestarOtrasDetenciones(TR_computo_salidas_transitorias, _otrosTiemposDeDetencion)

        # Se ajustan los resultados para que no tengan decimales
        if type(TR_requisito_salidas_transitorias.años) is not int and TR_requisito_salidas_transitorias.años.is_integer():
            TR_requisito_salidas_transitorias.años = int(TR_requisito_salidas_transitorias.años)
        if type(TR_requisito_salidas_transitorias.meses) is not int and TR_requisito_salidas_transitorias.meses.is_integer():
            TR_requisito_salidas_transitorias.meses = int(TR_requisito_salidas_transitorias.meses)
        if type(TR_requisito_salidas_transitorias.dias) is not int and TR_requisito_salidas_transitorias.dias.is_integer():
            TR_requisito_salidas_transitorias.dias = int(TR_requisito_salidas_transitorias.dias)
        
        return TR_computo_salidas_transitorias, TR_computo_salidas_transitorias_sinRestarOtrasDetenciones, TR_requisito_salidas_transitorias

    def __CalcularLibertadAsistida_3meses(self, _vencimientoDePena:datetime.date, _vencimiento_sinRestarOtrasDetenciones:datetime.date):
        
        TR_computo_libertad_asistida_3meses = _vencimientoDePena
        TR_computo_libertad_asistida_3meses += relativedelta(months=-3)

        TR_computo_libertad_asistida_3meses_sinRestarOtrasDetenciones = _vencimiento_sinRestarOtrasDetenciones
        TR_computo_libertad_asistida_3meses_sinRestarOtrasDetenciones += relativedelta(months=-3)
        
        return TR_computo_libertad_asistida_3meses, TR_computo_libertad_asistida_3meses_sinRestarOtrasDetenciones
        
    def __CalcularLibertadAsistida_6meses(self, _vencimientoDePena:datetime.date, _vencimiento_sinRestarOtrasDetenciones:datetime.date):
        
        TR_computo_libertad_asistida_6meses = _vencimientoDePena
        TR_computo_libertad_asistida_6meses += relativedelta(months=-3)

        TR_computo_libertad_asistida_6meses_sinRestarOtrasDetenciones = _vencimiento_sinRestarOtrasDetenciones
        TR_computo_libertad_asistida_6meses_sinRestarOtrasDetenciones += relativedelta(months=-3)
        
        return TR_computo_libertad_asistida_6meses, TR_computo_libertad_asistida_6meses_sinRestarOtrasDetenciones

    def _ImprimirResultados(self):
        resultadosFinales = '''
Cómputo de pena
---------------
Fecha de detención: {}
Vencimiento de pena: {}
Caducidad de la pena: {}
La libertad condicional se obtiene a los {} año(s), {} mes(es) y {} día(s) de detención.
Libertad condicional: {}
Las salidas transitorias se obtienen a los {} año(s), {} mes(es) y {} día(s) de detención.
Salidas transitorias: {}
Libertad asistida -3 meses-: {}
Libertad asistida -6 meses-: {}
'''.format(self._fecha_de_detencion,
        self._vencimiento_de_pena,
        self._caducidad_de_la_pena, 
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
Caducidad de la pena: {}
Libertad condicional: {}
Salidas transitorias: {}
Libertad asistida -3 meses-: {}
Libertad asistida -6 meses-: {}
'''.format(self._fecha_de_detencion, 
        self._vencimiento_de_pena_sinRestarOtrasDetenciones, 
        self._caducidad_de_la_pena_sinRestarOtrasDetenciones, 
        self._computo_libertad_condicional_sinRestarOtrasDetenciones,        
        self._computo_salidas_transitorias_sinRestarOtrasDetenciones,
        self._computo_libertad_asistida_3meses_sinRestarOtrasDetenciones,
        self._computo_libertad_asistida_6meses_sinRestarOtrasDetenciones)

        print(resultadosFinales)
        print(resultadosSinRestarOtrasDetenciones)

def _DEBUG():    
    
    fechaDelHecho = GetConsoleInput_Fecha('Ingresar fecha del hecho en formato día/mes/año (XX/XX/XXXX): ')
    fechaDeDetencionInput = GetConsoleInput_Fecha('Ingresar fecha de detención en formato día/mes/año (XX/XX/XXXX): ')
    montoDePena = GetConsoleInput_MontoDePena()
    otrasDetenciones = GetConsoleInput_OtrosTiemposDeDetencion()
    
    computo = ComputoDePena(fechaDelHecho, fechaDeDetencionInput, montoDePena, otrasDetenciones)    
    computo._ImprimirResultados()    

if __name__ == '__main__':
    _DEBUG()