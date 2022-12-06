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

class ComputoPenaTemporalOPerpetua(Computo):
    def __init__(self,
    fechaDelHecho:datetime.date='NULL',
    fechaDeDetencion:datetime.date='NULL',
    montoDePena:MontoDePena='NULL',
    montoUnidadesFijas:Union[int,float]='NULL',
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
        self._monto_multa_unidades_fijas = montoUnidadesFijas
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

        self._regimen_preparacion_libertad_COMPUTO = 'NULL'

        self._multa_unidadesFijas_en_pesos = 'NULL'

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
        self._CalcularRegimenPreparacionLibertad()
        self._CalcularUnidadesFijas()
        
        # Imprime los resultados
        self._ImprimirSTRINGGeneral()
        self._ImprimirSTRINGRegimenNormativo()
        self._ImprimirSTRINGVencimientoYCaducidadDePena()
        self._ImprimirSTRINGLibertadCondicional()
        self._ImprimirSTRINGSalidasTransitorias()        
        self._ImprimirSTRINGLibertadAsistida()
        self._ImprimirSTRINGRegimenPreparatorioParaLaLiberacion()
        self._ImprimirSTRINGMultaUnidadesFijasEnPesos()
        print(Separadores._separadorComun)
    
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
        
        # Si la pena es perpetua esta función no hace nada, porque aún no se cuenta con el cómputo de
        # libertad condicional. El vencimiento y caducidad lo va a calcular la función de la condicional
        if self._monto_de_pena.perpetua:
            return
        
        _vencimiento_de_pena = 0
        _caducidad_de_pena = 0

        _vencimiento_de_pena = self._SumarMontoDePena(self._fecha_de_detencion, self._monto_de_pena)
        print(f'DEBUG: Vencimiento de pena sin restar otras detenciones = {Datetime_date_enFormatoXX_XX_XXXX(_vencimiento_de_pena)}')
        _vencimiento_de_pena = self._RestarOtrasDetenciones(_vencimiento_de_pena, self._otras_detenciones)
        _caducidad_de_pena = _vencimiento_de_pena + relativedelta(years=10)

        self._vencimiento_de_pena = _vencimiento_de_pena
        self._caducidad_de_pena = _caducidad_de_pena        
    
    def _CalcularLibertadCondicional(self):

        def _CalcularLibertadCondicional_RequisitoCalificacion():

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
        
        def _CalcularLibertadCondicional_ComputoIntegral():
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

        # -----------------------------------------
        #
        # def _CalcularLibertadCondicional(self)
        #
        # -----------------------------------------

        if self._regimen_normativo._regimen_LC == LC_REGIMENES._No_aplica.value:
            return

        # Crea las variables temporales que va a necesitar para el output y les asigna los datos que van a usar
        _computo_libertad_condicional = self._fecha_de_detencion
        _requisito_temporal_libertad_condicional = TiempoEn_Años_Meses_Dias()

        # Si es reincidente, o por delitos excluídos, igual hace el cálculo, pero arroja advertencias
        # Las advertencias las manejan las funciones que arman los string

        # Define el requisito temporal, y luego calcula el cómputo
        print(f'DEBUG: self._monto_de_pena es mayor a 3 años? --> {MontoDeTiempoA_es_Mayor_que_MontoDeTiempoB(self._monto_de_pena, TiempoEn_Años_Meses_Dias(_años=3))}')
        if self._monto_de_pena.perpetua:
        # Penas perpetuas
            _requisito_temporal_libertad_condicional.años = self._regimen_normativo.LIBERTAD_CONDICIONAL(LC_KEYS._requisitoTemporalPenaPerpetua_KEY)
            _computo_libertad_condicional = self._SumarMontoDePena(self._fecha_de_detencion, _requisito_temporal_libertad_condicional)
        elif MontoDeTiempoA_es_Mayor_que_MontoDeTiempoB(self._monto_de_pena, TiempoEn_Años_Meses_Dias(_años=3)) != True:
        # Penas temporales de hasta 3 años
            _requisito_temporal_libertad_condicional.meses = 8                
            _computo_libertad_condicional = self._SumarMontoDePena(self._fecha_de_detencion, _requisito_temporal_libertad_condicional)
        else:
        # Penas temporales de más de 3 años
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

        if self._monto_de_pena.perpetua: # Si es pena perpetua, calcula vencimiento y caducidad
            self._vencimiento_de_pena = self._SumarMontoDePena(self._libertad_condicional_COMPUTO, TiempoEn_Años_Meses_Dias(_años=5))
            self._caducidad_de_pena = self._vencimiento_de_pena + relativedelta(years=10)

        # Si aplica la ley 27.375, calcula además el requisito de calificación, y el integral
        if self._regimen_normativo._regimen_LC == LC_REGIMENES._Ley_27375.value:
            _CalcularLibertadCondicional_RequisitoCalificacion()
            _CalcularLibertadCondicional_ComputoIntegral()        
    
    def _CalcularSalidasTransitorias(self):  
        
        def _CalcularSalidasTransitorias_RequisitoCalificacionBUENO():

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
                
                self._salidas_transitorias_REQUISITO_CALIF_SITUACION = 1
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

        def _CalcularRequisitoTemporal_PeriodoDePrueba():

            # Calcula el requisito temporal del periodo de prueba        
            if self._monto_de_pena.perpetua:
                self._salidas_transitorias_REQUISITO_TEMPORAL_PERIODO_DE_PRUEBA = MontoDePena(_años=15)
            else:
                self._salidas_transitorias_REQUISITO_TEMPORAL_PERIODO_DE_PRUEBA = self._Calcular_la_mitad(self._monto_de_pena)
            
            # Hace la cuenta (fecha de detención + requisito temporal)
            self._salidas_transitorias_COMPUTO_PERIODO_DE_PRUEBA = self._SumarMontoDePena(self._fecha_de_detencion, self._salidas_transitorias_REQUISITO_TEMPORAL_PERIODO_DE_PRUEBA)        
    
        def _CalcularRequisitoTemporal_SalidasTransitorias_Ley27375():
            '''DEVUELVE CUANTOS MESES O AÑOS HAY QUE SUMARLE AL PERIODO DE PRUEBA PARA OBTENER LAS SALIDAS TRANSITORIAS'''
            reqASumar=TiempoEn_Años_Meses_Dias()
            if self._monto_de_pena.perpetua:
                reqASumar.años = 1
            elif MontoDeTiempoA_es_Mayor_que_MontoDeTiempoB(self._monto_de_pena, TiempoEn_Años_Meses_Dias(_años=10)):
                reqASumar.años = 1
            elif MontoDeTiempoA_es_Mayor_que_MontoDeTiempoB(self._monto_de_pena, TiempoEn_Años_Meses_Dias(_años=5)):
                reqASumar.meses = 6 
            return reqASumar
    
        def _CalcularSalidasTransitorias_RequisitoConductaEJEMPLAR():            
            # if self._fecha_calificacion_EJEMPLAR == 'NULL':
            # # SI AÚN NO CONSIGUIÓ LA CALIFICACIÓN EJEMPLAR:
            #     if self._fecha_ingreso_a_periodo_de_prueba == 'NULL':
            #         # SI NO TIENE CONDUCTA EJEMPLAR NI INGRESÓ AL PERIODO DE PRUEBA:
            #         # Calcula la fecha en que habría que tener el requisito de calificación para poder
            #         # aprovechar la eventual mejor situación

            #         # Calcula el requisito potencial de las ST (si se alcanza en tiempo el periodo de prueba)
            #         self._salidas_transitorias_REQUISITO_CALIF_EJEMPLAR = self._SumarMontoDePena(self._salidas_transitorias_COMPUTO_PERIODO_DE_PRUEBA, self._CalcularRequisitoTemporal_SalidasTransitorias_Ley27375())
            #         # A esa fecha le resta un año
            #         self._salidas_transitorias_REQUISITO_CALIF_EJEMPLAR -= relativedelta(years=1)
            #     else:
            #         # SI NO TIENE CONDUCTA EJEMPLAR, PERO INGRESÓ AL PERIODO DE PRUEBA, ENTONCES TIENE
            #         # CÓMPUTO DE SALIDAS TRANSITORIAS:
            #         # En ese caso solamente se le resta un año a ese cómputo
            #         self._salidas_transitorias_REQUISITO_CALIF_EJEMPLAR = self._salidas_transitorias_COMPUTO
            #         self._salidas_transitorias_REQUISITO_CALIF_EJEMPLAR -= relativedelta(years=1)
            # else:
            # # SI YA TIENE FECHA DE CALIFICACIÓN EJEMPLAR:
            # # Calcula desde cuándo se podrán obtener las salidas transitorias, según ese requisito (sin contemplar
            # # los otros requisitos de la ST. Esos se valorarán en el cómputo integral)
            #     self._salidas_transitorias_REQUISITO_CALIF_EJEMPLAR = self._fecha_calificacion_EJEMPLAR
            #     self._salidas_transitorias_REQUISITO_CALIF_EJEMPLAR += relativedelta(years=1)
            pass

        # -----------------------------------------
        #
        # def _CalcularSalidasTransitorias(self)
        #
        # -----------------------------------------

        if self._regimen_normativo._regimen_ST == ST_REGIMENES._No_aplica.value:
            return      
        
        _computo_salidas_transitorias = self._fecha_de_detencion        
        _requisito_salidas_transitorias = MontoDePena()        

        if (self._regimen_normativo._regimen_ST == ST_REGIMENES._DecretoLey412_58.value
            or self._regimen_normativo._regimen_ST == ST_REGIMENES._Ley_24660.value
            or self._regimen_normativo._regimen_ST == ST_REGIMENES._Ley_25948.value):
            
            # Calcula el requisito temporal
            if self._monto_de_pena.perpetua:
                _requisito_salidas_transitorias.años = 15
            else:
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

            _CalcularRequisitoTemporal_PeriodoDePrueba()

            if self._fecha_ingreso_a_periodo_de_prueba == 'NULL':
                # Si todavía no está en periodo de prueba:
                # Calcula la fecha mínima, y el requisito temporal para poder ingresar al periodo de prueba                

                print(f'DEBUG: Cómputo Salidas transitorias (periodo de prueba) sin restar otras detenciones = {Datetime_date_enFormatoXX_XX_XXXX(self._salidas_transitorias_COMPUTO_PERIODO_DE_PRUEBA)}')
                self._salidas_transitorias_COMPUTO_PERIODO_DE_PRUEBA = self._RestarOtrasDetenciones(self._salidas_transitorias_COMPUTO_PERIODO_DE_PRUEBA, self._otras_detenciones)

                print(f'DEBUG: Cómputo Salidas transitorias (periodo de prueba) sin aplicar estímulo educativo = {Datetime_date_enFormatoXX_XX_XXXX(self._salidas_transitorias_COMPUTO_PERIODO_DE_PRUEBA)}')
                self._salidas_transitorias_COMPUTO_PERIODO_DE_PRUEBA = self._AplicarEstimuloEducativo(self._salidas_transitorias_COMPUTO_PERIODO_DE_PRUEBA, self._estimulo_educativo)
                self._salidas_transitorias_27375_SITUACION = ST_COMPUTO_27375_SITUACION.TODAVIA_NO_INGRESO_A_PERIODO_DE_PRUEBA.value

                # Calcula el requisito temporal de las Salidas Transitorias en función del requisito temporal para ingresar la periodo de prueba
                self._salidas_transitorias_REQUISITO_TEMPORAL=_CalcularRequisitoTemporal_SalidasTransitorias_Ley27375()                
                self._salidas_transitorias_REQUISITO_TEMPORAL_INTEGRAL = deepcopy(self._salidas_transitorias_REQUISITO_TEMPORAL_PERIODO_DE_PRUEBA)
                self._salidas_transitorias_REQUISITO_TEMPORAL_INTEGRAL.años += self._salidas_transitorias_REQUISITO_TEMPORAL.años
                self._salidas_transitorias_REQUISITO_TEMPORAL_INTEGRAL.meses += self._salidas_transitorias_REQUISITO_TEMPORAL.meses

                # Con el requisito temporal de las salidas transitorias, calcula el cómputo
                self._salidas_transitorias_COMPUTO = self._SumarMontoDePena(self._fecha_de_detencion, self._salidas_transitorias_REQUISITO_TEMPORAL_INTEGRAL)                

                # Calcula cuándo debe obtenerse la conducta ejemplar (resta un año al cómputo)
                self._salidas_transitorias_REQUISITO_CALIF_EJEMPLAR = self._salidas_transitorias_COMPUTO
                self._salidas_transitorias_REQUISITO_CALIF_EJEMPLAR -= relativedelta(years=1)

                # Calcula cuándo debe obtenerse la calificación "Bueno" para lograr los 2/3
                _CalcularSalidasTransitorias_RequisitoCalificacionBUENO()

            else:
                # Si ya está en periodo de prueba:
                # Calcula el cómputo (guarda el cálculo sin restar otras detenciones ni aplicar estímulo educativo
                # en otra variable, para que elija el usuario si lo computa doble, o no)
                
                # Calcula el requisito temporal de las salidas transitorias, teniendo en cuenta la fecha de ingreso al
                # periodo de prueba
                self._salidas_transitorias_REQUISITO_TEMPORAL = _CalcularRequisitoTemporal_SalidasTransitorias_Ley27375()                

                # Hace el cómputo de las salidas transitorias y lo guarda en la variable sin restar
                requisito_temporal = self._salidas_transitorias_REQUISITO_TEMPORAL.años + self._salidas_transitorias_REQUISITO_TEMPORAL.meses + self._salidas_transitorias_REQUISITO_TEMPORAL.dias
                if requisito_temporal != 0:
                    self._salidas_transitorias_COMPUTO = self._SumarMontoDePena(self._fecha_ingreso_a_periodo_de_prueba, self._salidas_transitorias_REQUISITO_TEMPORAL)                

                if self._vuelve_a_restar_otras_detenciones_y_140_en_ST:
                    # Resta otras detenciones
                    self._salidas_transitorias_COMPUTO = self._RestarOtrasDetenciones(self._salidas_transitorias_COMPUTO, self._otras_detenciones)

                    # Aplica estímulo educativo
                    self._salidas_transitorias_COMPUTO = self._AplicarEstimuloEducativo(self._salidas_transitorias_COMPUTO, self._estimulo_educativo)

                # Calcula cuándo debe obtenerse la conducta ejemplar (resta un año al cómputo)
                self._salidas_transitorias_REQUISITO_CALIF_EJEMPLAR = self._salidas_transitorias_COMPUTO
                self._salidas_transitorias_REQUISITO_CALIF_EJEMPLAR -= relativedelta(years=1)

                # Calcula cuándo debe obtenerse la calificación "Bueno" para lograr los 2/3
                _CalcularSalidasTransitorias_RequisitoCalificacionBUENO()

                self._salidas_transitorias_27375_SITUACION = ST_COMPUTO_27375_SITUACION.HAY_COMPUTO.value
        
    def _CalcularLibertadAsistida(self):
        
        # Utiliza las siguientes variables:
        # - _vencimientoDePena

        if self._regimen_normativo._regimen_LA == LA_REGIMENES._No_aplica.value:
            return
        
        if self._monto_de_pena.perpetua:
            return

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
    
    def _CalcularRegimenPreparacionLibertad(self):
        
        # Utiliza las siguientes variables:
        # - _vencimientoDePena  

        if self._regimen_normativo._regimen_PREPLIB == REGPREPLIB_REGIMENES._No_aplica.value:
            return 

        if self._monto_de_pena.perpetua:
            return                     
        
        if self._regimen_normativo._regimen_PREPLIB == REGPREPLIB_REGIMENES._Ley_27375.value:

            _computo_regPrepLib = self._vencimiento_de_pena
            _computo_regPrepLib += relativedelta(years=-1)            
        
            # No se resta acá las otras detenciones porque ya fueron restadas en el vencimiento de pena

            print(f'DEBUG: Régimen de preparación para la libertad sin aplicar estímulo educativo = {Datetime_date_enFormatoXX_XX_XXXX(_computo_regPrepLib)}')
            # Aplica el estímulo educativo, si hay
            _computo_regPrepLib = self._AplicarEstimuloEducativo(_computo_regPrepLib, self._estimulo_educativo)        

            # Guarda el dato en la variable correspondiente
            self._regimen_preparacion_libertad_COMPUTO = _computo_regPrepLib

    def _CalcularUnidadesFijas(self):
        if self._regimen_normativo._regimen_UNIDADESFIJAS == 'No aplica':
            return
        
        self._multa_unidadesFijas_en_pesos = self._monto_multa_unidades_fijas * self._regimen_normativo.UNIDADES_FIJAS(UNIDADESFIJAS_KEYS._valorDeLaUnidadFija)

    def _ImprimirSTRINGGeneral(self):
        print(Separadores._separadorComun)
        print('DATOS INGRESADOS')
        print('----------------')
        print(f' - Fecha del hecho: {Datetime_date_enFormatoXX_XX_XXXX(self._fecha_del_hecho)}')
        print(f' - Fecha de detención: {Datetime_date_enFormatoXX_XX_XXXX(self._fecha_de_detencion)}')
        
        if self._monto_de_pena.perpetua:
            print(' - Es una pena perpetua.')
        else:
            print(f' - La pena es de {self._monto_de_pena.años} año(s), {self._monto_de_pena.meses} mes(es) y {self._monto_de_pena.dias} día(s).')
        
        if self._monto_multa_unidades_fijas != 'NULL':
            print(f'    - La multa es de {self._monto_multa_unidades_fijas} unidades fijas.')
            
        if self._monto_de_pena.reincidencia:
            print('    - Es reincidente.')
        # if self._monto_de_pena.ejecucionCondicional:
        #     print('    - Es de ejecución condicional.')
        #     print(f'    - El plazo de control es de {self._monto_de_pena.plazoControl_años} año(s), {self._monto_de_pena.plazoControl_meses} mes(es) y {self._monto_de_pena.plazoControl_dias} día(s).')
        # if self._monto_de_pena.reclusionPorTiempoIndeterminado:
        #     print('    - Hay accesoria de reclusión por tiempo indeterminado.')
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

    def _ImprimirSTRINGRegimenNormativo(self):
        if self._monto_multa_unidades_fijas == 'NULL':
            self._regimen_normativo._Imprimir()
        else:
            self._regimen_normativo._Imprimir(imprimir_reg_unidadesFijas=True)

    def _ImprimirSTRINGVencimientoYCaducidadDePena(self):
        print(Separadores._separadorComun)
        print('VENCIMIENTO Y CADUCIDAD')
        print('-----------------------')        
        print(f' - Vencimiento de la pena: {Datetime_date_enFormatoXX_XX_XXXX(self._vencimiento_de_pena)}')
        print(f' - Caducidad de la pena: {Datetime_date_enFormatoXX_XX_XXXX(self._caducidad_de_pena)}')
        if self._monto_de_pena.perpetua:
            print(' - Los cálculos están sujetos a obtener la libertad condicional en la fecha del cómputo.')
    
    def _ImprimirSTRINGLibertadCondicional(self):  

        if self._regimen_normativo._regimen_LC == LC_REGIMENES._No_aplica.value:
            return

        print(Separadores._separadorComun)
        print('LIBERTAD CONDICIONAL')
        print('--------------------')
        print(f' - La libertad condicional se obtiene a los {self._libertad_condicional_REQUISITO_TEMPORAL.años} año(s), {self._libertad_condicional_REQUISITO_TEMPORAL.meses} mes(es) y {self._libertad_condicional_REQUISITO_TEMPORAL.dias} día(s).')
        print(f' - El requisito temporal para acceder a la libertad condicional se cumple el {Datetime_date_enFormatoXX_XX_XXXX(self._libertad_condicional_COMPUTO)}')        
        
        # Imprime advertencias, si corresponde
        if self._monto_de_pena.reincidencia:
            print('ADVERTENCIA: No aplicaría el instituto de la Libertad Condicional porque la pena incluye reincidencia.')            
        
        if self._regimen_normativo._regimen_LC == LC_REGIMENES._Ley_25892.value and self._monto_de_pena.delitosExcluidosLey25892:
            print('ADVERTENCIA: No aplicaría el instituto de la Libertad Condicional porque se condenó por alguno de los delitos excluídos, por art. 14 CP (según reforma de la ley 25.892).')
        
        if self._regimen_normativo._regimen_LC == LC_REGIMENES._Ley_27375.value and self._monto_de_pena.delitosExcluidosLey27375:
            print('ADVERTENCIA: No aplicaría el instituto de la Libertad Condicional porque se condenó por alguno de los delitos excluídos, por art. 14 CP (según reforma de la ley 27.375).')
        
        # Imprime requisito de calificación, si corresponde
        if self._regimen_normativo._regimen_LC == LC_REGIMENES._Ley_27375.value:
            if self._libertad_condicional_REQUISITO_CALIF_SITUACION == 1:
                print('Como no se cuenta con la fecha en la que se inició la ejecución de la pena, no es posible calcular el requisito temporal de calificación (art. 28, ley 24.660).')
            if self._libertad_condicional_REQUISITO_CALIF_SITUACION == 2:
                print(f' - Teniendo en cuenta que se comenzó a ejecutar la pena el día {Datetime_date_enFormatoXX_XX_XXXX(self._fecha_inicio_ejecucion)}, para acceder a la libertad condicional en la fecha indicada, la fecha límite para obtener el requisito de calificación "bueno" es {Datetime_date_enFormatoXX_XX_XXXX(self._libertad_condicional_REQUISITO_CALIF_BUENO)}.')
            if self._libertad_condicional_REQUISITO_CALIF_SITUACION == 3:
                print(f' - Teniendo en cuenta que se comenzó a ejecutar la pena el día {Datetime_date_enFormatoXX_XX_XXXX(self._fecha_inicio_ejecucion)} y que se obtuvo el requisito de calificación "bueno" el día {Datetime_date_enFormatoXX_XX_XXXX(self._fecha_calificacion_BUENO)}, los 2/3 de pena con calificación "bueno" se cumplirán el día {Datetime_date_enFormatoXX_XX_XXXX(self._libertad_condicional_REQUISITO_CALIF_BUENO)}.')

    def _ImprimirSTRINGSalidasTransitorias(self):

        if self._regimen_normativo._regimen_ST == ST_REGIMENES._No_aplica.value:
            return

        print(Separadores._separadorComun)
        print('SALIDAS TRANSITORIAS')
        print('--------------------')

        if self._regimen_normativo._regimen_ST == ST_REGIMENES._DecretoLey412_58.value or self._regimen_normativo._regimen_ST == ST_REGIMENES._Ley_24660.value or self._regimen_normativo._regimen_ST == ST_REGIMENES._Ley_25948.value:
            print(f' - Las salidas transitorias se obtienen a los {self._salidas_transitorias_REQUISITO_TEMPORAL.años} año(s), {self._salidas_transitorias_REQUISITO_TEMPORAL.meses} mes(es) y {self._salidas_transitorias_REQUISITO_TEMPORAL.dias} día(s).')
            print(f' - El requisito temporal para acceder a las salidas transitorias se cumple el {Datetime_date_enFormatoXX_XX_XXXX(self._salidas_transitorias_COMPUTO)}')            
        
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
                    print(f' - Teniendo en cuenta que se comenzó a ejecutar la pena el día {Datetime_date_enFormatoXX_XX_XXXX(self._fecha_inicio_ejecucion)} y que se obtuvo el requisito de calificación "bueno" el día {Datetime_date_enFormatoXX_XX_XXXX(self._fecha_calificacion_BUENO)}, los 2/3 de pena con calificación "bueno" se cumplirán el día {Datetime_date_enFormatoXX_XX_XXXX(self._salidas_transitorias_REQUISITO_CALIF_BUENO)}.')

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
                    print(f' - Teniendo en cuenta que se comenzó a ejecutar la pena el día {Datetime_date_enFormatoXX_XX_XXXX(self._fecha_inicio_ejecucion)} y que se obtuvo el requisito de calificación "bueno" el día {Datetime_date_enFormatoXX_XX_XXXX(self._fecha_calificacion_BUENO)}, los 2/3 de pena con calificación "bueno" se cumplirán el día {Datetime_date_enFormatoXX_XX_XXXX(self._salidas_transitorias_REQUISITO_CALIF_BUENO)}.')                   

                fecha_mayor = Comparar_fechas_y_devolver_la_mayor(self._salidas_transitorias_COMPUTO, self._salidas_transitorias_REQUISITO_CALIF_EJEMPLAR, self._fecha_calificacion_BUENO)                                
                print(f' - En este contexto, y teniendo en cuenta las fechas de cada requisito, las salidas transitorias podrían obtenerse el día {Datetime_date_enFormatoXX_XX_XXXX(fecha_mayor)}.')

        # Imprime advertencias, si corresponde
        if self._regimen_normativo._regimen_ST == ST_REGIMENES._Ley_25948.value and self._monto_de_pena.delitosExcluidosLey25948:
            print('ADVERTENCIA: No aplicaría el instituto de las Salidas Transitorias porque se condenó por alguno de los delitos excluídos, por art. 56 bis, ley 24.660 (según reforma de la ley 25.948).')            
        
        if self._regimen_normativo._regimen_ST == ST_REGIMENES._Ley_27375.value and self._monto_de_pena.delitosExcluidosLey27375:
            print('ADVERTENCIA: No aplicaría el instituto de las Salidas Transitorias porque se condenó por alguno de los delitos excluídos, por art. 56 bis -17.III-, ley 24.660 (según reforma de la ley 27.375).')            
        
        if (self._regimen_normativo._regimen_ST == ST_REGIMENES._Ley_27375.value
            and self._monto_de_pena.perpetua):
            print('ADVERTENCIA: Las salidas transitorias no estarían legalmente previstas para una pena perpetua (ver art. 17, ley 24.660, según ley 27.375).\nNo obstante, se realiza el cómputo mediante una interpretación amplia del art. 17.I.a de esa ley.')

    def _ImprimirSTRINGLibertadAsistida(self):
        
        if self._regimen_normativo._regimen_LA == LA_REGIMENES._No_aplica.value:
            return
        
        if self._monto_de_pena.perpetua:
            return
        
        print(Separadores._separadorComun)
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

    def _ImprimirSTRINGRegimenPreparatorioParaLaLiberacion(self):

        if self._regimen_normativo._regimen_PREPLIB == REGPREPLIB_REGIMENES._No_aplica.value:
            return
        
        if self._monto_de_pena.perpetua:
            return
        
        if self._regimen_normativo._regimen_PREPLIB == REGPREPLIB_REGIMENES._Ley_27375.value:
            print(Separadores._separadorComun)
            print('RÉGIMEN PREPARATORIO PARA LA LIBERTAD')
            print('-------------------------------------')
            print(f' - El régimen preparatorio para la libertad comienza el día {Datetime_date_enFormatoXX_XX_XXXX(self._regimen_preparacion_libertad_COMPUTO)}.')

    def _ImprimirSTRINGMultaUnidadesFijasEnPesos(self):
        if self._regimen_normativo._regimen_UNIDADESFIJAS == 'No aplica':
            return
        
        if self._monto_multa_unidades_fijas == 'NULL':
            return
        
        print(Separadores._separadorComun)
        print('MULTA')
        print('-----')
        print(f' - Valor de la unidad fija: ${NumeroConSeparadorDeMiles(self._regimen_normativo.UNIDADES_FIJAS(UNIDADESFIJAS_KEYS._valorDeLaUnidadFija))}')
        print(f' - Multa en pesos: ${NumeroConSeparadorDeMiles(self._multa_unidadesFijas_en_pesos)}')

class ComputPenaEjecucionCondicional(Computo):
    def __init__(self,
                 fechaDeSentencia:datetime.date='NULL',
                 fechaFirmezaDeSentencia:datetime.date='NULL',
                 montoDePena:MontoDePena='NULL') -> None:
        
        # DEFINE VARIABLES INTERNAS
        self.requisito27CP = TiempoEn_Años_Meses_Dias(_años=4)
        self.requisito51CP_EjecCond  = TiempoEn_Años_Meses_Dias(_años=10)

        # VARIABLES CON EL INPUT
        self._fecha_de_sentencia = fechaDeSentencia
        self._fecha_firmeza_de_sentencia = fechaFirmezaDeSentencia
        self._monto_de_pena = montoDePena

        # VARIABLES CON LOS DATOS
        self._vencimiento_de_pena = 'NULL'
        self._caducidad_de_pena = 'NULL'
        self._vencimiento_plazo_de_control = 'NULL'

        self._CalcularVencimientoYCaducidad()

        self._ImprimirDatosGenerales()
        self._ImprimirVencimiento_y_Caducidad()

    def _CalcularVencimientoYCaducidad(self):
        
        self._vencimiento_de_pena = self._SumarMontoDePena(self._fecha_de_sentencia, self.requisito27CP)
        self._caducidad_de_pena = self._SumarMontoDePena(self._fecha_de_sentencia, self.requisito51CP_EjecCond)        
        self._vencimiento_plazo_de_control = self._SumarMontoDePena(self._fecha_firmeza_de_sentencia, self._monto_de_pena, _sumarPlazoControl=True)
    
    def _ImprimirDatosGenerales(self):
        print(Separadores._separadorComun)
        print('DATOS INGRESADOS')
        print('----------------')
        print(f' - Fecha de sentencia: {Datetime_date_enFormatoXX_XX_XXXX(self._fecha_de_sentencia)}')
        print(f' - Fecha de firmeza de la sentencia: {Datetime_date_enFormatoXX_XX_XXXX(self._fecha_firmeza_de_sentencia)}')
        print(f' - La pena es de {self._monto_de_pena.años} año(s), {self._monto_de_pena.meses} mes(es) y {self._monto_de_pena.dias} día(s) de ejecución condicional.')                
        print(f' - El plazo de control es de {self._monto_de_pena.plazoControl_años} año(s), {self._monto_de_pena.plazoControl_meses} mes(es) y {self._monto_de_pena.plazoControl_dias} día(s).')

    def _ImprimirVencimiento_y_Caducidad(self):
        print(Separadores._separadorComun)
        print('COMPUTO DE PENA')
        print('---------------')        
        print(f' - La sentencia ee tiene por no pronunciada el día {Datetime_date_enFormatoXX_XX_XXXX(self._vencimiento_de_pena)}')
        print(f' - El plazo de control finaliza el {Datetime_date_enFormatoXX_XX_XXXX(self._vencimiento_plazo_de_control)}')
        print(f' - Caducidad: {Datetime_date_enFormatoXX_XX_XXXX(self._caducidad_de_pena)}')

def _DEBUG_PENA_TEMPORAL():    
    fechaDelHecho = datetime.date(2018, 5, 26)
    fechaDeDetencionInput = datetime.date(2020, 1, 1)
    montoDePena = MontoDePena(es_perpetua=True, _esPorDelitosExcluidosLey27375=True, _esPorDelitosExcluidosLey25948=True)
    montoUnidadesFijas='NULL'
    otrasDetenciones='NULL'
    estimuloEducativo=TiempoEn_Años_Meses_Dias()
    #fechaInicioEjecucion=datetime.date(2022, 6, 1)
    fechaInicioEjecucion=datetime.date(2022, 1, 1)
    fechaCalificacionBUENO=datetime.date(2023, 1, 1)    
    #fechaIngresoPeriodoDePrueba=datetime.date(2024, 1, 1)
    fechaIngresoPeriodoDePrueba='NULL'
    #fechaCalificacionEJEMPLAR=datetime.date(2023, 9, 1)
    fechaCalificacionEJEMPLAR='NULL'
    vuelveARestarOtrasDetencionesyAplicar140enST=False
    
    computo = ComputoPenaTemporalOPerpetua(fechaDelHecho=fechaDelHecho,
        fechaDeDetencion=fechaDeDetencionInput,
        montoDePena=montoDePena,
        montoUnidadesFijas=montoUnidadesFijas,
        otrasDetenciones=otrasDetenciones,
        estimuloEducativo=estimuloEducativo,
        fechaInicioEjecucion=fechaInicioEjecucion,
        fechaCalificacionBUENO=fechaCalificacionBUENO,
        fechaIngresoPeriodoDePrueba=fechaIngresoPeriodoDePrueba,
        fechaCalificacionEJEMPLAR=fechaCalificacionEJEMPLAR,
        vuelveARestarOtrasDetencionesyAplicar140enST=vuelveARestarOtrasDetencionesyAplicar140enST)   

if __name__ == '__main__':
    
    _DEBUG_PENA_TEMPORAL()

    print('')
    print('HAY QUE CORRER ESTO DESDE MAIN_APP')