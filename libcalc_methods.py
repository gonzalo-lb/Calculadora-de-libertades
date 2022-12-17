import os
from typing import Union
import datetime
import json
from dateutil.relativedelta import relativedelta
from enum_keys import *

class TiempoEn_Años_Meses_Dias():
    def __init__(self, _años:int=0, _meses:int=0, _dias:int=0):        
        self.años = _años
        self.meses = _meses
        self.dias = _dias        
    
    def __str__(self):               
        return '...{} año(s), {} mes(es) y {} día(s)...'.format(self.años, self.meses, self.dias)

class MontoDePena(TiempoEn_Años_Meses_Dias):
    def __init__(self,
    _años: int = 0,
    _meses: int = 0,
    _dias: int = 0,
    es_perpetua: bool = False,
    esDeEjecucionCondicional:bool=False,
    hayReclusionIndetArt52CP:bool=False,
    _plazoControlAños:int=0,
    _plazoControlMeses:int=0,
    _plazoControlDias:int=0,
    _esReincidente:bool=False,
    _esPorDelitosExcluidosLey27375:bool=False,
    _esPorDelitosExcluidosLey25892:bool=False,
    _esPorDelitosExcluidosLey25948:bool=False):
        super().__init__(_años, _meses, _dias)
        self.reincidencia = _esReincidente
        self.perpetua = es_perpetua
        self.ejecucionCondicional = esDeEjecucionCondicional
        self.reclusionPorTiempoIndeterminado = hayReclusionIndetArt52CP
        self.delitosExcluidosLey25948 = _esPorDelitosExcluidosLey25948
        self.delitosExcluidosLey25892 = _esPorDelitosExcluidosLey25892
        self.delitosExcluidosLey27375 = _esPorDelitosExcluidosLey27375        
        self.plazoControl_años = _plazoControlAños
        self.plazoControl_meses = _plazoControlMeses
        self.plazoControl_dias = _plazoControlDias

        warning = self.perpetua + self.ejecucionCondicional + self.reclusionPorTiempoIndeterminado + self.reincidencia
        if warning > 1 and self.ejecucionCondicional:
            print('[[[ADVERTENCIA: Se ingresó pena de ejecución condicional junto con otra circunstancia incompatible (reincidencia, pena perpetua o reclusión por tiempo indeterminado)]]]')

        if self.perpetua:
            self.años = self.meses = self.dias = 0
    
    def _Return_TiempoEn_Años_Meses_Dias(self):
        return TiempoEn_Años_Meses_Dias(self.años, self.meses, self.dias)
    
    def __str__(self):
        if self.perpetua:
            return 'Es una pena perpetua'
        'La pena es de {} año(s), {} mes(es) y {} día(s).'.format(self.años, self.meses, self.dias)
        if self.reclusionPorTiempoIndeterminado:
            return 'La pena es de {} año(s), {} mes(es) y {} día(s), con la accesoria de reclusión por tiempo indeterminado (art. 52 CP).'.format(self.años, self.meses, self.dias)
        else:
            return 'La pena es de {} año(s), {} mes(es) y {} día(s).'.format(self.años, self.meses, self.dias)

class OtraDetencion():    
    
    # class OtraDetencion():  CLASS VIEJA  
#     def __init__(self, fecha_de_detencion:datetime.datetime, fecha_de_libertad:datetime.datetime, nombre:str="Sin nombre"):
#         self._nombre = nombre
#         self._detencion = fecha_de_detencion
#         self._libertad = fecha_de_libertad
#         self._tiempoDeDetencion = MontoDePena()
#         self._CalcularTiempoDeDetencion()
    
#     def _CalcularTiempoDeDetencion(self):
#         if FechaA_es_Mayor_Que_FechaB(self._detencion, self._libertad):            
#             raise Exception('ERROR: Se ingresó una fecha de detención posterior a la fecha de libertad.')
        
#         fecha_temp = self._detencion
#         _meses = 0
#         _años = 0
#         _dias = 1

#         if self._detencion.day > self._libertad.day:
#             _meses -= 1
        
#         while fecha_temp.month != self._libertad.month:
#             _meses += 1
#             fecha_temp += relativedelta(months=1)
        
#         while fecha_temp.year != self._libertad.year:
#             _años += 1
#             fecha_temp += relativedelta(years=1)
        
#         while fecha_temp.day != self._libertad.day:
#             _dias += 1
#             fecha_temp += relativedelta(days=1)
        
#         self._tiempoDeDetencion.años = _años
#         self._tiempoDeDetencion.meses = _meses
#         self._tiempoDeDetencion.dias = _dias

#         print('Este tiempo de detención es de: {}'.format(self._tiempoDeDetencion)) 
    
    def __init__(self, fecha_de_detencion:datetime.datetime, fecha_de_libertad:datetime.datetime, nombre:str="Sin nombre"):
        self._nombre = nombre
        self._detencion = fecha_de_detencion
        self._libertad = fecha_de_libertad
        self._tiempoDeDetencion = MontoDePena()
        self._CalcularTiempoDeDetencion()
    
    def _CalcularTiempoDeDetencion(self):
        if FechaA_es_Mayor_Que_FechaB(self._detencion, self._libertad):            
            raise Exception('ERROR: Se ingresó una fecha de detención posterior a la fecha de libertad.')
        
        if FechaA_es_Igual_Que_FechaB(self._detencion, self._libertad):
            self._tiempoDeDetencion.dias = 1
            print('Este tiempo de detención es de {} año(s), {} mes(es) y {} día(s)'.format(self._tiempoDeDetencion.años, self._tiempoDeDetencion.meses, self._tiempoDeDetencion.dias))
            return
        
        fecha_temp = self._detencion
        _meses = 0
        _años = 0
        _dias = 0
        se_paso = False

        # Primero suma meses/años y los acumula hasta que se pase de la fecha de libertad, o que sean iguales
        while se_paso == False:
            fecha_previa = fecha_temp
            fecha_temp += relativedelta(months=1)
            if (FechaA_es_Mayor_Que_FechaB(fecha_temp, self._libertad) == False
            or FechaA_es_Igual_Que_FechaB(fecha_temp, self._libertad) == True):
                _meses += 1
                if _meses == 12:
                    _meses = 0
                    _años += 1
            else:
                se_paso = True
                fecha_temp = fecha_previa
        
        # Luego, hace lo mismo con los días
        se_paso = False
        while se_paso == False:
            fecha_previa = fecha_temp
            fecha_temp += relativedelta(days=1)
            if (FechaA_es_Mayor_Que_FechaB(fecha_temp, self._libertad) == False
            or FechaA_es_Igual_Que_FechaB(fecha_temp, self._libertad) == True):
                _dias += 1                
            else:
                se_paso = True
        
        self._tiempoDeDetencion.años = _años
        self._tiempoDeDetencion.meses = _meses
        self._tiempoDeDetencion.dias = _dias

        # Aplica correcciones
        if (self._tiempoDeDetencion.años == 0
        and self._tiempoDeDetencion.meses == 0):
            self._tiempoDeDetencion.dias += 1

        print('Este tiempo de detención es de {} año(s), {} mes(es) y {} día(s)'.format(self._tiempoDeDetencion.años, self._tiempoDeDetencion.meses, self._tiempoDeDetencion.dias))

class RegimenNormativoAplicable():
    def __init__(self, _fechaDelHecho:datetime.date):
        
        # CARGA LOS ARCHIVOS JSON EN VARIABLES

        with open('Regimenes/libertadCondicional.json', encoding='utf-8') as reg_LC:
            self._JSON_LC = json.load(reg_LC)

        with open('Regimenes/salidasTransitorias.json', encoding='utf-8') as reg_ST:
            self._JSON_ST = json.load(reg_ST)
        
        with open('Regimenes/libertadAsistida.json', encoding='utf-8') as reg_LA:
            self._JSON_LA = json.load(reg_LA)
        
        with open('Regimenes/regimenPrepLib.json', encoding='utf-8') as reg_PrepLib:
            self._JSON_PREPLIB = json.load(reg_PrepLib)
        
        with open('Regimenes/unidadesFijas.json', encoding='utf-8') as reg_unidadesFijas:
            self._JSON_UNIDADESFIJAS = json.load(reg_unidadesFijas)
            # En este JSON, la información de vigencia de la Resolución MSEG 270/2016 corresponde a la de la
            # ley 27.302, porque desde esa fecha aplica el régimen de las Unidades Fijas. Los formularios
            # ya existían de antes
        
        with open('Regimenes/delitosExcluidosLib.json', encoding='utf-8') as textoDelitosExcluidosLib:
            self._JSON_DELITOSEXCLUIDOSLIB = json.load(textoDelitosExcluidosLib)

        # DETERMINA RÉGIMEN DE LIBERTAD CONDICIONAL

        self._regimen_LC = 'No aplica'
        for key in self._JSON_LC:            
            fecha_implementacion = datetime.date(self._JSON_LC[key][LC_KEYS._fechaImplementacion_YEAR_KEY.value], self._JSON_LC[key][LC_KEYS._fechaImplementacion_MONTH_KEY.value], self._JSON_LC[key][LC_KEYS._fechaImplementacion_DAY_KEY.value])
            if FechaA_es_Mayor_O_Igual_Que_FechaB(_fechaDelHecho, fecha_implementacion):
                self._regimen_LC = key        

        # DETERMINA RÉGIMEN DE SALIDAS TRANSITORIAS

        self._regimen_ST = 'No aplica'
        for key in self._JSON_ST:            
            fecha_implementacion = datetime.date(self._JSON_ST[key][ST_KEYS._fechaImplementacion_YEAR_KEY.value], self._JSON_ST[key][ST_KEYS._fechaImplementacion_MONTH_KEY.value], self._JSON_ST[key][ST_KEYS._fechaImplementacion_DAY_KEY.value])
            if FechaA_es_Mayor_O_Igual_Que_FechaB(_fechaDelHecho, fecha_implementacion):
                self._regimen_ST = key        

        # DETERMINA RÉGIMEN DE LIBERTAD ASISTIDA

        self._regimen_LA = 'No aplica'
        for key in self._JSON_LA:            
            fecha_implementacion = datetime.date(self._JSON_LA[key][LA_KEYS._fechaImplementacion_YEAR_KEY.value], self._JSON_LA[key][LA_KEYS._fechaImplementacion_MONTH_KEY.value], self._JSON_LA[key][LA_KEYS._fechaImplementacion_DAY_KEY.value])
            if FechaA_es_Mayor_O_Igual_Que_FechaB(_fechaDelHecho, fecha_implementacion):
                self._regimen_LA = key
        
        # DETERMINA RÉGIMEN DE PREPARACIÓN PARA LA LIBERTAD

        self._regimen_PREPLIB = 'No aplica'
        for key in self._JSON_PREPLIB:            
            fecha_implementacion = datetime.date(self._JSON_PREPLIB[key][REGPREPLIB_KEYS._fechaImplementacion_YEAR_KEY.value], self._JSON_PREPLIB[key][REGPREPLIB_KEYS._fechaImplementacion_MONTH_KEY.value], self._JSON_PREPLIB[key][REGPREPLIB_KEYS._fechaImplementacion_DAY_KEY.value])
            if FechaA_es_Mayor_O_Igual_Que_FechaB(_fechaDelHecho, fecha_implementacion):
                self._regimen_PREPLIB = key
        
        # DETERMINA RÉGIMEN DE UNIDADES FIJAS

        self._regimen_UNIDADESFIJAS = 'No aplica'
        for key in self._JSON_UNIDADESFIJAS:            
            fecha_implementacion = datetime.date(self._JSON_UNIDADESFIJAS[key][UNIDADESFIJAS_KEYS._fechaImplementacion_YEAR_KEY.value], self._JSON_UNIDADESFIJAS[key][UNIDADESFIJAS_KEYS._fechaImplementacion_MONTH_KEY.value], self._JSON_UNIDADESFIJAS[key][UNIDADESFIJAS_KEYS._fechaImplementacion_DAY_KEY.value])
            if FechaA_es_Mayor_O_Igual_Que_FechaB(_fechaDelHecho, fecha_implementacion):
                self._regimen_UNIDADESFIJAS = key        
    
    def LIBERTAD_CONDICIONAL(self, ask:LC_KEYS):
        return self._JSON_LC[self._regimen_LC][ask.value]
    
    def SALIDAS_TRANSITORIAS(self, ask:ST_KEYS):
        return self._JSON_ST[self._regimen_ST][ask.value]
    
    def LIBERTAD_ASISTIDA(self, ask:LA_KEYS):
        return self._JSON_LA[self._regimen_LA][ask.value]
    
    def REGIMEN_PREPARACION_LIBERTAD(self, ask:REGPREPLIB_KEYS):
        return self._JSON_PREPLIB[self._regimen_PREPLIB][ask.value]
    
    def UNIDADES_FIJAS(self, ask:UNIDADESFIJAS_KEYS):
        return self._JSON_UNIDADESFIJAS[self._regimen_UNIDADESFIJAS][ask.value]
    
    def DELITOS_EXCLUIDOS_LIBERTAD(self, ask:DELITOS_EXCLUIDOS_LIB_KEYS):
        return self._JSON_DELITOSEXCLUIDOSLIB[ask.value]
    
    def _ImprimirOutput(self, imprimir_reg_unidadesFijas:bool=False):
        print(Separadores._separadorComun)
        print('REGIMEN LEGAL APLICABLE')
        print('-----------------------')
        print(f' - Libertad condicional: {self._regimen_LC}')
        print(f' - Salidas transitorias: {self._regimen_ST}')
        print(f' - Libertad asistida: {self._regimen_LA}')
        print(f' - Régimen preparatorio para la liberación: {self._regimen_PREPLIB}')
        if imprimir_reg_unidadesFijas:
            print(f' - Unidades fijas: {self.UNIDADES_FIJAS(UNIDADESFIJAS_KEYS._denominacion_KEY)}')    
    
    def _ArmarSTRING(self, imprimir_reg_unidadesFijas:bool=False):
        treturn = []
        treturn.append(Separadores._separadorComun)
        treturn.append('REGIMEN LEGAL APLICABLE')
        treturn.append('-----------------------')
        treturn.append(f' - Libertad condicional: {self._regimen_LC}')
        treturn.append(f' - Salidas transitorias: {self._regimen_ST}')
        treturn.append(f' - Libertad asistida: {self._regimen_LA}')
        treturn.append(f' - Régimen preparatorio para la liberación: {self._regimen_PREPLIB}')
        if imprimir_reg_unidadesFijas:
            treturn.append(f' - Unidades fijas: {self.UNIDADES_FIJAS(UNIDADESFIJAS_KEYS._denominacion_KEY)}')
        return treturn

class Preguntas_Input_Pena_TemporalOPerpetua():
    def __init__(self, pena_perpetua:bool=False):        
        
        # Argumentos
        self._ARGUMENTOS_pena_perpetua = pena_perpetua

        self._fecha_del_hecho = 'NULL'
        self._regimen_normativo = 'NULL'
        self._fecha_de_detencion = 'NULL'
        self._monto_de_pena = 'NULL'
        self._monto_multa = 'NULL'
        self._otras_detenciones = 'NULL'
        self._estimulo_educativo = 'NULL'

        self._fecha_inicio_ejecucion = 'NULL'
        self._esta_ejecutando_pena = False
        self._fecha_ingreso_periodo_de_prueba = 'NULL'
        self._fecha_calificacion_BUENO = 'NULL'
        self._fecha_calificacion_EJEMPLAR = 'NULL'
        self._vuelve_a_restar_otras_detenciones_y_140_en_ST = False

        self.GetConsoleInput_HacerPreguntas()

    def GetConsoleInput_HacerPreguntas(self):

        # Si es por una perpetua, primero pregunta por la accesoria de reclusión por tiempo indeterminado, ya que
        # si se aplicó, las demás preguntas y cálculos no tendrían sentido
        if self._ARGUMENTOS_pena_perpetua:            
            print(Separadores._separadorComun)
            user_input_52 = input('¿Se aplicó la accesoria del 52 CP (reclusión por tiempo indeterminado)? (S/N): ')
            if user_input_52 == "S" or user_input_52 == "s":
                self._monto_de_pena = MontoDePena(es_perpetua=True)
                self._monto_de_pena.reclusionPorTiempoIndeterminado = True                
                print(' - Se aplicó la accesoria de reclusión por tiempo indeterminado.')
                return
            else:
                print(' - No hay accesoria de reclusión por tiempo indeterminado.')                

        # Fecha del hecho y cálculo del régimen normativo
        print(Separadores._separadorComun)
        self._fecha_del_hecho = GetConsoleInput_Fecha('Ingresar la fecha del hecho: ')
        self._regimen_normativo = RegimenNormativoAplicable(self._fecha_del_hecho)
        print(f' - Fecha ingresada: {Datetime_date_enFormatoXX_XX_XXXX(self._fecha_del_hecho)}')
        
        # Fecha de detención
        print(Separadores._separadorComun)
        self._fecha_de_detencion = GetConsoleInput_Fecha('Ingresar fecha de detención: ')
        print(f' - Fecha ingresada: {Datetime_date_enFormatoXX_XX_XXXX(self._fecha_de_detencion)}')
        
        # Monto de pena
        if self._ARGUMENTOS_pena_perpetua:
            self._monto_de_pena = MontoDePena(es_perpetua=True)
        else:
            print(Separadores._separadorComun)
            self._monto_de_pena = GetConsoleInput_MontoDePena_temporal()
            print(f' - La pena ingresada es de {self._monto_de_pena.años} año(s), {self._monto_de_pena.meses} mes(es), {self._monto_de_pena.dias} día(s).')

        # Unidades Fijas
        if self._regimen_normativo._regimen_UNIDADESFIJAS != 'No aplica':
            print(Separadores._separadorComun)
            self._monto_multa = GetConsoleInput_Multa_Unidades_Fijas('Monto de la multa (en Unidades Fijas): ')
            if self._monto_multa == 'NULL':
                print(' - No se ingresó monto de multa.')
            else:
                print(f' - El monto ingresado es de {self._monto_multa} Unidades Fijas.')

        # Reincidencia
        if self._regimen_normativo.LIBERTAD_CONDICIONAL(LC_KEYS._ask_esReincidente_KEY):            
            print(Separadores._separadorComun)
            while True:
                user_input = input('¿Hay declaración de reincidencia? (S/N): ')
                if user_input == "N" or user_input == "n" or user_input == '':
                    self._monto_de_pena.reincidencia = False
                    print(' - No es reincidente.')
                    break
                if user_input == "S" or user_input == "s":
                    self._monto_de_pena.reincidencia = True
                    print(' - Es reincidente.')
                    break
                print('ERROR: Solo se puede responder con "s" o "n"')
        
        # Si es pena temporal, pregunta si se aplicó la reclusión por tiempo indeterminado
        if self._ARGUMENTOS_pena_perpetua == False:            
            if self._regimen_normativo.SALIDAS_TRANSITORIAS(ST_KEYS._ask_siHayAccesoria52) or self._regimen_normativo.LIBERTAD_CONDICIONAL(LC_KEYS._ask_siHayAccesoria52):
                print(Separadores._separadorComun)
                while True:
                    user_input = input('¿Se aplicó la accesoria del 52 CP (reclusión por tiempo indeterminado)? (S/N): ')
                    if user_input == "N" or user_input == "n" or user_input == '':
                        self._monto_de_pena.reclusionPorTiempoIndeterminado = False
                        print(' - No hay accesoria de reclusión por tiempo indeterminado.')
                        break
                    if user_input == "S" or user_input == "s":
                        self._monto_de_pena.reclusionPorTiempoIndeterminado = True
                        print(' - Se aplicó la accesoria de reclusión por tiempo indeterminado.')
                        break
                    print('ERROR: Solo se puede responder con "s" o "n"')

        # Otros tiempos de detención a computar
        print(Separadores._separadorComun)
        self._otras_detenciones = GetConsoleInput_OtrosTiemposDeDetencion()
        if self._otras_detenciones == 'NULL':
            print(' - No se ingresaron otras detenciones a computar.')
        else:
            print(' - Se van a computar las siguientes detenciones:')
            for otra_det in self._otras_detenciones:                
                print(f'    - "{otra_det._nombre}": {otra_det._tiempoDeDetencion.años} año(s), {otra_det._tiempoDeDetencion.meses} mes(es) y {otra_det._tiempoDeDetencion.dias} día(s).')

        # Estímulo educativo
        print(Separadores._separadorComun)
        self._estimulo_educativo = GetConsoleInput_EstimuloEducativo()
        if self._estimulo_educativo.años == 0 and self._estimulo_educativo.meses == 0 and self._estimulo_educativo.dias == 0:
            print(' - No se aplica el estímulo educativo.')
        else:
            print(f' - El estímulo educativo es de {self._estimulo_educativo.años} año(s), {self._estimulo_educativo.meses} mes(es) y {self._estimulo_educativo.dias} día(s).')                
            
        # PREGUNTAR SI ES POR DELITOS EXCLUIDOS LEY 25.892 o 25.948, según corresponda (son los mismos delitos)
        if (self._regimen_normativo.LIBERTAD_CONDICIONAL(LC_KEYS._ask_delitosExcluidos25892_KEY)
            or self._regimen_normativo.SALIDAS_TRANSITORIAS(ST_KEYS._ask_delitosExcluidos25948_KEY)
            or self._regimen_normativo.LIBERTAD_ASISTIDA(LA_KEYS._ask_delitosExcluidos25948_KEY)):
            print(Separadores._separadorComun)
            while True:
                print(self._regimen_normativo.DELITOS_EXCLUIDOS_LIBERTAD(DELITOS_EXCLUIDOS_LIB_KEYS._Ley_25892_y_25948_KEY))
                user_input = input('¿La condena es por alguno de los siguientes delitos? (S/N): ')
                if user_input == "N" or user_input == "n" or user_input == '':
                    if self._regimen_normativo.LIBERTAD_CONDICIONAL(LC_KEYS._ask_delitosExcluidos25892_KEY):
                        self._monto_de_pena.delitosExcluidosLey25892 = False
                    if(self._regimen_normativo.SALIDAS_TRANSITORIAS(ST_KEYS._ask_delitosExcluidos25948_KEY)
                       or self._regimen_normativo.LIBERTAD_ASISTIDA(LA_KEYS._ask_delitosExcluidos25948_KEY)):
                        self._monto_de_pena.delitosExcluidosLey25948 = False
                    print(' - No')
                    break
                if user_input == "S" or user_input == "s":
                    if self._regimen_normativo.LIBERTAD_CONDICIONAL(LC_KEYS._ask_delitosExcluidos25892_KEY):
                        self._monto_de_pena.delitosExcluidosLey25892 = True
                    if(self._regimen_normativo.SALIDAS_TRANSITORIAS(ST_KEYS._ask_delitosExcluidos25948_KEY)
                       or self._regimen_normativo.LIBERTAD_ASISTIDA(LA_KEYS._ask_delitosExcluidos25948_KEY)):
                        self._monto_de_pena.delitosExcluidosLey25948 = True
                    print(' - Si')
                    break
                print('ERROR: Solo se puede responder con "s" o "n"')

        # PREGUNTAR SI ES POR DELITOS EXCLUIDOS LEY 27.375
        if self._regimen_normativo.LIBERTAD_CONDICIONAL(LC_KEYS._ask_delitosExcluidos27375_KEY) or self._regimen_normativo.SALIDAS_TRANSITORIAS(ST_KEYS._ask_delitosExcluidos27375_KEY) or self._regimen_normativo.LIBERTAD_ASISTIDA(LA_KEYS._ask_delitosExcluidos27375_KEY) or self._regimen_normativo.REGIMEN_PREPARACION_LIBERTAD(REGPREPLIB_KEYS._ask_delitosExcluidos27375_KEY):
            print(Separadores._separadorComun)
            while True:
                print(self._regimen_normativo.DELITOS_EXCLUIDOS_LIBERTAD(DELITOS_EXCLUIDOS_LIB_KEYS._Ley_27375_KEY))
                user_input = input('¿La condena es por alguno de los delitos enumerados en la ley 27.375? (S/N): ')
                if user_input == "N" or user_input == "n" or user_input == '':
                    self._monto_de_pena.delitosExcluidosLey27375 = False
                    print(' - No')
                    break
                if user_input == "S" or user_input == "s":
                    self._monto_de_pena.delitosExcluidosLey27375 = True
                    print(' - Si')
                    break
                print('ERROR: Solo se puede responder con "s" o "n"')

        # PREGUNTA FECHA DE INICIO DE EJECUCIÓN DE PENA
        if self._regimen_normativo._regimen_LC == LC_REGIMENES._Ley_27375.value or self._regimen_normativo._regimen_ST == ST_REGIMENES._Ley_27375.value:
            print(Separadores._separadorComun)
            self._fecha_inicio_ejecucion = GetConsoleInput_Fecha('Fecha de inicio de ejecución o de ingreso a REAV (Dejar en blanco si aún no ejecuta pena): ', ENTER_devuelve_NULL=True)
            if self._fecha_inicio_ejecucion == 'NULL':
                print(' - No se ingresó fecha de inicio de ejecución. No se utilizará esta variable en el cómputo.')
                self._esta_ejecutando_pena = False
            else:
                print(f' - Fecha de inicio de ejecución: {Datetime_date_enFormatoXX_XX_XXXX(self._fecha_inicio_ejecucion)}')
                self._esta_ejecutando_pena = True            
        
        # Si está ejecutando pena, hace las otras preguntas
        if self._esta_ejecutando_pena == True:
            # PREGUNTAR SI ESTA EN PERIODO DE PRUEBA, Y DESDE CUÁNDO
            if self._regimen_normativo.SALIDAS_TRANSITORIAS(ST_KEYS._ask_siEstaPeriodoDePruebaYDesdeCuando):
                print(Separadores._separadorComun)
                self._fecha_ingreso_periodo_de_prueba = GetConsoleInput_Fecha('Fecha de ingreso al periodo de prueba (Dejar en blanco si aún no ingresó al periodo de prueba): ', ENTER_devuelve_NULL=True)
                if self._fecha_ingreso_periodo_de_prueba == 'NULL':
                    print(' - No se ingresó fecha de ingreso al periodo de prueba. No se utilizará esta variable en el cómputo.')                    
                else:
                    print(f' - Fecha de ingreso al periodo de prueba: {Datetime_date_enFormatoXX_XX_XXXX(self._fecha_ingreso_periodo_de_prueba)}')                

            # PREGUNTAR SI TIENE CONCEPTO BUENO DURANTE 2/3 DE LA EJECUCIÓN
            if self._regimen_normativo.LIBERTAD_CONDICIONAL(LC_KEYS._ask_2_3ConCalifBUENO_KEY):
                print(Separadores._separadorComun)
                self._fecha_calificacion_BUENO = GetConsoleInput_Fecha('Fecha en la que se obtuvo calificación "BUENO" (Dejar en blanco si aún no se obtuvo): ', ENTER_devuelve_NULL=True)
                if self._fecha_calificacion_BUENO == 'NULL':
                    print(' - No se ingresó fecha en la que se obtuvo calificación "BUENO". No se utilizará esta variable en el cómputo.')                    
                else:
                    print(f' - Fecha en la que se obtuvo calificación "BUENO": {Datetime_date_enFormatoXX_XX_XXXX(self._fecha_calificacion_BUENO)}')

            # PREGUNTAR POR REQUISITO DE CALIFICACIÓN PARA ST
            if self._regimen_normativo.SALIDAS_TRANSITORIAS(ST_KEYS._ask_requisitoDeCalificacion):
                print(Separadores._separadorComun)
                self._fecha_calificacion_EJEMPLAR = GetConsoleInput_Fecha('Fecha en la que se obtuvo calificación "EJEMPLAR" (Dejar en blanco si aún no se obtuvo): ', ENTER_devuelve_NULL=True)
                if self._fecha_calificacion_EJEMPLAR == 'NULL':
                    print(' - No se ingresó fecha en la que se obtuvo calificación "EJEMPLAR". No se utilizará esta variable en el cómputo.')                    
                else:
                    print(f' - Fecha en la que se obtuvo calificación "EJEMPLAR": {Datetime_date_enFormatoXX_XX_XXXX(self._fecha_calificacion_EJEMPLAR)}')
            
            # PREGUNTAR POR CRITERIO PARA APLICAR ESTÍMULO EDUCATIVO EN LAS SALIDAS TRANSITORIAS
            hay_estimulo_educativo = self._estimulo_educativo.años + self._estimulo_educativo.meses + self._estimulo_educativo.dias            
            if self._regimen_normativo._regimen_ST == ST_REGIMENES._Ley_27375.value and hay_estimulo_educativo > 0:
                print(Separadores._separadorComun)
                while True:
                    print('Indicar el criterio para aplicar el estímulo educativo a las salidas transitorias')
                    print(Separadores._separadorComun)
                    print('1 --> Se aplica a los plazos para acceder al periodo de prueba.')
                    print('2 --> Se aplica a los plazos para acceder al periodo de prueba, y al requisito temporal de las salidas transitorias.')                    
                    print(Separadores._separadorComun)
                    user_input = input('INDICAR OPCIÓN: ')
                    if user_input == "1" or user_input == '':
                        self._vuelve_a_restar_otras_detenciones_y_140_en_ST = False
                        print(' - Se aplica la opción 1.')
                        break
                    if user_input == "2":
                        self._vuelve_a_restar_otras_detenciones_y_140_en_ST = True
                        print(' - Se aplica la opción 2.')
                        break                    
                    print('ERROR: Solo se puede responder con números 1 ó 2.')

class Preguntas_Input_Pena_EjecucionCondicional():
    def __init__(self):        
        
        self._fecha_de_sentencia = 'NULL'
        self._fecha_firmeza_de_sentencia = 'NULL'
        self._monto_de_pena = 'NULL'

        self.GetConsoleInput_HacerPreguntas()

    def GetConsoleInput_HacerPreguntas(self):                  

        # Fecha de la sentencia
        print(Separadores._separadorComun)
        self._fecha_de_sentencia = GetConsoleInput_Fecha('Ingresar la fecha de la sentencia: ')        
        print(f' - Fecha ingresada: {Datetime_date_enFormatoXX_XX_XXXX(self._fecha_de_sentencia)}')

        # Fecha de firmeza de la sentencia
        print(Separadores._separadorComun)
        self._fecha_firmeza_de_sentencia = GetConsoleInput_Fecha('Ingresar la fecha en la que la sentencia adquirió firmeza: ')        
        print(f' - Fecha ingresada: {Datetime_date_enFormatoXX_XX_XXXX(self._fecha_firmeza_de_sentencia)}')

        # Monto de pena
        print(Separadores._separadorComun)
        self._monto_de_pena = GetConsoleInput_MontoDePena_temporal(ejecucionCondicional=True)
        print(f' - La pena ingresada es de {self._monto_de_pena.años} año(s), {self._monto_de_pena.meses} mes(es), {self._monto_de_pena.dias} día(s).')
        print(f' - El plazo de control es de {self._monto_de_pena.plazoControl_años} año(s), {self._monto_de_pena.plazoControl_meses} mes(es), {self._monto_de_pena.plazoControl_dias} día(s).')

class Preguntas_Input_NuevoComputoPorLibertadRevocada():
    def __init__(self):        
        
        self._fecha_del_hecho = 'NULL'
        self._fecha_de_egreso = 'NULL'
        self._fecha_nueva_detencion = 'NULL'
        self._fecha_libertad_condicional = 'NULL'
        self._fecha_salidas_transitorias = 'NULL'
        self._vencimiento_de_pena = 'NULL'
        self._libertad_evadida = 'NULL'
        self._computa_tiempo_en_libertad = 'NULL'

        self.GetConsoleInput_HacerPreguntas()

    def GetConsoleInput_HacerPreguntas(self):

        # Tipo de libertad
        print(Separadores._separadorComun)
        while True:
            print('Indicar la circunstancia en la que se revocó la libertad:')
            print(Separadores._separadorComun)
            print('1 --> Se revocó la libertad condicional.')
            print('2 --> Se revocó la libertad asistida.')
            print('3 --> No retornó de una salida transitoria.')
            print('4 --> Fuga del establecimiento penitenciario.')
            print(Separadores._separadorComun)
            user_input = input('INDICAR OPCIÓN: ')
            if user_input == "1":
                self._libertad_evadida = LIBERTAD_EVADIDA._libertad_condicional.value
                print(' - Se aplica la opción 1.')
                break
            if user_input == "2":
                self._libertad_evadida = LIBERTAD_EVADIDA._libertad_asistida.value
                print(' - Se aplica la opción 2.')
                break
            if user_input == "3":
                self._libertad_evadida = LIBERTAD_EVADIDA._salidas_transitorias.value
                print(' - Se aplica la opción 3.')
                break
            if user_input == "4":
                self._libertad_evadida = LIBERTAD_EVADIDA._fuga.value
                print(' - Se aplica la opción 4.')
                break
            print('ERROR: Solo se puede responder con números 1 a 4.')

        # Fecha del hecho
        print(Separadores._separadorComun)
        self._fecha_del_hecho = GetConsoleInput_Fecha('Ingresar la fecha del hecho: ')        
        print(f' - Fecha ingresada: {Datetime_date_enFormatoXX_XX_XXXX(self._fecha_del_hecho)}')

        # Fecha de egreso en libertad
        print(Separadores._separadorComun)
        self._fecha_de_egreso = GetConsoleInput_Fecha('Ingresar la fecha de egreso en libertad: ')        
        print(f' - Fecha ingresada: {Datetime_date_enFormatoXX_XX_XXXX(self._fecha_de_egreso)}')

        # Fecha de la nueva detención
        print(Separadores._separadorComun)
        self._fecha_nueva_detencion = GetConsoleInput_Fecha('Ingresar la fecha de la nueva detención: ')        
        print(f' - Fecha ingresada: {Datetime_date_enFormatoXX_XX_XXXX(self._fecha_nueva_detencion)}')

        # Fecha del vencimiento de pena
        print(Separadores._separadorComun)
        self._vencimiento_de_pena = GetConsoleInput_Fecha('Ingresar la fecha en la que correspondía el vencimiento de pena: ')
        print(f' - Fecha ingresada: {Datetime_date_enFormatoXX_XX_XXXX(self._vencimiento_de_pena)}')
        
        # Pregunta si computa el tiempo en libertad (para casos de libertad condicional o asistida)
        if (self._libertad_evadida == LIBERTAD_EVADIDA._libertad_condicional.value
        or self._libertad_evadida == LIBERTAD_EVADIDA._libertad_asistida.value):
            print(Separadores._separadorComun)
            while True:
                user_input = input('¿Se computa el tiempo que duró la libertad? (S/N): ')
                if user_input == "N" or user_input == "n" or user_input == '':
                    self._computa_tiempo_en_libertad = False
                    print(' - No se computa el tiempo que duró la libertad.')
                    break
                if user_input == "S" or user_input == "s":
                    self._computa_tiempo_en_libertad = True
                    print(' - Se computa el tiempo que duró la libertad.')
                    break
                print('ERROR: Solo se puede responder con "s" o "n"')
        
        # Fecha de libertad condicional
        if (self._libertad_evadida == LIBERTAD_EVADIDA._fuga.value
        or self._libertad_evadida == LIBERTAD_EVADIDA._salidas_transitorias.value):
            print(Separadores._separadorComun)
            self._fecha_libertad_condicional = GetConsoleInput_Fecha('Ingresar la fecha en la que correspondía la libertad condicional (dejar en blanco si no se cuenta con esa fecha): ', ENTER_devuelve_NULL=True)        
            if self._fecha_libertad_condicional == 'NULL':
                print(' - No se ingresó fecha.')
            else:
                print(f' - Fecha ingresada: {Datetime_date_enFormatoXX_XX_XXXX(self._fecha_libertad_condicional)}')
        
        # Fecha de salidas transitorias
        if self._libertad_evadida == LIBERTAD_EVADIDA._fuga.value:
            print(Separadores._separadorComun)
            self._fecha_salidas_transitorias = GetConsoleInput_Fecha('Ingresar la fecha en la que correspondían las salidas transitorias (dejar en blanco si no se cuenta con esa fecha): ', ENTER_devuelve_NULL=True)        
            if self._fecha_salidas_transitorias == 'NULL':
                print(' - No se ingresó fecha.')
            else:
                print(f' - Fecha ingresada: {Datetime_date_enFormatoXX_XX_XXXX(self._fecha_salidas_transitorias)}')

class Separadores():
    _separadorComun = ''

def Datetime_date_enFormatoXX_XX_XXXX(_date:datetime.date):
    if type(_date) is not datetime.date:
        return _date
    
    toRT = str(_date)
    return '{}/{}/{}'.format(toRT[8:10], toRT[5:7], toRT[0:4])

def NumeroConSeparadorDeMiles(numero:Union[int, float]):
    
    if type(numero) is int:    
        return f"{numero:,}".replace(',', '.')
    
    if type(numero) is float:
        numero = f'{numero:,.2f}'.replace(',','h')
        numero = f'{numero}'.replace('.',',')
        numero = f'{numero}'.replace('h','.')
        return numero
    
    print('def NumeroConSeparadorDeMiles: WARNING: El valor ingresao no es ni float ni int. La función no va a hacer nada.')

def FechaA_es_Mayor_Que_FechaB(fecha_a:datetime.date, fecha_b:datetime.date):
    temp = fecha_a - fecha_b    
    if temp.days > 0:
        return True
    else:
        return False

def FechaA_es_Mayor_O_Igual_Que_FechaB(fecha_a:datetime.date, fecha_b:datetime.date):
    temp = fecha_a - fecha_b
    if temp.days >= 0:
        return True    
    else:
        return False

def FechaA_es_Igual_Que_FechaB(fecha_a:datetime.date, fecha_b:datetime.date):
    temp = fecha_a - fecha_b    
    if temp.days == 0:
        return True
    else:
        return False

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

def MontoDeTiempoA_es_Mayor_que_MontoDeTiempoB(tiempo_a:TiempoEn_Años_Meses_Dias, tiempo_b:TiempoEn_Años_Meses_Dias):
    if tiempo_a.años > tiempo_b.años:
        return True
    if tiempo_a.años < tiempo_b.años:
        return False
    if tiempo_a.meses > tiempo_b.meses:
        return True
    if tiempo_a.meses < tiempo_b.meses:
        return False
    if tiempo_a.dias > tiempo_b.dias:
        return True
    else:
        return False    

def es_multiplo(numero, multiplo):
    return numero % multiplo == 0

def GetConsoleInput_Fecha(mensaje_para_el_usuario='Fecha: ', ENTER_devuelve_NULL=False, forceInput:str='') -> datetime.date:
    '''Hace ingresar por consola una fecha (formatos XX/XX/XXXX ó X/X/XX) y la devuelve como un datetime.date\n    
    ENTER_devuelve_NULL=True: Si no se ingresa una fecha válida, devuelve "NULL"\n
    ENTER_devuelve_NULL=False: Si se ingresa una fecha inválida, la vuelve a solicitar\n
    forceInput="": Si se ingresa un string, la función no solicita input, y utiliza ese string como si se hubiera ingresado por consola'''
    while True:
        seImprimioError=False
        try:
            if forceInput == '':
                user_input = input(mensaje_para_el_usuario)                
            else:
                user_input = forceInput
            if len(user_input) < 6 or len(user_input) > 10:                
                if ENTER_devuelve_NULL:
                    return 'NULL'
                else:
                    print('ERROR: No se ingresó una fecha válida')
                    seImprimioError=True
                    raise Exception

            cursor = 0
            number_start = 0
            number_end = 0    
            fecha = []

            for x in range(2):
                for y in range(3):
                    if user_input[cursor] == "/":
                        number_end = cursor - 1
                        break
                    else:
                        cursor += 1
                if number_start == number_end:
                    fecha.append(int(user_input[number_start]))
                else:
                    fecha.append(int(user_input[number_start:number_end+1]))
                
                cursor += 1
                number_start = cursor
            
            # Para el año, busca desde el fondo
            number_end = cursor = len(user_input) - 1
            for y in range(5):
                if user_input[cursor] == "/":
                    number_start = cursor + 1
                    break
                else:
                    cursor -= 1
            
            # Revisa que los años tengan 2 dígitos o 4
            year_digits = len(user_input[number_start:number_end+1])
            if year_digits != 2 and year_digits != 4:
                if ENTER_devuelve_NULL:
                    return 'NULL'
                else:
                    print('ERROR: Solo se aceptan los años en formato de dos o cuatro dígitos.')
                    seImprimioError=True
                    raise Exception                
            
            year = int(user_input[number_start:number_end+1])

            # Si el año ingresado es de dos dígitos, lo pasa a formato de 4 dígitos
            if year_digits == 2:
                if year <= 60:
                    year += 2000
                else:
                    year += 1900

            fecha.append(year)
            return datetime.date(fecha[2], fecha[1], fecha[0])
        except:
            if ENTER_devuelve_NULL:
                return 'NULL'
            else:
                if seImprimioError == False:
                    print('ERROR: No se ingresó una fecha válida')

def GetConsoleInput_MontoDePena_temporal(ejecucionCondicional:bool=False):
    '''Hace ingresar por consola un monto de pena temporal y la devuelve como un MontoDePena()\n
    Por el momento solo pide el monto de tiempo. No consulta por reincidencia, accesoria del 52 CP, etc.'''    
    montoDePena = MontoDePena()
    
    # Intenta tomar monto de pena. Si se ingresa 0, 0, 0, vuelve a intentar
    while True:
        # Ingresar años
        while True:
            try:
                _years = input('Ingresar monto de pena (años): ')
                if _years == '':
                    _years = 0
                    break
                _years = int(_years)
                if _years >= 0 and _years <= 50:
                    break
                print(' - ERROR: El monto de pena en años debe ser un número entero entre 0 y 50.')
            except:
                print(' - ERROR: El monto de pena en años debe ser un número entero entre 0 y 50.')
        
        # Ingresar meses
        while True:
            try:
                _months = input('Ingresar monto de pena (meses): ')
                if _months == '':
                    _months = 0
                    break
                _months = int(_months)
                if _months >= 0 and _months <= 11:
                    break
                print(' - ERROR: El monto de pena en meses debe ser un número entero entre 0 y 11.')
            except:
                print(' - ERROR: El monto de pena en meses debe ser un número entero entre 0 y 11.')

        # Ingresar días
        while True:
            try:
                _days = input('Ingresar monto de pena (días): ')
                if _days == '':
                    _days = 0
                    break
                _days = int(_days)
                if _days >= 0 and _days <= 30:
                    break
                print(' - ERROR: El monto de pena en días debe ser un número entero entre 0 y 30.')    
            except:
                print(' - ERROR: El monto de pena en días debe ser un número entero entre 0 y 30.')
        
        _total = _years + _months + _days
        if _total != 0:
            break
        print(' - ERROR: No se ingresó ninguna pena. Intente de nuevo.')
    
    if ejecucionCondicional:
        _plazoControl_years = 0
        _PlazoControl_months = 0
        _PlazoControl_days = 0
        print(Separadores._separadorComun)
        # Intenta tomar el plazo de control. Si se ingresa 0, 0, 0, vuelve a intentar
        
        # Ingresar años
        while True:
            try:
                _plazoControl_years = input('Ingresar plazo de control (años): ')
                if _plazoControl_years == '':
                    _plazoControl_years = 2
                    break
                _plazoControl_years = int(_plazoControl_years)
                if _plazoControl_years >= 2 and _plazoControl_years <= 4:
                    break
                print(' - ERROR: Solo se puede ingresar un número entero entre 2 y 4.')
            except:
                print(' - ERROR: Solo se puede ingresar un número entero entre 2 y 4.')
        
        if _plazoControl_years != 4:
            # Ingresar meses
            while True:
                try:
                    _PlazoControl_months = input('Ingresar plazo de control (meses): ')
                    if _PlazoControl_months == '':
                        _PlazoControl_months = 0
                        break
                    _PlazoControl_months = int(_PlazoControl_months)
                    if _PlazoControl_months >= 0 and _PlazoControl_months <= 11:
                        break
                    print(' - ERROR: Solo se puede ingresar un número entero entre 0 y 11.')
                except:
                    print(' - ERROR: Solo se puede ingresar un número entero entre 0 y 11.')

            # Ingresar días
            while True:
                try:
                    _PlazoControl_days = input('Ingresar monto de pena (días): ')
                    if _PlazoControl_days == '':
                        _PlazoControl_days = 0
                        break
                    _PlazoControl_days = int(_PlazoControl_days)
                    if _PlazoControl_days >= 0 and _PlazoControl_days <= 30:
                        break
                    print(' - ERROR: Solo se puede ingresar un número entero entre 0 y 30.')    
                except:
                    print(' - ERROR: Solo se puede ingresar un número entero entre 0 y 30.')                
        
        montoDePena.plazoControl_años = _plazoControl_years
        montoDePena.plazoControl_meses = _PlazoControl_months
        montoDePena.plazoControl_dias = _PlazoControl_days
        montoDePena.ejecucionCondicional = True

    # Arma lo que va a devolver
    montoDePena.años = _years
    montoDePena.meses = _months
    montoDePena.dias = _days    

    return montoDePena

def GetConsoleInput_Multa_Unidades_Fijas(mensaje_para_el_usuario:str='Ingresar monto de la multa (en unidades fijas): ', _min:float=45, _max:float=900) -> Union[int,float]:    
    '''_min=45 : Es el monto mínimo de multa que permite la función. Por defecto es 45.\n
       _max=900 : Es el monto máximo de multa que permite la función. Por defecto es 900.\n
       Si el mínimo ingresado es mayor al máximo, la función invierte los valores para que siempre el máximo sea mayor
       o igual al mínimo.\n
       Si se ingresa 0, o nada, devuelve str -> "NULL"'''

    if _min > _max:
        _newMax = _min
        _newMin = _max
        _min = _newMin
        _max = _newMax
    
    while True:
        try:
            _multa = input(mensaje_para_el_usuario)
            if _multa == '' or _multa == 0:
                _multa = 'NULL'
                break
            _multa = int(_multa)
            if _multa >= _min and _multa <= _max:
                break
            print(f' - ERROR: El monto de la multa debe ser un número entre {_min} y {_max}.')
        except:
            print(f' - ERROR: El monto de la multa debe ser un número entre {_min} y {_max}.')
    return _multa

def GetConsoleInput_OtrosTiemposDeDetencion() -> list[OtraDetencion]:
    OTDD = []
    seguir_preguntando = True
    init_query = input('Ingresar otros tiempos de detención a computar? (S/N): ')
    if init_query == "S" or init_query == "s":
        while seguir_preguntando:
            f_det = ''
            f_lib = ''
            f_nombre = input('Ingresar denominación o referencia para esta detención: ')
            if f_nombre == '':
                f_nombre = 'Sin nombre'
            f_det = GetConsoleInput_Fecha('Ingresar fecha de detención del otro tiempo a computar: ')
            f_lib = GetConsoleInput_Fecha('Ingresar fecha de libertad: ')
            este = OtraDetencion(f_det, f_lib, nombre=f_nombre)
            OTDD.append(este)
            seguir = input('Necesita ingresar otro tiempo de detención? (S/N): ')
            if seguir == "S" or seguir == "s":
                seguir_preguntando = True
            else:
                seguir_preguntando = False        
        return OTDD         
    else:
        return "NULL"

def GetConsoleInput_EstimuloEducativo() -> TiempoEn_Años_Meses_Dias:
    
    estimulo = TiempoEn_Años_Meses_Dias()
    
    # Ingresar años
    while True:
        try:
            _years = input('Ingresar estímulo educativo (años): ')
            if _years == '':
                _years = 0
                break
            _years = int(_years)
            if _years >= 0 and _years <= 50:
                break
            print(' - ERROR: El monto en años debe ser un número entre 0 y 50.')
        except:
            print(' - ERROR: El monto en años debe ser un número entre 0 y 50.')
    
    # Ingresar meses
    while True:
        try:
            _months = input('Ingresar estímulo educativo (meses): ')
            if _months == '':
                _months = 0
                break
            _months = int(_months)
            if _months >= 0 and _months <= 11:
                break
            print(' - ERROR: El monto meses debe ser un número entre 0 y 11.')
        except:
            print(' - ERROR: El monto en meses debe ser un número entre 0 y 11.')

    # Ingresar días
    while True:
        try:
            _days = input('Ingresar estímulo educativo (días): ')
            if _days == '':
                _days = 0
                break
            _days = int(_days)
            if _days >= 0 and _days <= 30:
                break
            print(' - ERROR: El monto en días debe ser un número entre 0 y 30.')    
        except:
            print(' - ERROR: El monto en días debe ser un número entre 0 y 30.')    
    

    estimulo.años = _years
    estimulo.meses = _months
    estimulo.dias = _days      

    return estimulo

def RestarOtrasDetenciones(fecha_de_requisito_temporal:datetime.date, otras_detenciones:list[OtraDetencion]):
        toreturn = fecha_de_requisito_temporal
        for otra_det in otras_detenciones:            
            toreturn += relativedelta(days=-otra_det._tiempoDeDetencion.dias)
            toreturn += relativedelta(months=-otra_det._tiempoDeDetencion.meses)
            toreturn += relativedelta(years=-otra_det._tiempoDeDetencion.años)
        return toreturn

if __name__ == '__main__':    
    fechadet = datetime.date(2014, 6, 15)    
    fechalib = datetime.date(2014, 7, 16)
    x = OtraDetencion(fechadet, fechalib)