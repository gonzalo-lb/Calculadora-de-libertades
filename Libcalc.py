import datetime
from dateutil.relativedelta import relativedelta
from libcalc_methods import *

class ComputoDePena():
    
    def __init__(self, fechaDelHecho:datetime.date, fechaDeDetencion:datetime.date, fechaDeSentencia:datetime.date, montoDePena:MontoDePena, otrosTiemposDeDetencion='NULL', situacionProcesal:SituacionProcesal=None):

        # DEFINE LAS VARIABLES QUE DEPENDEN DE LOS PARÁMETROS INGRESADOS
        self._fecha_del_hecho = fechaDelHecho
        self._fecha_de_sentencia = fechaDeSentencia
        self._fecha_de_detencion = fechaDeDetencion
        self._monto_de_pena = montoDePena
        self._otros_tiempos_de_detencion = otrosTiemposDeDetencion 
        self._situacionProcesal = situacionProcesal
        
        # DETERMINA EL REGIMEN NORMATIVO A UTILIZAR
        self._regimenNormativoAplicable = RegimenNormativoAplicable(self._fecha_del_hecho)
        print(self._regimenNormativoAplicable)

        # CALCULA LAS LIBERTADES
        self._vencimiento_de_pena, self._vencimiento_de_pena_sinRestarOtrasDetenciones, self._caducidad_de_la_pena, self._caducidad_de_la_pena_sinRestarOtrasDetenciones = self.__CalcularVencimientoYCaducidadDePena(self._fecha_de_detencion, self._monto_de_pena, self._otros_tiempos_de_detencion)                
        self._computo_libertad_condicional, self._computo_libertad_condicional_sinRestarOtrasDetenciones, self._requisito_libertad_condicional = self.__CalcularLibertadCondicional(self._fecha_de_detencion, self._monto_de_pena, self._otros_tiempos_de_detencion)
        self._computo_salidas_transitorias, self._computo_salidas_transitorias_sinRestarOtrasDetenciones, self._requisito_salidas_transitorias = self.__CalcularSalidasTransitorias(self._fecha_de_detencion, self._monto_de_pena, self._otros_tiempos_de_detencion)
        self._computo_libertad_asistida, self._computo_libertad_asistida_sinRestarOtrasDetenciones = self.__CalcularLibertadAsistida(self._vencimiento_de_pena, self._vencimiento_de_pena_sinRestarOtrasDetenciones)
        
    def __Calcular_dos_tercios(self, _montoDePena:MontoDePena):

        if _montoDePena.perpetua:
            return _montoDePena
        
        TR_dos_tercios = MontoDePena()

        # Calcula los 2/3 de los días, lo redondea para abajo si da con coma, y los suma
        TR_dos_tercios.dias = int((_montoDePena.dias * 2) / 3) # Hace los dos tercios y lo redondea para abajo        

        # Calcula los 2/3 de los meses
        TR_dos_tercios.meses = _montoDePena.meses
        TR_dos_tercios.meses = (TR_dos_tercios.meses * 2) / 3
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

        # 2/3 de los años
        LC_años_en_meses = _montoDePena.años * 12
        LC_años_en_meses = (LC_años_en_meses * 2) / 3        

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
    
    def __Calcular_la_mitad(self, _montoDePena:MontoDePena):  

        if _montoDePena.perpetua:
            return _montoDePena
              
        TR_mitad_de_pena = MontoDePena()        
        
        # Calcula la mitad de los días lo redondea para abajo si da con coma, y los suma
        TR_mitad_de_pena.dias = int(_montoDePena.dias / 2) # Hace la mitad y lo redondea para abajo        

        # Calcula la mitad de los meses
        TR_mitad_de_pena.meses = _montoDePena.meses
        ST_dias_resto = 0
        if TR_mitad_de_pena.meses == 1:
            TR_mitad_de_pena.meses = 0
            ST_dias_resto = int(15)
        elif TR_mitad_de_pena.meses > 1:
            if es_multiplo(TR_mitad_de_pena.meses, 2):
                TR_mitad_de_pena.meses /= 2
            else:
                TR_mitad_de_pena.meses = _montoDePena.meses/2
                TR_mitad_de_pena.meses = int(TR_mitad_de_pena.meses)        
                ST_dias_resto = int(15)        

        while ST_dias_resto >= 30:
            TR_mitad_de_pena.meses += 1
            ST_dias_resto -= 30
        TR_mitad_de_pena.dias += ST_dias_resto

        # Calcula la mitad de los años
        TR_mitad_de_pena.años = _montoDePena.años
        ST_meses_resto = 0
        if TR_mitad_de_pena.años == 1:
            TR_mitad_de_pena.años = 0
            ST_meses_resto = int(6)
        elif TR_mitad_de_pena.años > 1:
            if es_multiplo(TR_mitad_de_pena.años, 2):
                TR_mitad_de_pena.años /= 2
            else:
                TR_mitad_de_pena.años /= 2
                TR_mitad_de_pena.años = int(TR_mitad_de_pena.años)
                ST_meses_resto = int(6)        

        while ST_meses_resto >= 12:
            TR_mitad_de_pena.años += 1
            ST_meses_resto -= 12
        TR_mitad_de_pena.meses += ST_meses_resto                

        # Se ajustan los resultados para que no tengan decimales
        if type(TR_mitad_de_pena.años) is not int and TR_mitad_de_pena.años.is_integer():
            TR_mitad_de_pena.años = int(TR_mitad_de_pena.años)
        if type(TR_mitad_de_pena.meses) is not int and TR_mitad_de_pena.meses.is_integer():
            TR_mitad_de_pena.meses = int(TR_mitad_de_pena.meses)
        if type(TR_mitad_de_pena.dias) is not int and TR_mitad_de_pena.dias.is_integer():
            TR_mitad_de_pena.dias = int(TR_mitad_de_pena.dias)
        
        return TR_mitad_de_pena
    
    def __SumarMontoDePena(self, _fecha:datetime.date, _montoDePena:MontoDePena):
        TR_fecha = _fecha
        TR_fecha += relativedelta(years=_montoDePena.años)
        TR_fecha += relativedelta(months=_montoDePena.meses)
        TR_fecha += relativedelta(days=_montoDePena.dias)
        TR_fecha += relativedelta(days=-1)
        return TR_fecha

    def __RestarOtrasDetenciones(self, _fecha:datetime.date, _otrasDetenciones:OtraDetencion):
        TR_fecha = _fecha
        if _otrasDetenciones != "NULL":
            TR_fecha = RestarOtrasDetenciones(TR_fecha, _otrasDetenciones)
        return TR_fecha
            
    def __CalcularVencimientoYCaducidadDePena(self, _fechaDeDetencion:datetime.date, _fechaDeSentencia:datetime.date, _montoDePena:MontoDePena, _otrosTiemposDeDetencion="NULL"):

        TR_vencimientoDePena = ''
        TR_vencimientoDePena_sinRestarOtrasDetenciones = ''
        TR_caducidad_de_la_pena = ''
        TR_caducidad_de_la_pena_sinRestarOtrasDetenciones = ''        

        if _montoDePena.ejecuciónCondicional:
            TR_vencimientoDePena = self.__SumarMontoDePena(_fechaDeSentencia, _montoDePena)            
            TR_caducidad_de_la_pena = TR_vencimientoDePena + relativedelta(years=10)    
            TR_vencimientoDePena_sinRestarOtrasDetenciones = 'No aplica'        
            TR_caducidad_de_la_pena_sinRestarOtrasDetenciones = 'No aplica'
        elif _montoDePena.perpetua and not _montoDePena.reclusionPorTiempoIndeterminado:
            TR_vencimientoDePena = 'Vencimiento de pena: Pena perpetua'
            TR_vencimientoDePena_sinRestarOtrasDetenciones = 'Vencimiento de pena: Pena perpetua'
            TR_caducidad_de_la_pena = 'Vencimiento de pena: Pena perpetua'
            TR_caducidad_de_la_pena_sinRestarOtrasDetenciones = 'Vencimiento de pena: Pena perpetua'
        elif _montoDePena.perpetua and _montoDePena.reclusionPorTiempoIndeterminado:
            TR_vencimientoDePena = 'Vencimiento de pena: Pena perpetua y reclusión por tiempo indeterminado'
            TR_vencimientoDePena_sinRestarOtrasDetenciones = 'Vencimiento de pena: Pena perpetua y reclusión por tiempo indeterminado'
            TR_caducidad_de_la_pena = 'Vencimiento de pena: Pena perpetua y reclusión por tiempo indeterminado'
            TR_caducidad_de_la_pena_sinRestarOtrasDetenciones = 'Vencimiento de pena: Pena perpetua y reclusión por tiempo indeterminado'        
        else:            
            TR_vencimientoDePena = self.__SumarMontoDePena(_fechaDeDetencion, _montoDePena)
            TR_vencimientoDePena_sinRestarOtrasDetenciones = TR_vencimientoDePena
            TR_vencimientoDePena = self.__RestarOtrasDetenciones(TR_vencimientoDePena, _otrosTiemposDeDetencion)            
            TR_caducidad_de_la_pena = TR_vencimientoDePena + relativedelta(years=10)
            TR_caducidad_de_la_pena_sinRestarOtrasDetenciones = TR_vencimientoDePena_sinRestarOtrasDetenciones + relativedelta(years=10)            
        
        return (TR_vencimientoDePena,
        TR_vencimientoDePena_sinRestarOtrasDetenciones,
        TR_caducidad_de_la_pena,
        TR_caducidad_de_la_pena_sinRestarOtrasDetenciones)
        
    def __CalcularLibertadCondicional(self, _fechaDeDetencion:datetime.date, _montoDePena:MontoDePena, _otrosTiemposDeDetencion="NULL"):

        TR_computo_libertad_condicional = _fechaDeDetencion
        TR_requisito_libertad_condicional = MontoDePena()        

        if _montoDePena.perpetua:
            
            TR_requisito_libertad_condicional.perpetua = True

            # CALCULO DE PENA PERPETUA

            if self._regimenNormativoAplicable._regimen_LC == "Ley 11.179":                                
                TR_requisito_libertad_condicional.años = 20
                TR_computo_libertad_condicional = self.__SumarMontoDePena(_fechaDeDetencion, TR_requisito_libertad_condicional)

            
            if self._regimenNormativoAplicable._regimen_LC == "Ley 25.892" or self._regimenNormativoAplicable._libertadCondicional == "Ley 27.375":
                TR_requisito_libertad_condicional.años = 35
                TR_computo_libertad_condicional = self.__SumarMontoDePena(_fechaDeDetencion, TR_requisito_libertad_condicional)                

        else:

            # CALCULO DE PENA TEMPORAL

            if _montoDePena.años < 3 or (_montoDePena.años == 3 and _montoDePena.meses == 0 and _montoDePena.dias == 0):                
                TR_requisito_libertad_condicional.meses = 8                
                TR_computo_libertad_condicional = self.__SumarMontoDePena(_fechaDeDetencion, TR_requisito_libertad_condicional)
            else:
                TR_requisito_libertad_condicional = self.__Calcular_dos_tercios(_montoDePena)
                TR_computo_libertad_condicional = self.__SumarMontoDePena(_fechaDeDetencion, TR_requisito_libertad_condicional)                

        # Resta otras detenciones, si hay
        TR_computo_libertad_condicional_sinRestarOtrasDetenciones = TR_computo_libertad_condicional
        TR_computo_libertad_condicional = self.__RestarOtrasDetenciones(TR_computo_libertad_condicional, _otrosTiemposDeDetencion)
            
        return TR_computo_libertad_condicional, TR_computo_libertad_condicional_sinRestarOtrasDetenciones, TR_requisito_libertad_condicional
     
    def __CalcularSalidasTransitorias(self, _fechaDeDetencion:datetime.date, _montoDePena:MontoDePena, _otrosTiemposDeDetencion="NULL", _fechaIngresoAPeriodoDePrueba:datetime.date=None):
        TR_computo_salidas_transitorias = _fechaDeDetencion
        TR_computo_salidas_transitorias_sinRestarOtrasDetenciones = datetime.date
        TR_requisito_salidas_transitorias = MontoDePena()        

        if _montoDePena.perpetua:

            TR_requisito_salidas_transitorias.perpetua = True

            if self._regimenNormativoAplicable._regimen_ST == "Decreto Ley 412/58" or self._regimenNormativoAplicable._regimen_ST == "Ley 24.660" or self._regimenNormativoAplicable._regimen_ST == "Ley 25.948":
                
                TR_requisito_salidas_transitorias.años = 15
                TR_computo_salidas_transitorias = self.__SumarMontoDePena(_fechaDeDetencion, TR_requisito_salidas_transitorias)                
            
            if  self._regimenNormativoAplicable._regimen_ST == "Ley 27.375":
                TR_computo_salidas_transitorias = 'Se requiere un año luego de haber ingresado al periodo de prueba'
                TR_computo_salidas_transitorias_sinRestarOtrasDetenciones = 'Se requiere un año luego de haber ingresado al periodo de prueba'
                TR_requisito_salidas_transitorias.años = '***'
                TR_requisito_salidas_transitorias.meses = '***'
                TR_requisito_salidas_transitorias.dias = '***'
        else:   

            if self._regimenNormativoAplicable._regimen_ST == "Decreto Ley 412/58" or self._regimenNormativoAplicable._regimen_ST == "Ley 24.660" or self._regimenNormativoAplicable._regimen_ST == "Ley 25.948":
                
                TR_requisito_salidas_transitorias = self.__Calcular_la_mitad(_montoDePena)
                TR_computo_salidas_transitorias = self.__SumarMontoDePena(TR_computo_salidas_transitorias, TR_requisito_salidas_transitorias)
            
            if  self._regimenNormativoAplicable._regimen_ST == "Ley 27.375":
                TR_computo_salidas_transitorias = 'Se requiere un año luego de haber ingresado al periodo de prueba'
                TR_computo_salidas_transitorias_sinRestarOtrasDetenciones = 'Se requiere un año luego de haber ingresado al periodo de prueba'
                TR_requisito_salidas_transitorias.años = '***'
                TR_requisito_salidas_transitorias.meses = '***'
                TR_requisito_salidas_transitorias.dias = '***'            
        
        # Resta otras detenciones, si hay
        TR_computo_salidas_transitorias_sinRestarOtrasDetenciones = TR_computo_salidas_transitorias
        TR_computo_salidas_transitorias = self.__RestarOtrasDetenciones(TR_computo_salidas_transitorias, _otrosTiemposDeDetencion)

        return TR_computo_salidas_transitorias, TR_computo_salidas_transitorias_sinRestarOtrasDetenciones, TR_requisito_salidas_transitorias
    
    def __CalcularLibertadAsistida(self, _vencimientoDePena:datetime.date, _vencimiento_sinRestarOtrasDetenciones:datetime.date):
        
        TR_computo_libertad_asistida = ''
        TR_computo_libertad_asistida_sinRestarOtrasDetenciones = ''

        if self._monto_de_pena.perpetua:
            TR_computo_libertad_asistida = 'Pena perpetua'
            TR_computo_libertad_asistida_sinRestarOtrasDetenciones = 'Pena perpetua'

        else:
            if self._regimenNormativoAplicable._regimen_LA == "Ley 24.660" or self._regimenNormativoAplicable._regimen_LA == "Ley 25.948":

                TR_computo_libertad_asistida = _vencimientoDePena
                TR_computo_libertad_asistida += relativedelta(months=-6)

                TR_computo_libertad_asistida_sinRestarOtrasDetenciones = _vencimiento_sinRestarOtrasDetenciones
                TR_computo_libertad_asistida_sinRestarOtrasDetenciones += relativedelta(months=-6)
            
            if self._regimenNormativoAplicable._regimen_LA == "Ley 27.375":

                TR_computo_libertad_asistida = _vencimientoDePena
                TR_computo_libertad_asistida += relativedelta(months=-3)

                TR_computo_libertad_asistida_sinRestarOtrasDetenciones = _vencimiento_sinRestarOtrasDetenciones
                TR_computo_libertad_asistida_sinRestarOtrasDetenciones += relativedelta(months=-3)
        
        return TR_computo_libertad_asistida, TR_computo_libertad_asistida_sinRestarOtrasDetenciones

    def _ImprimirResultadosVIEJO(self):        
        resultadosFinales = '''CÓMPUTO DE PENA
---------------
Fecha de detención: {}
Vencimiento de pena: {}
Caducidad de la pena: {}
La libertad condicional se obtiene a los {} año(s), {} mes(es) y {} día(s) de detención.
Libertad condicional: {}
Las salidas transitorias se obtienen a los {} año(s), {} mes(es) y {} día(s) de detención.
Salidas transitorias: {}
La libertad asistida se obtiene {} meses antes del vencimiento de pena
Libertad asistida: {}
'''.format(Datetime_date_enFormatoXX_XX_XXXX(self._fecha_de_detencion),
        Datetime_date_enFormatoXX_XX_XXXX(self._vencimiento_de_pena),
        Datetime_date_enFormatoXX_XX_XXXX(self._caducidad_de_la_pena), 
        self._requisito_libertad_condicional.años, self._requisito_libertad_condicional.meses, self._requisito_libertad_condicional.dias,
        Datetime_date_enFormatoXX_XX_XXXX(self._computo_libertad_condicional),
        self._requisito_salidas_transitorias.años, self._requisito_salidas_transitorias.meses, self._requisito_salidas_transitorias.dias,
        Datetime_date_enFormatoXX_XX_XXXX(self._computo_salidas_transitorias),
        self._regimenNormativoAplicable.LIBERTAD_ASISTIDA(LA_KEYS._requisitoTemporal_KEY),
        Datetime_date_enFormatoXX_XX_XXXX(self._computo_libertad_asistida))

        resultadosSinRestarOtrasDetenciones = '''RESULTADOS SIN RESTAR OTRAS DETENCIONES
---------------------------------------
Fecha de detención: {}
Vencimiento de pena: {}
Caducidad de la pena: {}
Libertad condicional: {}
Salidas transitorias: {}
Libertad asistida: {}
'''.format(Datetime_date_enFormatoXX_XX_XXXX(self._fecha_de_detencion), 
        Datetime_date_enFormatoXX_XX_XXXX(self._vencimiento_de_pena_sinRestarOtrasDetenciones), 
        Datetime_date_enFormatoXX_XX_XXXX(self._caducidad_de_la_pena_sinRestarOtrasDetenciones), 
        Datetime_date_enFormatoXX_XX_XXXX(self._computo_libertad_condicional_sinRestarOtrasDetenciones),        
        Datetime_date_enFormatoXX_XX_XXXX(self._computo_salidas_transitorias_sinRestarOtrasDetenciones),
        Datetime_date_enFormatoXX_XX_XXXX(self._computo_libertad_asistida_sinRestarOtrasDetenciones))

        print(resultadosFinales)
        print(resultadosSinRestarOtrasDetenciones)

    def _ImprimirResultados(self):
        # Arma el vencimiento de pena
        vencimientoDePena = ''
        vencimientoDePenaSinRestarOtrasDetenciones = ''
        if self._monto_de_pena.perpetua:
            vencimientoDePena = vencimientoDePenaSinRestarOtrasDetenciones = 'Vencimiento de pena: Pena perpetua'
        else:
            vencimientoDePena = f'Vencimiento de pena: {Datetime_date_enFormatoXX_XX_XXXX(self._vencimiento_de_pena)}'
            vencimientoDePenaSinRestarOtrasDetenciones  = f'Vencimiento de pena: {Datetime_date_enFormatoXX_XX_XXXX(self._vencimiento_de_pena_sinRestarOtrasDetenciones)}'
        
        # Arma la caducidad de la pena
        caducidadDeLaPena = ''
        caducidadDeLaPenaSinRestarOtrasDetenciones = ''
        if self._monto_de_pena.perpetua:
            caducidadDeLaPena = caducidadDeLaPenaSinRestarOtrasDetenciones = 'Caducidad de la pena: Pena perpetua'
        else:
            caducidadDeLaPena = f'Caducidad de la pena: {Datetime_date_enFormatoXX_XX_XXXX(self._caducidad_de_la_pena)}'
            caducidadDeLaPenaSinRestarOtrasDetenciones = f'Caducidad de la pena: {Datetime_date_enFormatoXX_XX_XXXX(self._caducidad_de_la_pena_sinRestarOtrasDetenciones)}'
        
        # Arma la libertad condicional
        libertadCondicional = ''
        libertadCondicional_requisito = f'La libertad condicional se obtiene a los {self._requisito_libertad_condicional.años} año(s), {self._requisito_libertad_condicional.meses} mes(es) y {self._requisito_libertad_condicional.dias} día(s) de detención.'
        libertadCondicional_computo = f'Libertad condicional: {Datetime_date_enFormatoXX_XX_XXXX(self._computo_libertad_condicional)}'
        libertadCondicional_advertenciaReincidencia = 'ADVERTENCIA: En el caso la persona es reincidente. No aplicaría el instituto de la libertad condicional (art. 14 CP).'
        libertadCondicional_advertenciaDelitosExcluidosLey25892 = 'ADVERTENCIA: Persona condenada por los delitos enumerados en el art. 14 CP. No aplicaría el instituto de la libertad condicional.'
        libertadCondicional_advertenciaDelitosExcluidosLey27375 = 'ADVERTENCIA: Persona condenada por los delitos enumerados en el art. 14 CP. No aplicaría el instituto de la libertad condicional.'

        libertadCondicional = f'{libertadCondicional_requisito}\n'\
            f'{libertadCondicional_computo}'
        if self._situacionProcesal._EsReincidente:
                libertadCondicional = f'{libertadCondicional}\n'\
                f'{libertadCondicional_advertenciaReincidencia}'       

        if self._regimenNormativoAplicable._regimen_LC == LC_REGIMENES._Ley_25892:            
            if self._situacionProcesal._EsPorDelitosExcluidosLey25892:
                libertadCondicional = f'{libertadCondicional}\n'\
                f'{libertadCondicional_advertenciaDelitosExcluidosLey25892}'
        
        if self._regimenNormativoAplicable._regimen_LC == LC_REGIMENES._Ley_27375:            
            if self._situacionProcesal._EsPorDelitosExcluidosLey27375:
                libertadCondicional = f'{libertadCondicional}\n'\
                f'{libertadCondicional_advertenciaDelitosExcluidosLey27375}'        
        

def _DEBUG():    
    
    fechaDelHecho = GetConsoleInput_Fecha('Ingresar fecha del hecho en formato día/mes/año (XX/XX/XXXX): ')
    fechaDeDetencionInput = GetConsoleInput_Fecha('Ingresar fecha de detención en formato día/mes/año (XX/XX/XXXX): ')
    montoDePena = GetConsoleInput_MontoDePena()
    otrasDetenciones = GetConsoleInput_OtrosTiemposDeDetencion()
    
    computo = ComputoDePena(fechaDelHecho, fechaDeDetencionInput, montoDePena, otrasDetenciones)    
    computo._ImprimirResultadosVIEJO()    

if __name__ == '__main__':
    _DEBUG()