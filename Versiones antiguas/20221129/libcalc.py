import datetime
from dateutil.relativedelta import relativedelta
from dateutil import relativedelta
from libcalc_methods import *
from copy import deepcopy

class Computo():
    def _Calcular_un_tercio(self, _montoDePena:MontoDePena):
        if _montoDePena.perpetua:
            print('def Calcular_un_tercio: ERROR: No se puede calcular un tercio de una perpetua.')
            return
        
        TR_dos_tercios = MontoDePena()

        # Calcula 1/3 de los días, lo redondea para abajo si da con coma, y los suma
        TR_dos_tercios.dias = int(_montoDePena.dias / 3) # Hace los dos tercios y lo redondea para abajo        

        # Calcula 1/3 de los meses
        TR_dos_tercios.meses = _montoDePena.meses
        TR_dos_tercios.meses = TR_dos_tercios.meses / 3
        LC_dias_resto = 0
        if TR_dos_tercios.meses.is_integer() is False:            
            LC_dias_resto = TR_dos_tercios.meses - int(TR_dos_tercios.meses)
            if LC_dias_resto < 0:
                LC_dias_resto += 1
            TR_dos_tercios.meses = int(TR_dos_tercios.meses)
            if LC_dias_resto > 0.3 and LC_dias_resto < 0.4:
                LC_dias_resto = int(10)
            elif LC_dias_resto > 0.6 and LC_dias_resto < 0.7:
                LC_dias_resto = int(20)
            else:
                print(LC_dias_resto)
                print('ERROR: Al calcular 1/3 de los meses, los decimales no son ni 0.3333 ni 0.6666!')                    

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

    def _Calcular_dos_tercios(self, _montoDePena:MontoDePena):

        if _montoDePena.perpetua:
            print('def Calcular_un_tercio: ERROR: No se puede calcular dos tercio de una perpetua.')
            return
        
        TR_dos_tercios = MontoDePena()

        # Calcula los 2/3 de los días, lo redondea para abajo si da con coma, y los suma
        TR_dos_tercios.dias = int((_montoDePena.dias * 2) / 3) # Hace los dos tercios y lo redondea para abajo        

        # Calcula los 2/3 de los meses
        TR_dos_tercios.meses = _montoDePena.meses
        TR_dos_tercios.meses = (TR_dos_tercios.meses * 2) / 3
        LC_dias_resto = 0
        if TR_dos_tercios.meses.is_integer() is False:
            LC_dias_resto = TR_dos_tercios.meses - int(TR_dos_tercios.meses)
            if LC_dias_resto < 0:
                LC_dias_resto += 1
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
    
    def _Calcular_la_mitad(self, _montoDePena:MontoDePena):  

        if _montoDePena.perpetua:
            print('def Calcular_un_tercio: ERROR: No se puede calcular la mitad de una perpetua.')
            return
              
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
    
    def _SumarMontoDePena(self, _fecha:datetime.date, _montoDePena:MontoDePena, _sumarPlazoControl:bool=False):
        TR_fecha = _fecha
        if _sumarPlazoControl:
            TR_fecha += relativedelta(years=_montoDePena.plazoControl_años)
            TR_fecha += relativedelta(months=_montoDePena.plazoControl_meses)
            TR_fecha += relativedelta(days=_montoDePena.plazoControl_dias)
            TR_fecha += relativedelta(days=-1)
        else:    
            TR_fecha += relativedelta(years=_montoDePena.años)
            TR_fecha += relativedelta(months=_montoDePena.meses)
            TR_fecha += relativedelta(days=_montoDePena.dias)
            TR_fecha += relativedelta(days=-1)
        return TR_fecha

    def _Multiplicar_Tiempo(self, tiempo:TiempoEn_Años_Meses_Dias, factor:int):        
        
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

    def _RestarOtrasDetenciones(self, _fecha:datetime.date, _otrasDetenciones:OtraDetencion):
        TR_fecha = _fecha
        if _otrasDetenciones != "NULL":
            TR_fecha = RestarOtrasDetenciones(TR_fecha, _otrasDetenciones)
        return TR_fecha

    def _AplicarEstimuloEducativo(self, _fecha:datetime.date, _tiempo:TiempoEn_Años_Meses_Dias):
        TR_fecha = _fecha
        TR_fecha -= relativedelta(days=_tiempo.dias)
        TR_fecha -= relativedelta(months=_tiempo.meses)
        TR_fecha -= relativedelta(years=_tiempo.años)
        return TR_fecha

class ComputoPenaTemporal(Computo):
    def __init__(self,
    fechaDelHecho:datetime.date='NULL',
    fechaDeDetencion:datetime.date='NULL',
    montoDePena:MontoDePena='NULL',
    otrasDetenciones:list[OtraDetencion]='NULL',
    estimuloEducativo:TiempoEn_Años_Meses_Dias=TiempoEn_Años_Meses_Dias(),
    fechaInicioEjecucion:datetime.date='NULL',
    fechaCalificacionBUENO:datetime.date='NULL',
    fechaIngresoPeriodoDePrueba:datetime.date='NULL',
    fechaCalificacionEJEMPLAR:datetime.date='NULL',
    vuelveARestarOtrasDetencionesyAplicar140enST=False) -> None:
        super().__init__()
        
        # INPUT
        self._fecha_del_hecho = fechaDelHecho
        self._fecha_de_detencion = fechaDeDetencion
        self._monto_de_pena = montoDePena
        self._otras_detenciones = otrasDetenciones
        self._estimulo_educativo = estimuloEducativo
        self._fecha_inicio_ejecucion = fechaInicioEjecucion
        self._fecha_calificacion_BUENO = fechaCalificacionBUENO
        self._fecha_calificacion_EJEMPLAR = fechaCalificacionEJEMPLAR
        self._fecha_ingreso_a_periodo_de_prueba = fechaIngresoPeriodoDePrueba
        self._vuelve_a_restar_otras_detenciones_y_140_en_ST= vuelveARestarOtrasDetencionesyAplicar140enST

        # VARIABLES CON LOS DATOS
        self._regimen_normativo = 'NULL'

        self._vencimiento_de_pena = 'NULL'
        self._caducidad_de_pena = 'NULL'

        self._libertad_condicional_COMPUTO = 'NULL'
        self._libertad_condicional_REQUISITO_TEMPORAL = 'NULL'
        self._libertad_condicional_REQUISITO_CALIF_BUENO = 'NULL'
        self._libertad_condicional_REQUISITO_CALIF_SITUACION = 'NULL'
        self._libertad_condicional_COMPUTO_INTEGRAL = 'NULL'

        self._salidas_transitorias_COMPUTO = 'NULL'
        self._salidas_transitorias_REQUISITO_TEMPORAL = 'NULL'
        self._salidas_transitorias_27375_SITUACION = 'NULL'
        self._salidas_transitorias_COMPUTO_PERIODO_DE_PRUEBA = 'NULL'        
        self._salidas_transitorias_REQUISITO_TEMPORAL_PERIODO_DE_PRUEBA = 'NULL'
        self._salidas_transitorias_REQUISITO_TEMPORAL_INTEGRAL = 'NULL'
        self._salidas_transitorias_REQUISITO_CALIF_EJEMPLAR = 'NULL'
        self._salidas_transitorias_REQUISITO_CALIF_BUENO = 'NULL'
        self._salidas_transitorias_REQUISITO_CALIF_SITUACION = 'NULL'

        self._libertad_asistida_COMPUTO = 'NULL'

        # VARIABLES OUTPUT (STRING)
        self._STRING_vencimiento_de_pena = ''
        self._STRING_caducidad_de_pena = ''

        if self._ControlarParametros():
            return
        
        # Determina el régimen normativo a utilizar
        self._regimen_normativo = RegimenNormativoAplicable(self._fecha_del_hecho)

        # Calcula el cómputo y lo guarda en las variables de datos
        self._CalcularVencimientoYCaducidadDePena()
        self._CalcularLibertadCondicional()
        self._CalcularSalidasTransitorias()
        self._CalcularLibertadAsistida()
        
        # Imprime los resultados
        self._ImprimirSTRINGGeneral()
        self._regimen_normativo._Imprimir()
        self._ImprimirSTRINGVencimientoYCaducidadDePena()
        self._ImprimirSTRINGLibertadCondicional()
        self._ImprimirSTRINGSalidasTransitorias()
        self._ImprimirSTRINGLibertadAsistida()
    
    def _ControlarParametros(self):
        if self._fecha_del_hecho == 'NULL':
            print('ERROR: LA FECHA DEL HECHO ES UN PARÁMETRO NECESARIO PARA REALIZAR EL CÓMPUTO.')
            return True
        if self._fecha_de_detencion == 'NULL':
            print('ERROR: LA FECHA DE DETENCION ES UN PARÁMETRO NECESARIO PARA REALIZAR EL CÓMPUTO.')
            return True
        if self._monto_de_pena == 'NULL':
            print('ERROR: LA PENA ES UN PARÁMETRO NECESARIO PARA REALIZAR EL CÓMPUTO.')
            return True
        if self._monto_de_pena.perpetua:
            print('ADVERTENCIA: SE INGRESÓ UNA PENA PERPETUA. LA CLASS CALCULA COMPUTOS DE PENAS TEMPORALES.')
            print('LOS RESULTADOS PODRÍAN NO SER ACERTADOS.')

    def _CalcularVencimientoYCaducidadDePena(self):
        '''Determina "vencimiento de pena" y "caducidad de pena"'''
        _vencimiento_de_pena = 0
        _caducidad_de_pena = 0

        _vencimiento_de_pena = self._SumarMontoDePena(self._fecha_de_detencion, self._monto_de_pena)
        print(f'DEBUG: Vencimiento de pena sin restar otras detenciones = {Datetime_date_enFormatoXX_XX_XXXX(_vencimiento_de_pena)}')
        _vencimiento_de_pena = self._RestarOtrasDetenciones(_vencimiento_de_pena, self._otras_detenciones)
        _caducidad_de_pena = _vencimiento_de_pena + relativedelta(years=10)

        self._vencimiento_de_pena = _vencimiento_de_pena
        self._caducidad_de_pena = _caducidad_de_pena        
    
    def _CalcularLibertadCondicional(self):

        # Crea las variables temporales que va a necesitar para el output y les asigna los datos que van a usar
        _computo_libertad_condicional = self._fecha_de_detencion
        _requisito_temporal_libertad_condicional = TiempoEn_Años_Meses_Dias()

        # Si es reincidente, o por delitos excluídos, igual hace el cálculo, pero arroja advertencias
        # Las advertencias las manejan las funciones que arman los string

        print(f'DEBUG: self._monto_de_pena es mayor a 3 años? --> {MontoDeTiempoA_es_Mayor_que_MontoDeTiempoB(self._monto_de_pena, TiempoEn_Años_Meses_Dias(_años=3))}')
        if MontoDeTiempoA_es_Mayor_que_MontoDeTiempoB(self._monto_de_pena, TiempoEn_Años_Meses_Dias(_años=3)) != True:
            _requisito_temporal_libertad_condicional.meses = 8                
            _computo_libertad_condicional = self._SumarMontoDePena(self._fecha_de_detencion, _requisito_temporal_libertad_condicional)
        else:
            _requisito_temporal_libertad_condicional = self._Calcular_dos_tercios(self._monto_de_pena)
            _computo_libertad_condicional = self._SumarMontoDePena(self._fecha_de_detencion, _requisito_temporal_libertad_condicional)                

        # Resta otras detenciones, si hay
        print(f'DEBUG: Cómputo Libertad Condicional sin restar otras detenciones = {Datetime_date_enFormatoXX_XX_XXXX(_computo_libertad_condicional)}')
        _computo_libertad_condicional = self._RestarOtrasDetenciones(_computo_libertad_condicional, self._otras_detenciones)

        # Aplica el estímulo educativo, si hay
        print(f'DEBUG: Cómputo Libertad Condicional sin aplicar estímulo educativo = {Datetime_date_enFormatoXX_XX_XXXX(_computo_libertad_condicional)}')
        _computo_libertad_condicional = self._AplicarEstimuloEducativo(_computo_libertad_condicional, self._estimulo_educativo)    

        # Aplica la información obtenida a las variables de datos
        self._libertad_condicional_COMPUTO = _computo_libertad_condicional
        self._libertad_condicional_REQUISITO_TEMPORAL = _requisito_temporal_libertad_condicional

        # Si aplica la ley 27.375, calcula además el requisito de calificación, y el integral
        if self._regimen_normativo._regimen_LC == LC_REGIMENES._Ley_27375.value:
            self._CalcularLibertadCondicional_RequisitoCalificacion()
            self._CalcularLibertadCondicional_ComputoIntegral()        
    
    def _CalcularLibertadCondicional_RequisitoCalificacion(self):

        # Guarda los resultados en:
            #   self._libertad_condicional_REQUISITO_CALIFICACION_BUENO
            #   self._libertad_condicional_REQUISITO_CALIFICACION_SITUACION
        
        _fechaLC = self._libertad_condicional_COMPUTO
        _fechaInicioEjecucion = self._fecha_inicio_ejecucion
        _fechaCalificacionBueno = self._fecha_calificacion_BUENO
        self._libertad_condicional_REQUISITO_CALIF_SITUACION = 0

        if _fechaInicioEjecucion == 'NULL':
            # SITUACIÓN 1
            # SI TODAVÍA NO COMENZÓ LA EJECUCIÓN DE PENA
            # En este caso no es posible calcular el requisito
            
            self._libertad_condicional_REQUISITO_CALIF_SITUACION = 1
            return
        
        elif _fechaInicioEjecucion != 'NULL' and _fechaCalificacionBueno == 'NULL':
            # SITUACIÓN 2
            # SI COMENZÓ LA EJECUCIÓN DE PENA PERO AÚN NO CALIFICÓ COMO "BUENO"
            # Determina la fecha límite para obtener el requisito "BUENO" teniendo en cuenta el requisito temporal LC en el caso concreto            
            
            delta = relativedelta(_fechaLC, _fechaInicioEjecucion)
            pena1_3=MontoDePena(_años=delta.years, _meses=delta.months, _dias=delta.days)
            pena1_3 = self._Calcular_un_tercio(pena1_3)            
            self._libertad_condicional_REQUISITO_CALIF_BUENO = self._SumarMontoDePena(_fechaInicioEjecucion, pena1_3)
            self._libertad_condicional_REQUISITO_CALIF_SITUACION = 2            
            return

        elif _fechaInicioEjecucion != 'NULL' and _fechaCalificacionBueno != 'NULL':
            # SITUACIÓN 3
            # SI SE ENCEUNTRA EJECUTANDO PENA Y TIENE REQUISITO DE CALIFICACIÓN "BUENO"
            # Determina la fecha desde la que se encontrará cumplido el requisito de calificación

            self._libertad_condicional_REQUISITO_CALIF_SITUACION = 3            
            delta = relativedelta(_fechaCalificacionBueno, _fechaInicioEjecucion)
            delta_TAMD = TiempoEn_Años_Meses_Dias(_años=delta.years, _meses=delta.months, _dias=delta.days)
            delta_x_3 = self._Multiplicar_Tiempo(delta_TAMD, 3)
            self._libertad_condicional_REQUISITO_CALIF_BUENO = self._SumarMontoDePena(_fechaInicioEjecucion, delta_x_3)
            self._libertad_condicional_REQUISITO_CALIF_SITUACION = 3            
            return
    
    def _CalcularLibertadCondicional_ComputoIntegral(self):
        '''Este cómputo solo aplicaría en la situación 3 (contar con requisito de calificación "BUENO")'''
        # Guarda el resultado en:
        #   self._libertad_condicional_COMPUTO_INTEGRAL

        if type(self._libertad_condicional_COMPUTO) is not datetime.date:
            print('DEBUG: def _CalcularLibertadCondicional_ComputoIntegral: self._libertad_condicional_COMPUTO is not datetime.date')
            return
        if type(self._libertad_condicional_REQUISITO_CALIF_BUENO) is not datetime.date:
            print('DEBUG: def _CalcularLibertadCondicional_ComputoIntegral: self._libertad_condicional_REQUISITO_CALIFICACION_BUENO is not datetime.date')
            return        

        if self._libertad_condicional_REQUISITO_CALIF_SITUACION == 3:
            if FechaA_es_Mayor_Que_FechaB(self._libertad_condicional_COMPUTO, self._libertad_condicional_REQUISITO_CALIF_BUENO):
                self._libertad_condicional_COMPUTO_INTEGRAL = self._libertad_condicional_COMPUTO
            else:
                self._libertad_condicional_COMPUTO_INTEGRAL = self._libertad_condicional_REQUISITO_CALIF_BUENO

    def _CalcularSalidasTransitorias(self):        
        
        _computo_salidas_transitorias = self._fecha_de_detencion        
        _requisito_salidas_transitorias = MontoDePena()        

        if self._regimen_normativo._regimen_ST == ST_REGIMENES._DecretoLey412_58.value or self._regimen_normativo._regimen_ST == ST_REGIMENES._Ley_24660.value or self._regimen_normativo._regimen_ST == ST_REGIMENES._Ley_25948.value:            
            
            _requisito_salidas_transitorias = self._Calcular_la_mitad(self._monto_de_pena)
            _computo_salidas_transitorias = self._SumarMontoDePena(_computo_salidas_transitorias, _requisito_salidas_transitorias)

            # Resta otras detenciones, si hay
            print(f'DEBUG: Cómputo Salidas transitorias sin restar otras detenciones = {Datetime_date_enFormatoXX_XX_XXXX(_computo_salidas_transitorias)}')        
            _computo_salidas_transitorias = self._RestarOtrasDetenciones(_computo_salidas_transitorias, self._otras_detenciones)

            # Aplica el estímulo educativo, si hay
            print(f'DEBUG: Cómputo Salidas Transitorias sin aplicar estímulo educativo = {Datetime_date_enFormatoXX_XX_XXXX(_computo_salidas_transitorias)}')
            _computo_salidas_transitorias = self._AplicarEstimuloEducativo(_computo_salidas_transitorias, self._estimulo_educativo)

            # Aplica la información obtenida a las variables de datos
            self._salidas_transitorias_COMPUTO = _computo_salidas_transitorias
            self._salidas_transitorias_REQUISITO_TEMPORAL = _requisito_salidas_transitorias
            self._salidas_transitorias_27375_SITUACION = ST_COMPUTO_27375_SITUACION.ES_ANTERIOR_A_LEY_27375.value
        
        if  self._regimen_normativo._regimen_ST == ST_REGIMENES._Ley_27375.value:

            self._CalcularRequisitoTemporal_PeriodoDePrueba()

            if self._fecha_ingreso_a_periodo_de_prueba == 'NULL':
                # Si todavía no está en periodo de prueba:
                # Calcula la fecha mínima, y el requisito temporal para poder ingresar al periodo de prueba                

                print(f'DEBUG: Cómputo Salidas transitorias (periodo de prueba) sin restar otras detenciones = {Datetime_date_enFormatoXX_XX_XXXX(self._salidas_transitorias_COMPUTO_PERIODO_DE_PRUEBA)}')
                self._salidas_transitorias_COMPUTO_PERIODO_DE_PRUEBA = self._RestarOtrasDetenciones(self._salidas_transitorias_COMPUTO_PERIODO_DE_PRUEBA, self._otras_detenciones)

                print(f'DEBUG: Cómputo Salidas transitorias (periodo de prueba) sin aplicar estímulo educativo = {Datetime_date_enFormatoXX_XX_XXXX(self._salidas_transitorias_COMPUTO_PERIODO_DE_PRUEBA)}')
                self._salidas_transitorias_COMPUTO_PERIODO_DE_PRUEBA = self._AplicarEstimuloEducativo(self._salidas_transitorias_COMPUTO_PERIODO_DE_PRUEBA, self._estimulo_educativo)
                self._salidas_transitorias_27375_SITUACION = ST_COMPUTO_27375_SITUACION.TODAVIA_NO_INGRESO_A_PERIODO_DE_PRUEBA.value

                # Calcula el requisito temporal de las Salidas Transitorias en función del requisito temporal para ingresar la periodo de prueba
                self._salidas_transitorias_REQUISITO_TEMPORAL=self._CalcularRequisitoTemporal_SalidasTransitorias_Ley27375()                
                self._salidas_transitorias_REQUISITO_TEMPORAL_INTEGRAL = deepcopy(self._salidas_transitorias_REQUISITO_TEMPORAL_PERIODO_DE_PRUEBA)
                self._salidas_transitorias_REQUISITO_TEMPORAL_INTEGRAL.años += self._salidas_transitorias_REQUISITO_TEMPORAL.años
                self._salidas_transitorias_REQUISITO_TEMPORAL_INTEGRAL.meses += self._salidas_transitorias_REQUISITO_TEMPORAL.meses

                # Con el requisito temporal de las salidas transitorias, calcula el cómputo
                self._salidas_transitorias_COMPUTO = self._SumarMontoDePena(self._fecha_de_detencion, self._salidas_transitorias_REQUISITO_TEMPORAL_INTEGRAL)                

                # Calcula cuándo debe obtenerse la conducta ejemplar (resta un año al cómputo)
                self._salidas_transitorias_REQUISITO_CALIF_EJEMPLAR = self._salidas_transitorias_COMPUTO
                self._salidas_transitorias_REQUISITO_CALIF_EJEMPLAR -= relativedelta(years=1)

                # Calcula cuándo debe obtenerse la calificación "Bueno" para lograr los 2/3
                self._CalcularSalidasTransitorias_RequisitoCalificacionBUENO()

            else:
                # Si ya está en periodo de prueba:
                # Calcula el cómputo (guarda el cálculo sin restar otras detenciones ni aplicar estímulo educativo
                # en otra variable, para que elija el usuario si lo computa doble, o no)
                
                # Calcula el requisito temporal de las salidas transitorias, teniendo en cuenta la fecha de ingreso al
                # periodo de prueba
                self._salidas_transitorias_REQUISITO_TEMPORAL = self._CalcularRequisitoTemporal_SalidasTransitorias_Ley27375()                

                # Hace el cómputo de las salidas transitorias y lo guarda en la variable sin restar
                requisito_temporal = self._salidas_transitorias_REQUISITO_TEMPORAL.años + self._salidas_transitorias_REQUISITO_TEMPORAL.meses + self._salidas_transitorias_REQUISITO_TEMPORAL.dias
                if requisito_temporal != 0:
                    self._salidas_transitorias_COMPUTO = self._SumarMontoDePena(self._fecha_ingreso_a_periodo_de_prueba, self._salidas_transitorias_REQUISITO_TEMPORAL)
                # self._salidas_transitorias_COMPUTO = self._fecha_ingreso_a_periodo_de_prueba
                # self._salidas_transitorias_COMPUTO += relativedelta(years=self._salidas_transitorias_REQUISITO_TEMPORAL.años)
                # self._salidas_transitorias_COMPUTO += relativedelta(months=self._salidas_transitorias_REQUISITO_TEMPORAL.meses)

                if self._vuelve_a_restar_otras_detenciones_y_140_en_ST:
                    # Resta otras detenciones
                    self._salidas_transitorias_COMPUTO = self._RestarOtrasDetenciones(self._salidas_transitorias_COMPUTO, self._otras_detenciones)

                    # Aplica estímulo educativo
                    self._salidas_transitorias_COMPUTO = self._AplicarEstimuloEducativo(self._salidas_transitorias_COMPUTO, self._estimulo_educativo)

                # Calcula cuándo debe obtenerse la conducta ejemplar (resta un año al cómputo)
                self._salidas_transitorias_REQUISITO_CALIF_EJEMPLAR = self._salidas_transitorias_COMPUTO
                self._salidas_transitorias_REQUISITO_CALIF_EJEMPLAR -= relativedelta(years=1)

                # Calcula cuándo debe obtenerse la calificación "Bueno" para lograr los 2/3
                self._CalcularSalidasTransitorias_RequisitoCalificacionBUENO()

                self._salidas_transitorias_27375_SITUACION = ST_COMPUTO_27375_SITUACION.HAY_COMPUTO.value
    
    def _CalcularSalidasTransitorias_RequisitoCalificacionBUENO(self):

        # Guarda los resultados en:
            #   self._salidas_transitorias_REQUISITO_CALIFICACION_BUENO
            #   self._salidas_transitorias_REQUISITO_CALIFICACION_SITUACION
        
        _fechaST = self._salidas_transitorias_COMPUTO
        _fechaInicioEjecucion = self._fecha_inicio_ejecucion
        _fechaCalificacionBueno = self._fecha_calificacion_BUENO
        self._salidas_transitorias_REQUISITO_CALIF_SITUACION = 0

        if _fechaInicioEjecucion == 'NULL':
            # SITUACIÓN 1
            # SI TODAVÍA NO COMENZÓ LA EJECUCIÓN DE PENA
            # En este caso no es posible calcular el requisito
            
            self._libertad_condicional_REQUISITO_CALIF_SITUACION = 1
            return
        
        elif _fechaInicioEjecucion != 'NULL' and _fechaCalificacionBueno == 'NULL':
            # SITUACIÓN 2
            # SI COMENZÓ LA EJECUCIÓN DE PENA PERO AÚN NO CALIFICÓ COMO "BUENO"
            # Determina la fecha límite para obtener el requisito "BUENO" teniendo en cuenta el requisito temporal LC en el caso concreto            
            
            delta = relativedelta(_fechaST, _fechaInicioEjecucion)
            pena1_3=MontoDePena(_años=delta.years, _meses=delta.months, _dias=delta.days)
            pena1_3 = self._Calcular_un_tercio(pena1_3)            
            self._salidas_transitorias_REQUISITO_CALIF_BUENO = self._SumarMontoDePena(_fechaInicioEjecucion, pena1_3)
            self._salidas_transitorias_REQUISITO_CALIF_SITUACION = 2            
            return

        elif _fechaInicioEjecucion != 'NULL' and _fechaCalificacionBueno != 'NULL':
            # SITUACIÓN 3
            # SI SE ENCEUNTRA EJECUTANDO PENA Y TIENE REQUISITO DE CALIFICACIÓN "BUENO"
            # Determina la fecha desde la que se encontrará cumplido el requisito de calificación

            self._salidas_transitorias_REQUISITO_CALIF_SITUACION = 3            
            delta = relativedelta(_fechaCalificacionBueno, _fechaInicioEjecucion)
            delta_TAMD = TiempoEn_Años_Meses_Dias(_años=delta.years, _meses=delta.months, _dias=delta.days)
            delta_x_3 = self._Multiplicar_Tiempo(delta_TAMD, 3)
            self._salidas_transitorias_REQUISITO_CALIF_BUENO = self._SumarMontoDePena(_fechaInicioEjecucion, delta_x_3)
            self._salidas_transitorias_REQUISITO_CALIF_SITUACION = 3            
            return

    def _CalcularRequisitoTemporal_PeriodoDePrueba(self):
                
        self._salidas_transitorias_REQUISITO_TEMPORAL_PERIODO_DE_PRUEBA = self._Calcular_la_mitad(self._monto_de_pena)
        self._salidas_transitorias_COMPUTO_PERIODO_DE_PRUEBA = self._SumarMontoDePena(self._fecha_de_detencion, self._salidas_transitorias_REQUISITO_TEMPORAL_PERIODO_DE_PRUEBA)        
    
    def _CalcularRequisitoTemporal_SalidasTransitorias_Ley27375(self):
        '''DEVUELVE CUANTOS MESES O AÑOS HAY QUE SUMARLE AL PERIODO DE PRUEBA PARA OBTENER LAS SALIDAS TRANSITORIAS'''
        reqASumar=TiempoEn_Años_Meses_Dias()                
        if MontoDeTiempoA_es_Mayor_que_MontoDeTiempoB(self._monto_de_pena, TiempoEn_Años_Meses_Dias(_años=10)):
            reqASumar.años = 1                    
        elif MontoDeTiempoA_es_Mayor_que_MontoDeTiempoB(self._monto_de_pena, TiempoEn_Años_Meses_Dias(_años=5)):
            reqASumar.meses = 6 
        return reqASumar
    
    def _CalcularSalidasTransitorias_RequisitoConductaEJEMPLAR(self):
        if self._fecha_calificacion_EJEMPLAR == 'NULL':
        # SI AÚN NO CONSIGUIÓ LA CALIFICACIÓN EJEMPLAR:
            if self._fecha_ingreso_a_periodo_de_prueba == 'NULL':
                # SI NO TIENE CONDUCTA EJEMPLAR NI INGRESÓ AL PERIODO DE PRUEBA:
                # Calcula la fecha en que habría que tener el requisito de calificación para poder
                # aprovechar la eventual mejor situación

                # Calcula el requisito potencial de las ST (si se alcanza en tiempo el periodo de prueba)
                self._salidas_transitorias_REQUISITO_CALIF_EJEMPLAR = self._SumarMontoDePena(self._salidas_transitorias_COMPUTO_PERIODO_DE_PRUEBA, self._CalcularRequisitoTemporal_SalidasTransitorias_Ley27375())
                # A esa fecha le resta un año
                self._salidas_transitorias_REQUISITO_CALIF_EJEMPLAR -= relativedelta(years=1)
            else:
                # SI NO TIENE CONDUCTA EJEMPLAR, PERO INGRESÓ AL PERIODO DE PRUEBA, ENTONCES TIENE
                # CÓMPUTO DE SALIDAS TRANSITORIAS:
                # En ese caso solamente se le resta un año a ese cómputo
                self._salidas_transitorias_REQUISITO_CALIF_EJEMPLAR = self._salidas_transitorias_COMPUTO
                self._salidas_transitorias_REQUISITO_CALIF_EJEMPLAR -= relativedelta(years=1)
        else:
        # SI YA TIENE FECHA DE CALIFICACIÓN EJEMPLAR:
        # Calcula desde cuándo se podrán obtener las salidas transitorias, según ese requisito (sin contemplar
        # los otros requisitos de la ST. Esos se valorarán en el cómputo integral)
            self._salidas_transitorias_REQUISITO_CALIF_EJEMPLAR = self._fecha_calificacion_EJEMPLAR
            self._salidas_transitorias_REQUISITO_CALIF_EJEMPLAR += relativedelta(years=1)

    def _CalcularLibertadAsistida(self):
        
        # Utiliza las siguientes variables:
        # - _vencimientoDePena

        _computo_libertad_asistida = ''                
        
        if self._regimen_normativo._regimen_LA == LA_REGIMENES._Ley_24660.value or self._regimen_normativo._regimen_LA == LA_REGIMENES._Ley_25948.value:

            _computo_libertad_asistida = self._vencimiento_de_pena
            _computo_libertad_asistida += relativedelta(months=-6)            
        
        if self._regimen_normativo._regimen_LA == LA_REGIMENES._Ley_27375.value:

            _computo_libertad_asistida = self._vencimiento_de_pena
            _computo_libertad_asistida += relativedelta(months=-3)            
        
        # No se resta acá las otras detenciones porque ya fueron restadas en el vencimiento de pena

        print(f'DEBUG: Libertad asistida sin aplicar estímulo educativo = {Datetime_date_enFormatoXX_XX_XXXX(_computo_libertad_asistida)}')
        # Aplica el estímulo educativo, si hay
        _computo_libertad_asistida = self._AplicarEstimuloEducativo(_computo_libertad_asistida, self._estimulo_educativo)        

        # Guarda el dato en la variable correspondiente
        self._libertad_asistida_COMPUTO = _computo_libertad_asistida

    def _ImprimirSTRINGGeneral(self):
        print('')
        print('DATOS INGRESADOS')
        print('----------------')
        print(f' - Fecha del hecho: {Datetime_date_enFormatoXX_XX_XXXX(self._fecha_del_hecho)}')
        print(f' - Fecha de detención: {Datetime_date_enFormatoXX_XX_XXXX(self._fecha_de_detencion)}')
        
        if self._monto_de_pena.perpetua:
            print(' - Es una pena perpetua.')
        else:
            print(f' - La pena es de {self._monto_de_pena.años} año(s), {self._monto_de_pena.meses} mes(es) y {self._monto_de_pena.dias} día(s).')
        if self._monto_de_pena.reincidencia:
            print('    - Es reincidente.')
        if self._monto_de_pena.ejecucionCondicional:
            print('    - Es de ejecución condicional.')
            print(f'    - El plazo de control es de {self._monto_de_pena.plazoControl_años} año(s), {self._monto_de_pena.plazoControl_meses} mes(es) y {self._monto_de_pena.plazoControl_dias} día(s).')
        if self._monto_de_pena.reclusionPorTiempoIndeterminado:
            print('    - Hay accesoria de reclusión por tiempo indeterminado.')
        if self._monto_de_pena.delitosExcluidosLey25892:
            print('    - La condena es por delitos enumerados en la ley 25.892.')
        if self._monto_de_pena.delitosExcluidosLey25948:
            print('    - La condena es por delitos enumerados en la ley 25.948.')
        if self._monto_de_pena.delitosExcluidosLey27375:
            print('    - La condena es por delitos enumerados en la ley 27.375.')
        
        if self._otras_detenciones == 'NULL':
            print(' - No se ingresaron otros tiempos de detención a computar.')
        else:
            print(' - Otras detenciones a computar:')
            for detencion in self._otras_detenciones:
                print(f'    - "{detencion._nombre}": {detencion._tiempoDeDetencion.años} año(s), {detencion._tiempoDeDetencion.meses} mes(es) y {detencion._tiempoDeDetencion.dias} día(s).')

        estimulo_educativo = self._estimulo_educativo.años + self._estimulo_educativo.meses + self._estimulo_educativo.dias
        if estimulo_educativo == 0:
            print(' - No se ingresó tiempo a descontar por aplicación del estímulo educativo.')
        else:
            print(f' - El estímulo educativo a descontar es de {self._estimulo_educativo.años} año(s), {self._estimulo_educativo.meses} mes(es) y {self._estimulo_educativo.dias} día(s).')
        
        if self._regimen_normativo._regimen_LC == LC_REGIMENES._Ley_27375.value or self._regimen_normativo._regimen_ST == ST_REGIMENES._Ley_27375.value:
            if self._fecha_inicio_ejecucion == 'NULL':
                print(' - No se ingresó fecha de inicio de ejecución (o de REAV).')
            else:
                print(f' - Fecha de inicio de ejecución (o de REAV): {Datetime_date_enFormatoXX_XX_XXXX(self._fecha_inicio_ejecucion)}')
            
            if self._fecha_calificacion_BUENO == 'NULL':
                print(' - No se ingresó fecha en la que se adquirió la calificación "BUENO".')
            else:
                print(f' - Fecha en la que se adquirió la calificación "BUENO": {Datetime_date_enFormatoXX_XX_XXXX(self._fecha_calificacion_BUENO)}')
            
            if self._fecha_calificacion_EJEMPLAR == 'NULL':
                print(' - No se ingresó fecha en la que se adquirió la calificación "EJEMPLAR".')
            else:
                print(f' - Fecha en la que se adquirió la calificación "EJEMPLAR": {Datetime_date_enFormatoXX_XX_XXXX(self._fecha_calificacion_EJEMPLAR)}')
            
            if self._fecha_ingreso_a_periodo_de_prueba == 'NULL':
                print(' - No se ingresó fecha en la que se ingresó al periodo de prueba.')
            else:
                print(f' - Fecha en la que se ingresó al periodo de prueba: {Datetime_date_enFormatoXX_XX_XXXX(self._fecha_ingreso_a_periodo_de_prueba)}')

            if self._otras_detenciones != 'NULL' or estimulo_educativo != 0:
                if self._vuelve_a_restar_otras_detenciones_y_140_en_ST == True:
                    print(' - Para el cálculo de las salidas transitorias se va a computar estímulo educativo y/o se van a restar las otras detenciones ingresadas, tanto para el requisito temporal del periodo de prueba, como para el de las salidas transitorias.')
                else:
                    print(' - Para el cálculo de las salidas transitorias se va a computar estímulo educativo y/o se van a restar las otras detenciones ingresadas, solamente para el requisito temporal del periodo de prueba.')
            
    def _ImprimirSTRINGVencimientoYCaducidadDePena(self):
        print('')
        print('VENCIMIENTO Y CADUCIDAD')
        print('-----------------------')
        print(f' - Vencimiento de la pena: {Datetime_date_enFormatoXX_XX_XXXX(self._vencimiento_de_pena)}')
        print(f' - Caducidad de la pena: {Datetime_date_enFormatoXX_XX_XXXX(self._caducidad_de_pena)}')
    
    def _ImprimirSTRINGLibertadCondicional(self):        
        print('')
        print('LIBERTAD CONDICIONAL')
        print('--------------------')
        print(f' - La libertad condicional se obtiene a los {self._libertad_condicional_REQUISITO_TEMPORAL.años} año(s), {self._libertad_condicional_REQUISITO_TEMPORAL.meses} mes(es) y {self._libertad_condicional_REQUISITO_TEMPORAL.dias} día(s).')
        print(f' - El requisito temporal para acceder a la libertad condicional se cumple el {Datetime_date_enFormatoXX_XX_XXXX(self._libertad_condicional_COMPUTO)}')        
        
        # Imprime advertencias, si corresponde
        if self._monto_de_pena.reincidencia:
            print('ADVERTENCIA: No aplicaría el instituto de la Libertad Condicional porque la pena incluye reincidencia.')            
        
        if self._regimen_normativo._regimen_LC == LC_REGIMENES._Ley_27375.value and self._monto_de_pena.delitosExcluidosLey27375:
            print('ADVERTENCIA: No aplicaría el instituto de la Libertad Condicional porque se condenó por alguno de los delitos excluídos, por art. 14 CP (según reforma de la ley 27.375).')            
        
        if self._regimen_normativo._regimen_LC == LC_REGIMENES._Ley_27375.value:
            if self._libertad_condicional_REQUISITO_CALIF_SITUACION == 1:
                print('Como no se cuenta con la fecha en la que se inició la ejecución de la pena, no es posible calcular el requisito temporal de calificación (art. 28, ley 24.660).')
            if self._libertad_condicional_REQUISITO_CALIF_SITUACION == 2:
                print(f' - Teniendo en cuenta que se comenzó a ejecutar la pena el día {Datetime_date_enFormatoXX_XX_XXXX(self._fecha_inicio_ejecucion)}, para acceder a la libertad condicional en la fecha indicada, la fecha límite para obtener el requisito de calificación "bueno" es {Datetime_date_enFormatoXX_XX_XXXX(self._libertad_condicional_REQUISITO_CALIF_BUENO)}.')
            if self._libertad_condicional_REQUISITO_CALIF_SITUACION == 3:
                print(f' - Teniendo en cuenta que se comenzó a ejecutar la pena el día {Datetime_date_enFormatoXX_XX_XXXX(self._fecha_inicio_ejecucion)} y que se obtuvo el requisito de calificación "bueno" el día {Datetime_date_enFormatoXX_XX_XXXX(self._fecha_calificacion_BUENO)}, los 2/3 de pena con calificación "bueno" se cumplirán el día {self._libertad_condicional_REQUISITO_CALIF_BUENO}.')

    def _ImprimirSTRINGSalidasTransitorias(self):
        print('')
        print('SALIDAS TRANSITORIAS')
        print('--------------------')

        if self._regimen_normativo._regimen_ST == ST_REGIMENES._DecretoLey412_58.value or self._regimen_normativo._regimen_ST == ST_REGIMENES._Ley_24660.value or self._regimen_normativo._regimen_ST == ST_REGIMENES._Ley_25948.value:
            print(f' - Las salidas transitorias se obtienen a los {self._salidas_transitorias_REQUISITO_TEMPORAL.años} año(s), {self._salidas_transitorias_REQUISITO_TEMPORAL.meses} mes(es) y {self._salidas_transitorias_REQUISITO_TEMPORAL.dias} día(s).')
            print(f' - El requisito temporal para acceder a las salidas transitorias se cumple el {Datetime_date_enFormatoXX_XX_XXXX(self._salidas_transitorias_COMPUTO)}')
            
            if self._regimen_normativo.SALIDAS_TRANSITORIAS(ST_KEYS._ask_delitosExcluidos25948_KEY):
                if self._monto_de_pena.delitosExcluidosLey25948:
                    print(' - ADVERTENCIA: La salida transitoria no sería aplicable en función de que la condena es por uno de los delitos enumerados en el art. 56 bis, ley 24.660.')            
        
        if  self._regimen_normativo._regimen_ST == ST_REGIMENES._Ley_27375.value:            

            if self._fecha_ingreso_a_periodo_de_prueba == 'NULL': # Caso en el que aún no se ingresó al periodo de prueba
                # Indica el requisito para ingresar al periodo de prueba
                print(f' - Para ingresar al periodo de prueba se requiere un tiempo mínimo de detención de {self._salidas_transitorias_REQUISITO_TEMPORAL_PERIODO_DE_PRUEBA.años} año(s), {self._salidas_transitorias_REQUISITO_TEMPORAL_PERIODO_DE_PRUEBA.meses} mes(es) y {self._salidas_transitorias_REQUISITO_TEMPORAL_PERIODO_DE_PRUEBA.dias} día(s).')
                print(f' - El requisito temporal para ingresar al periodo de prueba se cumple el {Datetime_date_enFormatoXX_XX_XXXX(self._salidas_transitorias_COMPUTO_PERIODO_DE_PRUEBA)}')

                # Indica el requisito hipotético para las salidas transitorias
                if self._salidas_transitorias_REQUISITO_TEMPORAL.años == 1:
                    print(' - Como la pena es mayor a 10 años, las salidas transitorias podrían obtenerse luego de 1 año del ingreso al periodo de prueba.')
                    print(f' - El requisito temporal para acceder a las salidas transitorias se cumpliría el {Datetime_date_enFormatoXX_XX_XXXX(self._salidas_transitorias_COMPUTO)}')
                elif self._salidas_transitorias_REQUISITO_TEMPORAL.meses == 6:
                    print(' - Como la pena es mayor a 5 años -y no es mayor a 10 años-, las salidas transitorias podrían obtenerse luego de 6 meses del ingreso al periodo de prueba.')
                    print(f' - El requisito temporal para acceder a las salidas transitorias se cumpliría el {Datetime_date_enFormatoXX_XX_XXXX(self._salidas_transitorias_COMPUTO)}')
                else:
                    print(' - Como la pena no es mayor a 5 años, las salidas transitorias podrían obtenerse desde el ingreso al periodo de prueba.')
                
                # Indica el requisito de calificación "ejemplar"
                print(f' - Para acceder a las salidas transitorias en esa fecha, la fecha límite para obtener conducta "Ejemplar" es el {Datetime_date_enFormatoXX_XX_XXXX(self._salidas_transitorias_REQUISITO_CALIF_EJEMPLAR)}')
                
                # Indica el requisito de calificación "bueno"
                if self._salidas_transitorias_REQUISITO_CALIF_SITUACION == 1:
                    print(' - Como no se cuenta con la fecha en la que se inició la ejecución de la pena, no es posible calcular fechas en relación al requisito de calificación "bueno" del art. 17.III, ley 24.660.')
                if self._salidas_transitorias_REQUISITO_CALIF_SITUACION == 2:
                    print(f' - Teniendo en cuenta que se comenzó a ejecutar la pena el día {Datetime_date_enFormatoXX_XX_XXXX(self._fecha_inicio_ejecucion)}, para acceder a las salidas transitorias en la fecha indicada, la fecha límite para obtener el requisito de calificación "bueno" es {Datetime_date_enFormatoXX_XX_XXXX(self._salidas_transitorias_REQUISITO_CALIF_BUENO)}.')
                if self._salidas_transitorias_REQUISITO_CALIF_SITUACION == 3:
                    print(f' - Teniendo en cuenta que se comenzó a ejecutar la pena el día {Datetime_date_enFormatoXX_XX_XXXX(self._fecha_inicio_ejecucion)} y que se obtuvo el requisito de calificación "bueno" el día {Datetime_date_enFormatoXX_XX_XXXX(self._fecha_calificacion_BUENO)}, los 2/3 de pena con calificación "bueno" se cumplirán el día {self._salidas_transitorias_REQUISITO_CALIF_BUENO}.')                   

                fecha_mayor = Comparar_fechas_y_devolver_la_mayor(self._salidas_transitorias_COMPUTO, self._salidas_transitorias_REQUISITO_CALIF_EJEMPLAR, self._fecha_calificacion_BUENO)                                
                print(f' - En este contexto, y teniendo en cuenta las fechas de cada requisito, las salidas transitorias podrían obtenerse el día {Datetime_date_enFormatoXX_XX_XXXX(fecha_mayor)}.')
            
            else: # Caso en el que se ingresó al periodo de prueba
                print (f' - Se ingresó al periodo de prueba el día: {Datetime_date_enFormatoXX_XX_XXXX(self._fecha_ingreso_a_periodo_de_prueba)}.')

                # Indica el requisito hipotético para las salidas transitorias
                if self._salidas_transitorias_REQUISITO_TEMPORAL.años == 1:
                    print(' - Como la pena es mayor a 10 años, las salidas transitorias podrían obtenerse luego de 1 año del ingreso al periodo de prueba.')
                    print(f' - El requisito temporal para acceder a las salidas transitorias se cumple el día {Datetime_date_enFormatoXX_XX_XXXX(self._salidas_transitorias_COMPUTO)}')
                elif self._salidas_transitorias_REQUISITO_TEMPORAL.meses == 6:
                    print(' - Como la pena es mayor a 5 años -y no es mayor a 10 años-, las salidas transitorias podrían obtenerse luego de 6 meses del ingreso al periodo de prueba.')
                    print(f' - El requisito temporal para acceder a las salidas transitorias se cumple el día {Datetime_date_enFormatoXX_XX_XXXX(self._salidas_transitorias_COMPUTO)}')
                else:
                    print(' - Como la pena no es mayor a 5 años, las salidas transitorias podrían obtenerse desde el ingreso al periodo de prueba.')
                
                # Indica el requisito de calificación "ejemplar"
                print(f' - Para acceder a las salidas transitorias en esa fecha, la fecha límite para obtener conducta "Ejemplar" es el {Datetime_date_enFormatoXX_XX_XXXX(self._salidas_transitorias_REQUISITO_CALIF_EJEMPLAR)}')
                
                # Indica el requisito de calificación "bueno"
                if self._salidas_transitorias_REQUISITO_CALIF_SITUACION == 1:
                    print(' - Como no se cuenta con la fecha en la que se inició la ejecución de la pena, no es posible calcular fechas en relación al requisito de calificación "bueno" del art. 17.III, ley 24.660.')
                if self._salidas_transitorias_REQUISITO_CALIF_SITUACION == 2:
                    print(f' - Teniendo en cuenta que se comenzó a ejecutar la pena el día {Datetime_date_enFormatoXX_XX_XXXX(self._fecha_inicio_ejecucion)}, para acceder a las salidas transitorias en la fecha indicada, la fecha límite para obtener el requisito de calificación "bueno" es {Datetime_date_enFormatoXX_XX_XXXX(self._salidas_transitorias_REQUISITO_CALIF_BUENO)}.')
                if self._salidas_transitorias_REQUISITO_CALIF_SITUACION == 3:
                    print(f' - Teniendo en cuenta que se comenzó a ejecutar la pena el día {Datetime_date_enFormatoXX_XX_XXXX(self._fecha_inicio_ejecucion)} y que se obtuvo el requisito de calificación "bueno" el día {Datetime_date_enFormatoXX_XX_XXXX(self._fecha_calificacion_BUENO)}, los 2/3 de pena con calificación "bueno" se cumplirán el día {self._salidas_transitorias_REQUISITO_CALIF_BUENO}.')                   

                fecha_mayor = Comparar_fechas_y_devolver_la_mayor(self._salidas_transitorias_COMPUTO, self._salidas_transitorias_REQUISITO_CALIF_EJEMPLAR, self._fecha_calificacion_BUENO)                                
                print(f' - En este contexto, y teniendo en cuenta las fechas de cada requisito, las salidas transitorias podrían obtenerse el día {Datetime_date_enFormatoXX_XX_XXXX(fecha_mayor)}.')

        # Imprime advertencias, si corresponde
        if self._regimen_normativo._regimen_ST == ST_REGIMENES._Ley_25948.value and self._monto_de_pena.delitosExcluidosLey25948:
            print('ADVERTENCIA: No aplicaría el instituto de las Salidas Transitorias porque se condenó por alguno de los delitos excluídos, por art. 56 bis, ley 24.660 (según reforma de la ley 25.948).')            
        
        if self._regimen_normativo._regimen_ST == ST_REGIMENES._Ley_27375.value and self._monto_de_pena.delitosExcluidosLey27375:
            print('ADVERTENCIA: No aplicaría el instituto de las Salidas Transitorias porque se condenó por alguno de los delitos excluídos, por art. 56 bis -17.III-, ley 24.660 (según reforma de la ley 27.375).')            

    def _ImprimirSTRINGLibertadAsistida(self):
        print('')
        print('LIBERTAD ASISTIDA')
        print('-----------------')
        if self._regimen_normativo._regimen_LA == LA_REGIMENES._Ley_27375.value:            
            print(f' - La libertad asistida se obtiene 3 meses antes del vencimiento de pena.')
        else:
            print(f' - La libertad asistida se obtiene 6 meses antes del vencimiento de pena.')
        print(f' - El requisito temporal para acceder a la libertad asistida se cumple el {Datetime_date_enFormatoXX_XX_XXXX(self._libertad_asistida_COMPUTO)}')

        # Imprime advertencias, si correponde
        if self._regimen_normativo._regimen_LA == LA_REGIMENES._Ley_25948.value and self._monto_de_pena.delitosExcluidosLey25948:
            print('ADVERTENCIA: No aplicaría el instituto de la Libertad Asistida porque se condenó por alguno de los delitos excluídos, por art. 56 bis, ley 24.660 (según reforma de la ley 25.948).')
        
        if self._regimen_normativo._regimen_LA == LA_REGIMENES._Ley_27375.value and self._monto_de_pena.delitosExcluidosLey27375:
            print('ADVERTENCIA: No aplicaría el instituto de la Libertad Asistida porque se condenó por alguno de los delitos excluídos, por art. 56 bis, ley 24.660 (según reforma de la ley 27.375).')

    def _ArmarSTRINGRegimenPreparatorioParaLaLiberacion(self):
        pass

class ComputoDePena_VIEJO():    
    def __init__(self, fechaDelHecho:datetime.date='NULL',
    fechaDeDetencion:datetime.date='NULL',
    fechaDeSentencia:datetime.date='NULL',
    montoDePena:MontoDePena='NULL',
    fechaFirmezaDeSentencia:datetime.date='NULL',
    fechaComienzoEjecucion:datetime.date='NULL',
    otrosTiemposDeDetencion='NULL',
    situacionProcesal:SituacionProcesal=None,
    esComputoPorLCRevocada:bool=False,
    esComputoPorSTRevocada:bool=False,
    esComputoPorLARevocada:bool=False,
    estimuloEducativo:TiempoEn_Años_Meses_Dias='NULL',
    fechaCalificacionBUENO:datetime.date='NULL',
    libertadCondicionalEnComputoAnterior:datetime.date='NULL',
    vencimientoDePenaEnComputoAnterior:datetime.date='NULL',
    nuevaFechaDeDetencion:datetime.date='NULL',
    tiempoParcialEnLCAComputar:OtraDetencion='NULL',
    fechaIngresoAPeriodoDePrueba:datetime.date='NULL',
    fechaCalificacionEJEMPLAR:datetime.date='NULL'):

        # DEFINE LAS VARIABLES QUE DEPENDEN DE LOS PARÁMETROS INGRESADOS
            # Parámetros comunes a todos los casos
        self._fecha_del_hecho = fechaDelHecho
        self._fecha_de_sentencia = fechaDeSentencia
        self._fecha_de_firmeza_de_sentencia = fechaFirmezaDeSentencia
        self._fecha_comienzo_ejecucion = fechaComienzoEjecucion
        self._fecha_de_detencion = fechaDeDetencion
        self._monto_de_pena = montoDePena
        self._otros_tiempos_de_detencion = otrosTiemposDeDetencion 
        self._situacionProcesal = situacionProcesal
            # Estímulo educativo
        self._estimulo_educativo = TiempoEn_Años_Meses_Dias()
        if estimuloEducativo != 'NULL':
            self._estimulo_educativo = estimuloEducativo
            # Régimen ley 27.375
        self._fecha_calificacion_BUENO = fechaCalificacionBUENO
        self._fecha_calificacion_EJEMPLAR =fechaCalificacionEJEMPLAR
        self._fecha_ingreso_a_periodo_de_prueba = fechaIngresoAPeriodoDePrueba
            # Nuevo cómputo por libertades revocadas
        self._es_computo_por_LC_revocada = esComputoPorLCRevocada
        self._es_computo_por_ST_revocada = esComputoPorSTRevocada
        self._es_computo_por_LA_revocada = esComputoPorLARevocada
        self._libertad_condicional_en_computo_anterior = libertadCondicionalEnComputoAnterior
        self._vencimiento_de_pena_en_computo_anterior = vencimientoDePenaEnComputoAnterior
        self._nueva_fecha_de_detencion = nuevaFechaDeDetencion
        self._tiempo_parcial_en_LC_a_computar = tiempoParcialEnLCAComputar
        self._tiempo_que_permanecio_en_libertad = TiempoEn_Años_Meses_Dias()

        if self.__CorregirProblemasEnElIngresoDeParametros() == 'RETURN':
            return

        # DEFINE VARIABLES INTERNAS
        self.requisito27CP = TiempoEn_Años_Meses_Dias(_años=4)
        self.requisito51CP_EjecCond  = TiempoEn_Años_Meses_Dias(_años=10)

        # DEFINE LAS VARIABLES PARA EL OUTPUT
        # Vencimiento de pena
        self._vencimiento_de_pena = ''
        self._vencimiento_de_pena_sinRestarOtrasDetenciones = ''
        self._caducidad_de_la_pena = ''
        self._caducidad_de_la_pena_sinRestarOtrasDetenciones = ''
        self._vencimiento_plazo_de_control = ''
        self._vencimiento_y_caducidad_STRING = 'VENCIMIENTO Y CADUCIDAD STRING'
        self._vencimiento_y_caducidad_STRING_SROT = 'VENCIMIENTO Y CADUCIDAD STRING SIN RESTAR OTRAS DETENCIONES'

        self._computo_libertad_condicional = ''
        self._computo_libertad_condicional_sinRestarOtrasDetenciones = ''
        self._computo_integral_libertad_condicional = ''
        self._requisito_libertad_condicional = MontoDePena()        
        self._requisitoCalificacion_libertad_condicional = ''
        self._requisitoCalificacion_libertad_condicional_SITUACION = ''
        self._libertad_condicional_STRING = 'LIBERTAD CONDICIONAL STRING'
        self._libertad_condicional_STRING_SROT = 'LIBERTAD CONDICIONAL STRING SIN RESTAR OTRAS DETENCIONES'

        self._computo_salidas_transitorias = ''
        self._computo_salidas_transitorias_SITUACION = ST_COMPUTO_27375_SITUACION.NO_HAY_COMPUTO_CALCULADO.value
        self._computo_salidas_transitorias_sinRestarOtrasDetenciones = ''
        self._requisito_salidas_transitorias = MontoDePena()
        self._requisito_temporal_periodo_de_prueba = ''
        self._salidas_transitorias_STRING = 'SALIDAS TRANSITORIAS STRING'

        self._computo_libertad_asistida = ''
        self._computo_libertad_asistida_sinRestarOtrasDetenciones = ''
        self._libertad_asistida_STRING = 'LIBERTAD ASISTIDA STRING'
        
        # DETERMINA EL REGIMEN NORMATIVO A UTILIZAR
        self._regimenNormativoAplicable = RegimenNormativoAplicable(self._fecha_del_hecho)        

        # CÓMPUTO DE PENA DE EJECUCIÓN CONDICIONAL
        if self._monto_de_pena.ejecucionCondicional:                        
            self._vencimiento_de_pena, self._caducidad_de_la_pena, self._vencimiento_plazo_de_control = self.__CalcularVencimientoYCaducidadDePena_EjecucionCondicional(self._fecha_de_sentencia, self._fecha_de_firmeza_de_sentencia, self._monto_de_pena)
            return
        
        # NUEVO CÓMPUTO POR LC REVOCADA
        if self._es_computo_por_LC_revocada:
            self._vencimiento_de_pena, self._caducidad_de_la_pena = self.__CalcularNuevoComputoPorLCRevocada(libertadCondicionalEnComputoAnterior, vencimientoDePenaEnComputoAnterior, nuevaFechaDeDetencion, tiempoParcialEnLCAComputar)
            # Calcular salidas transitorias (mas que nada si es ley nueva, por el requisito de calificación)
            self._computo_libertad_asistida = self.__CalcularLibertadAsistida(self._vencimiento_de_pena, self._vencimiento_de_pena)
            return
        
        # CÓMPUTO DE PENA TEMPORAL SIN RECLUSIÓN POR TIEMPO INDETERMINADO
        if not self._monto_de_pena.ejecucionCondicional and not self._monto_de_pena.perpetua and not self._monto_de_pena.reclusionPorTiempoIndeterminado:
            self._vencimiento_de_pena, self._vencimiento_de_pena_sinRestarOtrasDetenciones, self._caducidad_de_la_pena, self._caducidad_de_la_pena_sinRestarOtrasDetenciones = self.__CalcularVencimientoYCaducidadDePena_Temporal(self._fecha_de_detencion, self._monto_de_pena, self._otros_tiempos_de_detencion)
            self._computo_libertad_condicional, self._computo_libertad_condicional_sinRestarOtrasDetenciones, self._requisito_libertad_condicional = self.__CalcularLibertadCondicional(self._fecha_de_detencion, self._monto_de_pena, self._otros_tiempos_de_detencion)
            if self._regimenNormativoAplicable._regimen_LC == LC_REGIMENES._Ley_27375.value:
                self._requisitoCalificacion_libertad_condicional, self._requisitoCalificacion_libertad_condicional_SITUACION = self.__CalcularRequisitoCalificacion_LC_o_ST(self._computo_libertad_condicional, self._fecha_comienzo_ejecucion, self._fecha_calificacion_BUENO)
            self._computo_salidas_transitorias, self._computo_salidas_transitorias_sinRestarOtrasDetenciones, self._requisito_salidas_transitorias = self.__CalcularSalidasTransitorias(self._fecha_de_detencion, self._monto_de_pena, self._otros_tiempos_de_detencion, self._fecha_ingreso_a_periodo_de_prueba)
            # Calcular LA

        # self._vencimiento_de_pena, self._vencimiento_de_pena_sinRestarOtrasDetenciones, self._caducidad_de_la_pena, self._caducidad_de_la_pena_sinRestarOtrasDetenciones = self.__CalcularVencimientoYCaducidadDePena_Temporal(self._fecha_de_detencion, self._fecha_de_sentencia, self._monto_de_pena, self._otros_tiempos_de_detencion)
        # self._computo_libertad_condicional, self._computo_libertad_condicional_sinRestarOtrasDetenciones, self._requisito_libertad_condicional = self.__CalcularLibertadCondicional(self._fecha_de_detencion, self._monto_de_pena, self._otros_tiempos_de_detencion)
        # self._computo_salidas_transitorias, self._computo_salidas_transitorias_sinRestarOtrasDetenciones, self._requisito_salidas_transitorias = self.__CalcularSalidasTransitorias(self._fecha_de_detencion, self._monto_de_pena, self._otros_tiempos_de_detencion)
        # self._computo_libertad_asistida, self._computo_libertad_asistida_sinRestarOtrasDetenciones = self.__CalcularLibertadAsistida(self._vencimiento_de_pena, self._vencimiento_de_pena_sinRestarOtrasDetenciones)

    def __CorregirProblemasEnElIngresoDeParametros(self):        
        # NO SE INGRESÓ MONTO DE PENA
        if self._monto_de_pena == 'NULL':
            print('ERROR: Es imposible calcular un cómputo si no se ingresa el monto de pena')
            return 'RETURN'
        
        # SE INGRESÓ FECHA DE FIRMEZA DE SENTENCIA PERO NO SE INGRESÓ FECHA DE COMIENZO DE EJECUCIÓN
        # En ese caso ambas fechas son la misma
        if self._fecha_de_firmeza_de_sentencia != 'NULL' and self._fecha_comienzo_ejecucion == 'NULL':
            self._fecha_comienzo_ejecucion = self._fecha_de_firmeza_de_sentencia

    def __Calcular_un_tercio(self, _montoDePena:MontoDePena):
        if _montoDePena.perpetua:
            return _montoDePena
        
        TR_dos_tercios = MontoDePena()

        # Calcula 1/3 de los días, lo redondea para abajo si da con coma, y los suma
        TR_dos_tercios.dias = int(_montoDePena.dias / 3) # Hace los dos tercios y lo redondea para abajo        

        # Calcula 1/3 de los meses
        TR_dos_tercios.meses = _montoDePena.meses
        TR_dos_tercios.meses = TR_dos_tercios.meses / 3
        LC_dias_resto = 0
        if TR_dos_tercios.meses.is_integer() is False:            
            LC_dias_resto = TR_dos_tercios.meses - int(TR_dos_tercios.meses)
            if LC_dias_resto < 0:
                LC_dias_resto += 1
            TR_dos_tercios.meses = int(TR_dos_tercios.meses)
            if LC_dias_resto > 0.3 and LC_dias_resto < 0.4:
                LC_dias_resto = int(10)
            elif LC_dias_resto > 0.6 and LC_dias_resto < 0.7:
                LC_dias_resto = int(20)
            else:
                print(LC_dias_resto)
                print('ERROR: Al calcular 1/3 de los meses, los decimales no son ni 0.3333 ni 0.6666!')                    

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
            if LC_dias_resto < 0:
                LC_dias_resto += 1
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
    
    def __SumarMontoDePena(self, _fecha:datetime.date, _montoDePena:MontoDePena, _sumarPlazoControl:bool=False):
        TR_fecha = _fecha
        if _sumarPlazoControl:
            TR_fecha += relativedelta(years=_montoDePena.plazoControl_años)
            TR_fecha += relativedelta(months=_montoDePena.plazoControl_meses)
            TR_fecha += relativedelta(days=_montoDePena.plazoControl_dias)
            TR_fecha += relativedelta(days=-1)
        else:    
            TR_fecha += relativedelta(years=_montoDePena.años)
            TR_fecha += relativedelta(months=_montoDePena.meses)
            TR_fecha += relativedelta(days=_montoDePena.dias)
            TR_fecha += relativedelta(days=-1)
        return TR_fecha

    def __Multiplicar_Tiempo(self, tiempo:TiempoEn_Años_Meses_Dias, factor:int):        
        
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

    def __RestarOtrasDetenciones(self, _fecha:datetime.date, _otrasDetenciones:OtraDetencion):
        TR_fecha = _fecha
        if _otrasDetenciones != "NULL":
            TR_fecha = RestarOtrasDetenciones(TR_fecha, _otrasDetenciones)
        return TR_fecha

    def __AplicarEstimuloEducativo(self, _fecha:datetime.date, _tiempo:TiempoEn_Años_Meses_Dias):
        TR_fecha = _fecha
        TR_fecha -= relativedelta(days=_tiempo.dias)
        TR_fecha -= relativedelta(months=_tiempo.meses)
        TR_fecha -= relativedelta(years=_tiempo.años)
        return TR_fecha

    def __CalcularVencimientoYCaducidadDePena_EjecucionCondicional(self, _fechaDeSentencia:datetime.date, _fechaFirmezaDeSentencia:datetime.date, _montoDePena:MontoDePena):
        
        TR_vencimientoDePena = self.__SumarMontoDePena(_fechaDeSentencia, self.requisito27CP)
        TR_caducidad_de_la_pena = self.__SumarMontoDePena(_fechaDeSentencia, self.requisito51CP_EjecCond)        
        TR_vencimiento_plazoDeControl = self.__SumarMontoDePena(_fechaFirmezaDeSentencia, _montoDePena, _sumarPlazoControl=True)

        self._vencimiento_y_caducidad_STRING = 'COMPUTO DE PENA\n'\
                '---------------\n'\
                f'La pena es de {self._monto_de_pena.años} año(s), {self._monto_de_pena.meses} mes(es) y {self._monto_de_pena.dias} día(s) de ejecución condicional.\n'\
                f'El plazo de control es de {self._monto_de_pena.plazoControl_años} año(s), {self._monto_de_pena.plazoControl_meses} mes(es) y {self._monto_de_pena.plazoControl_dias} día(s) de ejecución condicional.\n'\
                f'Fecha de sentencia: {Datetime_date_enFormatoXX_XX_XXXX(self._fecha_de_sentencia)} (adquirió firmeza el {self._fecha_de_firmeza_de_sentencia})\n'\
                f'Se tiene por no pronunciada el día {Datetime_date_enFormatoXX_XX_XXXX(TR_vencimientoDePena)}\n'\
                f'El plazo de control finaliza el {Datetime_date_enFormatoXX_XX_XXXX(TR_vencimiento_plazoDeControl)}\n'\
                f'Caducidad: {Datetime_date_enFormatoXX_XX_XXXX(TR_caducidad_de_la_pena)}\n'

        return (TR_vencimientoDePena,        
        TR_caducidad_de_la_pena,
        TR_vencimiento_plazoDeControl)

    def __CalcularVencimientoYCaducidadDePena_Temporal(self, _fechaDeDetencion:datetime.date, _montoDePena:MontoDePena, _otrosTiemposDeDetencion="NULL"):

        TR_vencimientoDePena = ''
        TR_vencimientoDePena_sinRestarOtrasDetenciones = ''
        TR_caducidad_de_la_pena = ''
        TR_caducidad_de_la_pena_sinRestarOtrasDetenciones = ''
        
        TR_vencimientoDePena = self.__SumarMontoDePena(_fechaDeDetencion, _montoDePena)
        TR_vencimientoDePena_sinRestarOtrasDetenciones = TR_vencimientoDePena
        TR_vencimientoDePena = self.__RestarOtrasDetenciones(TR_vencimientoDePena, _otrosTiemposDeDetencion)            
        TR_caducidad_de_la_pena = TR_vencimientoDePena + relativedelta(years=10)
        TR_caducidad_de_la_pena_sinRestarOtrasDetenciones = TR_vencimientoDePena_sinRestarOtrasDetenciones + relativedelta(years=10)            

        # Arma el string para imprimir el cómputo
        self._vencimiento_y_caducidad_STRING = f'Vencimiento de pena: {Datetime_date_enFormatoXX_XX_XXXX(TR_vencimientoDePena)}\n'\
                f'Caducidad de la pena: {Datetime_date_enFormatoXX_XX_XXXX(TR_caducidad_de_la_pena)}'
        self._vencimiento_y_caducidad_STRING_SROT = f'Vencimiento de pena: {Datetime_date_enFormatoXX_XX_XXXX(TR_vencimientoDePena_sinRestarOtrasDetenciones)}\n'\
                f'Caducidad de la pena: {Datetime_date_enFormatoXX_XX_XXXX(TR_caducidad_de_la_pena_sinRestarOtrasDetenciones)}'
        
        return (TR_vencimientoDePena,
        TR_vencimientoDePena_sinRestarOtrasDetenciones,
        TR_caducidad_de_la_pena,
        TR_caducidad_de_la_pena_sinRestarOtrasDetenciones)
        
    def __CalcularLibertadCondicional(self, _fechaDeDetencion:datetime.date, _montoDePena:MontoDePena, _otrosTiemposDeDetencion="NULL"):

        TR_computo_libertad_condicional = _fechaDeDetencion
        TR_requisito_libertad_condicional = MontoDePena()        

        # Si es reincidente, igual hace el cálculo. La reincidencia solo va a influír
        # cuando se imprima el resultado, como una advertencia

        if _montoDePena.perpetua:
            
            TR_requisito_libertad_condicional.perpetua = True

            # CALCULO DE PENA PERPETUA

            if self._regimenNormativoAplicable._regimen_LC == LC_REGIMENES._Ley_11179:
                TR_requisito_libertad_condicional.años = 20
                TR_computo_libertad_condicional = self.__SumarMontoDePena(_fechaDeDetencion, TR_requisito_libertad_condicional)

            
            if self._regimenNormativoAplicable._regimen_LC == LC_REGIMENES._Ley_25892 or self._regimenNormativoAplicable._libertadCondicional == LC_REGIMENES._Ley_27375.value:
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

        # Aplica el estímulo educativo, si hay
        TR_computo_libertad_condicional = self.__AplicarEstimuloEducativo(TR_computo_libertad_condicional, self._estimulo_educativo)    

        # Arma el string para imprimir el cómputo
        self._libertad_condicional_STRING = f'Libertad condicional: {Datetime_date_enFormatoXX_XX_XXXX(TR_computo_libertad_condicional)}'
        self._libertad_condicional_STRING_SROT = f'Libertad condicional: {Datetime_date_enFormatoXX_XX_XXXX(TR_computo_libertad_condicional_sinRestarOtrasDetenciones)}'

        if _montoDePena.reincidencia:
            advertencia = '\nADVERTENCIA: No aplicaría el instituto de la Libertad Condicional porque la pena incluye reincidencia.'
            self._libertad_condicional_STRING += advertencia
        
        if self._regimenNormativoAplicable._regimen_LC == LC_REGIMENES._Ley_27375.value and _montoDePena.delitosExcluidosLey27375:
            advertencia = '\nADVERTENCIA: No aplicaría el instituto de la Libertad Condicional porque se condenó por alguno de los delitos excluídos, por art. 14 CP (según reforma de la ley 27.375).'
            self._libertad_condicional_STRING += advertencia
        return TR_computo_libertad_condicional, TR_computo_libertad_condicional_sinRestarOtrasDetenciones, TR_requisito_libertad_condicional
    
    def __CalcularRequisitoCalificacion_LC_o_ST(self, _fechaLC_o_ST, _fechaInicioEjecucion='NULL', _fechaCalificacionBueno='NULL'):
        situacion = 0

        if _fechaInicioEjecucion == 'NULL':
            # SITUACIÓN 1
            # SI TODAVÍA NO COMENZÓ LA EJECUCIÓN DE PENA
            
            situacion = 1
            return 'Al no encontrarse aún ejecutando pena, no es posible determinar la fecha desde la cual se cumplirá con este requisito.', situacion
        
        elif _fechaInicioEjecucion != 'NULL' and _fechaCalificacionBueno == 'NULL':
            # SITUACIÓN 2
            # SI COMENZÓ LA EJECUCIÓN DE PENA PERO AÚN NO CALIFICÓ COMO "BUENO"

            situacion = 2            
            delta = relativedelta(_fechaLC_o_ST, _fechaInicioEjecucion)
            pena1_3=MontoDePena(_años=delta.years, _meses=delta.months, _dias=delta.days)
            pena1_3 = self.__Calcular_un_tercio(pena1_3)
            fechaMinRequisitoCalif = self.__SumarMontoDePena(_fechaInicioEjecucion, pena1_3)

            #Devuelve la fecha límite para obtener el requisito "BUENO" teniendo en cuenta el requisito temporal LC en el caso concreto
            return fechaMinRequisitoCalif, situacion

        elif _fechaInicioEjecucion != 'NULL' and _fechaCalificacionBueno != 'NULL':
            # SITUACIÓN 3
            # SI SE ENCEUNTRA EJECUTANDO PENA Y TIENE REQUISITO DE CALIFICACIÓN "BUENO"

            situacion = 3
            # delta = relativedelta(_fechaInicioEjecucion, _fechaCalificacionBueno)
            delta = relativedelta(_fechaCalificacionBueno, _fechaInicioEjecucion)
            delta_TAMD = TiempoEn_Años_Meses_Dias(_años=delta.years, _meses=delta.months, _dias=delta.days)
            delta_x_3 = self.__Multiplicar_Tiempo(delta_TAMD, 3)
            fechaReqCalif = self.__SumarMontoDePena(_fechaInicioEjecucion, delta_x_3)

            # Devuelve la fecha desde la que se encontrará cumplido el requisito de calificación
            return fechaReqCalif, situacion
     
    def __CalcularNuevoComputoPorLCRevocada(self, _fechaLibertadCondicional, _vencimientoDePena, _fechaNuevaDetencion, _tiempoParcialenLCaComputar:OtraDetencion='NULL'):
        delta = relativedelta(_vencimientoDePena, _fechaLibertadCondicional)
        delta_TAMD = TiempoEn_Años_Meses_Dias(_años=delta.years, _meses=delta.months, _dias=delta.days)
        TR_nuevoVencimiento = self.__SumarMontoDePena(_fechaNuevaDetencion, delta_TAMD)
        print(f'__CalcularNuevoComputoPorLCRevocada --> TR_nuevoVencimiento (sin restar otras detenciones): {Datetime_date_enFormatoXX_XX_XXXX(TR_nuevoVencimiento)}')        
        TR_nuevoVencimiento = self.__RestarOtrasDetenciones(TR_nuevoVencimiento, _tiempoParcialenLCaComputar)
        TR_nuevaCaducidad = TR_nuevoVencimiento + relativedelta(years=10)
        delta = relativedelta(_fechaNuevaDetencion, _fechaLibertadCondicional)
        self._tiempo_que_permanecio_en_libertad = TiempoEn_Años_Meses_Dias(_años=delta.years, _meses=delta.months, _dias=delta.days)

        # Arma los string
        self._vencimiento_y_caducidad_STRING = f'Vencimiento de pena: {Datetime_date_enFormatoXX_XX_XXXX(TR_nuevoVencimiento)}\n'\
                f'Caducidad de la pena: {Datetime_date_enFormatoXX_XX_XXXX(TR_nuevaCaducidad)}\n'
        
        return TR_nuevoVencimiento, TR_nuevaCaducidad

    def __CalcularSalidasTransitorias(self, _fechaDeDetencion:datetime.date, _montoDePena:MontoDePena, _otrosTiemposDeDetencion="NULL", _fechaIngresoAPeriodoDePrueba:datetime.date=None):
        TR_computo_salidas_transitorias = _fechaDeDetencion
        TR_computo_salidas_transitorias_sinRestarOtrasDetenciones = datetime.date
        TR_requisito_salidas_transitorias = MontoDePena()        

        if _montoDePena.perpetua:

            TR_requisito_salidas_transitorias.perpetua = True

            if self._regimenNormativoAplicable._regimen_ST == ST_REGIMENES._DecretoLey412_58.value or self._regimenNormativoAplicable._regimen_ST == ST_REGIMENES._Ley_24660.value or self._regimenNormativoAplicable._regimen_ST == ST_REGIMENES._Ley_25948.value:
                
                TR_requisito_salidas_transitorias.años = 15
                TR_computo_salidas_transitorias = self.__SumarMontoDePena(_fechaDeDetencion, TR_requisito_salidas_transitorias)
                self._computo_salidas_transitorias_SITUACION = ST_COMPUTO_27375_SITUACION.HAY_COMPUTO.value
                self._salidas_transitorias_STRING = 'El requisito temporal de las salidas transitorias se alcanza a los 15 años.\n'\
                    f''
            
            if  self._regimenNormativoAplicable._regimen_ST == ST_REGIMENES._Ley_27375.value:
                if self._fecha_ingreso_a_periodo_de_prueba == 'NULL':
                    # Si todavía no está en periodo de prueba:
                    TR_computo_salidas_transitorias = self.__CalcularRequisitoTemporal_PeriodoDePrueba(self._fecha_de_detencion, self._monto_de_pena, self._otros_tiempos_de_detencion)
                    self._computo_salidas_transitorias_SITUACION = ST_COMPUTO_27375_SITUACION.TODAVIA_NO_INGRESO_A_PERIODO_DE_PRUEBA.value
                    self._salidas_transitorias_STRING = 'Como aún no se ingresó en el periodo de prueba, no es posible calcular el requisito temporal.\n'\
                        f'El requisito temporal del periodo de prueba se alcanza a los {self._requisito_temporal_periodo_de_prueba.años} año(s), {self._requisito_temporal_periodo_de_prueba.años} mes(es) y {self._requisito_temporal_periodo_de_prueba.años} día(s).\n'\
                        f'El periodo de prueba se alcanza, como mínimo, el {TR_computo_salidas_transitorias}'
                else:
                    # Si ya está en periodo de prueba:
                    reqASumar=TiempoEn_Años_Meses_Dias(_años=1)                    
                    reqTemp = 'El requisito temporal de las salidas transitorias se alcanza luego de un año desde el ingreso al periodo de prueba.\n'                    
                    TR_computo_salidas_transitorias = self.__SumarMontoDePena(self._fecha_ingreso_a_periodo_de_prueba, reqASumar)
                    self._computo_salidas_transitorias_SITUACION = ST_COMPUTO_27375_SITUACION.HAY_COMPUTO.value
                    ingresoAPP = f'Fecha de ingreso a periodo de prueba: {Datetime_date_enFormatoXX_XX_XXXX(self._fecha_ingreso_a_periodo_de_prueba)}\n'
                    reqTempConFecha = f'Requisito temporal Salidas Transitorias: {Datetime_date_enFormatoXX_XX_XXXX(TR_computo_salidas_transitorias)}'
                    self._salidas_transitorias_STRING = reqTemp + ingresoAPP + reqTempConFecha
        else:   

            if self._regimenNormativoAplicable._regimen_ST == ST_REGIMENES._DecretoLey412_58.value or self._regimenNormativoAplicable._regimen_ST == ST_REGIMENES._Ley_24660.value or self._regimenNormativoAplicable._regimen_ST == ST_REGIMENES._Ley_25948.value:
                
                TR_requisito_salidas_transitorias = self.__Calcular_la_mitad(_montoDePena)
                TR_computo_salidas_transitorias = self.__SumarMontoDePena(TR_computo_salidas_transitorias, TR_requisito_salidas_transitorias)
            
            if  self._regimenNormativoAplicable._regimen_ST == ST_REGIMENES._Ley_27375.value:
                if self._fecha_ingreso_a_periodo_de_prueba == 'NULL':
                    # Si todavía no está en periodo de prueba:
                    TR_computo_salidas_transitorias = self.__CalcularRequisitoTemporal_PeriodoDePrueba(self._fecha_de_detencion, self._monto_de_pena, self._otros_tiempos_de_detencion)
                    self._computo_salidas_transitorias_SITUACION = ST_COMPUTO_27375_SITUACION.TODAVIA_NO_INGRESO_A_PERIODO_DE_PRUEBA.value
                    self._salidas_transitorias_STRING = 'Como aún no se ingresó en el periodo de prueba, no es posible calcular el requisito temporal.\n'\
                        f'El requisito temporal del periodo de prueba se alcanza a los {self._requisito_temporal_periodo_de_prueba.años} año(s), {self._requisito_temporal_periodo_de_prueba.años} mes(es) y {self._requisito_temporal_periodo_de_prueba.años} día(s).\n'\
                        f'El periodo de prueba se alcanza, como mínimo, el {TR_computo_salidas_transitorias}'
                else:
                    # Si ya está en periodo de prueba:
                    reqASumar=TiempoEn_Años_Meses_Dias()
                    reqTemp = ''
                    if MontoDeTiempoA_es_Mayor_que_MontoDeTiempoB(_montoDePena, TiempoEn_Años_Meses_Dias(_años=10)):
                        reqASumar.años = 1
                        reqTemp = 'El requisito temporal de las salidas transitorias se alcanza luego de un año desde el ingreso al periodo de prueba.\n'
                    elif MontoDeTiempoA_es_Mayor_que_MontoDeTiempoB(_montoDePena, TiempoEn_Años_Meses_Dias(_años=5)):
                        reqASumar.meses = 6
                        reqTemp = 'El requisito temporal de las salidas transitorias se alcanza luego de 6 meses desde el ingreso al periodo de prueba.\n'
                    TR_computo_salidas_transitorias = self.__SumarMontoDePena(self._fecha_ingreso_a_periodo_de_prueba, reqASumar)
                    self._computo_salidas_transitorias_SITUACION = ST_COMPUTO_27375_SITUACION.HAY_COMPUTO.value
                    ingresoAPP = f'Fecha de ingreso a periodo de prueba: {Datetime_date_enFormatoXX_XX_XXXX(self._fecha_ingreso_a_periodo_de_prueba)}\n'
                    reqTempConFecha = f'Requisito temporal Salidas Transitorias: {Datetime_date_enFormatoXX_XX_XXXX(TR_computo_salidas_transitorias)}'
                    self._salidas_transitorias_STRING = reqTemp + ingresoAPP + reqTempConFecha
        
        # Resta otras detenciones, si hay
        TR_computo_salidas_transitorias_sinRestarOtrasDetenciones = TR_computo_salidas_transitorias
        TR_computo_salidas_transitorias = self.__RestarOtrasDetenciones(TR_computo_salidas_transitorias, _otrosTiemposDeDetencion)

        # Aplica el estímulo educativo, si hay
        TR_computo_salidas_transitorias = self.__AplicarEstimuloEducativo(TR_computo_salidas_transitorias, self._estimulo_educativo)
        return TR_computo_salidas_transitorias, TR_computo_salidas_transitorias_sinRestarOtrasDetenciones, TR_requisito_salidas_transitorias
    
    def __CalcularRequisitoTemporal_PeriodoDePrueba(self, _fechaDeDetencion:datetime.date, _montoDePena:MontoDePena, _otrosTiemposDeDetencion="NULL"):
        if _montoDePena.perpetua:
            self._requisito_temporal_periodo_de_prueba = TiempoEn_Años_Meses_Dias(_años=15)
            reqTemporalPeriodoDePrueba = self.__SumarMontoDePena(_fechaDeDetencion, self._requisito_temporal_periodo_de_prueba)
            reqTemporalPeriodoDePrueba = self.__RestarOtrasDetenciones(reqTemporalPeriodoDePrueba, _otrosTiemposDeDetencion)
            return reqTemporalPeriodoDePrueba
        else:
            self._requisito_temporal_periodo_de_prueba = self.__Calcular_la_mitad(_montoDePena)
            reqTemporalPeriodoDePrueba = self.__SumarMontoDePena(_fechaDeDetencion, self._requisito_temporal_periodo_de_prueba)
            reqTemporalPeriodoDePrueba = self.__RestarOtrasDetenciones(reqTemporalPeriodoDePrueba, _otrosTiemposDeDetencion)
            return reqTemporalPeriodoDePrueba

    def __CalcularLibertadAsistida(self, _vencimientoDePena:datetime.date, _vencimiento_sinRestarOtrasDetenciones:datetime.date):
        
        TR_computo_libertad_asistida = ''
        TR_computo_libertad_asistida_sinRestarOtrasDetenciones = ''

        if self._monto_de_pena.perpetua:
            TR_computo_libertad_asistida = 'Pena perpetua'
            TR_computo_libertad_asistida_sinRestarOtrasDetenciones = 'Pena perpetua'
            return TR_computo_libertad_asistida, TR_computo_libertad_asistida_sinRestarOtrasDetenciones

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
        
        # No se resta acá las otras detenciones porque ya fueron restadas en el vencimiento de pena

        # Aplica el estímulo educativo, si hay
        TR_computo_libertad_asistida = self.__AplicarEstimuloEducativo(TR_computo_libertad_asistida, self._estimulo_educativo)
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
        
        # IMPRIME CÓMPUTO PENA DE EJECUCIÓN CONDICIONAL
        # -------------------------------------
        if self._monto_de_pena.ejecucionCondicional: 
            print(self._vencimiento_y_caducidad_STRING)
            return
        
        # IMPRIME NUEVO CÓMPUTO DE PENA POR LIBERTAD CONDICIONAL REVOCADA
        # ---------------------------------------------------------------
        if self._es_computo_por_LC_revocada:
            INFORMACION_SOBRE_EL_COMPUTO = 'INFORMACIÓN SOBRE EL CÓMPUTO\n'\
                '----------------------------\n'\
                f'Fecha del hecho: {Datetime_date_enFormatoXX_XX_XXXX(self._fecha_del_hecho)}\n'\
                f'Es un nuevo cómputo por una libertad condicional revocada.\n'\
                f'El egreso en libertad condicional se produjo el {Datetime_date_enFormatoXX_XX_XXXX(self._libertad_condicional_en_computo_anterior)}\n'\
                f'Fue detenido/a nuevamente el {Datetime_date_enFormatoXX_XX_XXXX(self._nueva_fecha_de_detencion)}\n'\
                f'La persona permaneció en libertad {self._tiempo_que_permanecio_en_libertad.años} año(s), {self._tiempo_que_permanecio_en_libertad.meses} mes(es) y {self._tiempo_que_permanecio_en_libertad.dias} día(s).'
            print(self._regimenNormativoAplicable)
            print(INFORMACION_SOBRE_EL_COMPUTO)
            print('')
            print('NUEVO CÓMPUTO DE PENA')
            print('---------------------')
            print(self._vencimiento_y_caducidad_STRING)
            print('Todavía no armé ST y LA')
            return
        
        # IMPRIME CÓMPUTO DE PENA TEMPORAL SIN RECLUSIÓN POR TIEMPO INDETERMINADO
        # -----------------------------------------------------------------------
        if not self._monto_de_pena.ejecucionCondicional and not self._monto_de_pena.perpetua and not self._monto_de_pena.reclusionPorTiempoIndeterminado:            

            INFORMACION_SOBRE_EL_COMPUTO = 'INFORMACIÓN SOBRE EL CÓMPUTO\n'\
                '----------------------------\n'\
                f'Fecha del hecho: {Datetime_date_enFormatoXX_XX_XXXX(self._fecha_del_hecho)}\n'\
                f'La pena es de {self._monto_de_pena.años} año(s), {self._monto_de_pena.meses} mes(es) y {self._monto_de_pena.dias} día(s).\n'\
                f'El requisito temporal de la libertad condicional se alcanza a los {self._requisito_libertad_condicional.años} año(s), {self._requisito_libertad_condicional.meses} mes(es) y {self._requisito_libertad_condicional.dias} día(s).'                
            print(self._regimenNormativoAplicable)
            print(INFORMACION_SOBRE_EL_COMPUTO)

            print('')
            print('CÓMPUTO DE PENA')
            print('---------------')
            print(self._vencimiento_y_caducidad_STRING)
            print(self._libertad_condicional_STRING)
            if self._regimenNormativoAplicable._regimen_LC == LC_REGIMENES._Ley_27375.value:
                if self._requisitoCalificacion_libertad_condicional_SITUACION == 1:
                    print('En tanto no se ha comenzado aún a ejecutar pena, no es posible calcular el requisito de calificación del art. 28, ley 24.660 (según ley 27.375).')
                if self._requisitoCalificacion_libertad_condicional_SITUACION == 2:
                    _print = 'La persona se encuentra ejecutando pena pero aún no cuenta con el requisito de calificación "BUENO".\n'\
                        f'La fecha límite para obtener la calificación "BUENO" sin postergar el requisito temporal de la libertad condicional es: {self._requisitoCalificacion_libertad_condicional}'
                    print(_print)
                    if FechaA_es_Mayor_Que_FechaB(self._computo_libertad_condicional, self._requisitoCalificacion_libertad_condicional):
                        print(f'Libertad condicional (integral): {Datetime_date_enFormatoXX_XX_XXXX(self._computo_libertad_condicional)}')
                    else:
                        print(f'Libertad condicional (integral): {Datetime_date_enFormatoXX_XX_XXXX(self._requisitoCalificacion_libertad_condicional)}')                    
                if self._requisitoCalificacion_libertad_condicional_SITUACION == 3:
                    _print = f'La persona se encuentra ejecutando pena y cuenta con el requisito de calificación "BUENO" desde el día: {Datetime_date_enFormatoXX_XX_XXXX(self._fecha_calificacion_BUENO)}\n'\
                        f'Requisito temporal de calificación: {Datetime_date_enFormatoXX_XX_XXXX(self._requisitoCalificacion_libertad_condicional)}'                    
                    print(_print)
                    if FechaA_es_Mayor_Que_FechaB(self._computo_libertad_condicional, self._requisitoCalificacion_libertad_condicional):
                        print(f'Libertad condicional (integral): {Datetime_date_enFormatoXX_XX_XXXX(self._computo_libertad_condicional)}')
                    else:
                        print(f'Libertad condicional (integral): {Datetime_date_enFormatoXX_XX_XXXX(self._requisitoCalificacion_libertad_condicional)}')
            print(self._salidas_transitorias_STRING)

            print('')
            print('CÓMPUTO DE PENA (SIN RESTAR OTRAS DETENCIONES)')
            print('---------------------------------------------)')
            print(self._vencimiento_y_caducidad_STRING_SROT)
            print(self._libertad_condicional_STRING_SROT)
            return

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
        
        if self._regimenNormativoAplicable._regimen_LC == LC_REGIMENES._Ley_27375.value:            
            if self._situacionProcesal._EsPorDelitosExcluidosLey27375:
                libertadCondicional = f'{libertadCondicional}\n'\
                f'{libertadCondicional_advertenciaDelitosExcluidosLey27375}'        
   
def _DEBUG_PENA_TEMPORAL():    
    fechaDelHecho = datetime.date(2018, 5, 26)
    fechaDeDetencionInput = datetime.date(2020, 1, 1)
    montoDePena = MontoDePena(_años=8, _esPorDelitosExcluidosLey27375=True, _esPorDelitosExcluidosLey25948=True)
    otrasDetenciones='NULL'
    estimuloEducativo=TiempoEn_Años_Meses_Dias()
    fechaInicioEjecucion=datetime.date(2022, 6, 1)
    fechaCalificacionBUENO='NULL'#datetime.date(2022, 3, 10)    
    fechaIngresoPeriodoDePrueba=datetime.date(2022, 12, 10)
    #fechaIngresoPeriodoDePrueba='NULL'
    
    computo = ComputoPenaTemporal(fechaDelHecho=fechaDelHecho,
    fechaDeDetencion=fechaDeDetencionInput,
    montoDePena=montoDePena,
    otrasDetenciones=otrasDetenciones,
    estimuloEducativo=estimuloEducativo,
    fechaInicioEjecucion=fechaInicioEjecucion,
    fechaCalificacionBUENO=fechaCalificacionBUENO,
    fechaIngresoPeriodoDePrueba=fechaIngresoPeriodoDePrueba)    

if __name__ == '__main__':
    _DEBUG_PENA_TEMPORAL()