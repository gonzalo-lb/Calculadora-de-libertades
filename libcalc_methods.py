import os
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
    def __init__(self, fecha_de_detencion:datetime.datetime, fecha_de_libertad:datetime.datetime, nombre:str="Sin nombre"):
        self._nombre = nombre
        self._detencion = fecha_de_detencion
        self._libertad = fecha_de_libertad
        self._tiempoDeDetencion = MontoDePena()
        self._CalcularTiempoDeDetencion()
    
    def _CalcularTiempoDeDetencion(self):
        if FechaA_es_Mayor_Que_FechaB(self._detencion, self._libertad):            
            raise Exception('ERROR: Se ingresó una fecha de detención posterior a la fecha de libertad.')
        
        fecha_temp = self._detencion
        _meses = 0
        _años = 0
        _dias = 1

        if self._detencion.day > self._libertad.day:
            _meses -= 1
        
        while fecha_temp.month != self._libertad.month:
            _meses += 1
            fecha_temp += relativedelta(months=1)
        
        while fecha_temp.year != self._libertad.year:
            _años += 1
            fecha_temp += relativedelta(years=1)
        
        while fecha_temp.day != self._libertad.day:
            _dias += 1
            fecha_temp += relativedelta(days=1)
        
        self._tiempoDeDetencion.años = _años
        self._tiempoDeDetencion.meses = _meses
        self._tiempoDeDetencion.dias = _dias

        print('Este tiempo de detención es de: {}'.format(self._tiempoDeDetencion))    

class RegimenNormativoAplicable():
    def __init__(self, _fechaDelHecho:datetime.date):
        
        # CARGA LOS ARCHIVOS JSON EN VARIABLES

        with open('Regimenes/libertadCondicional.json') as reg_LC:
            self._JSON_LC = json.load(reg_LC)

        with open('Regimenes/salidasTransitorias.json') as reg_ST:
            self._JSON_ST = json.load(reg_ST)
        
        with open('Regimenes/libertadAsistida.json') as reg_LA:
            self._JSON_LA = json.load(reg_LA)
        
        with open('Regimenes/regimenPrepLib.json') as reg_PrepLib:
            self._JSON_PREPLIB = json.load(reg_PrepLib)

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
    
    def LIBERTAD_CONDICIONAL(self, ask:LC_KEYS):
        return self._JSON_LC[self._regimen_LC][ask.value]
    
    def SALIDAS_TRANSITORIAS(self, ask:ST_KEYS):
        return self._JSON_ST[self._regimen_ST][ask.value]
    
    def LIBERTAD_ASISTIDA(self, ask:LA_KEYS):
        return self._JSON_LA[self._regimen_LA][ask.value]
    
    def REGIMEN_PREPARACION_LIBERTAD(self, ask:REGPREPLIB_KEYS):
        return self._JSON_PREPLIB[self._regimen_PREPLIB][ask.value]
    
    def _Imprimir(self):
        print('')
        print(self)

    def __str__(self):
        return '''REGIMEN LEGAL APLICABLE
-----------------------
Libertad condicional: {}
Salidas transitorias: {}
Libertad asistida: {}
Régimen preparatorio para la liberación: {}'''.format(self._regimen_LA, self._regimen_ST, self._regimen_LA, self._regimen_PREPLIB)

class Preguntas_Input():
    def __init__(self):
        self._fecha_del_hecho = 'NULL'
        self._regimen_normativo = 'NULL'
        self._fecha_de_detencion = 'NULL'
        self._monto_de_pena = 'NULL'
        self._otras_detenciones = 'NULL'
        self._estimulo_educativo = 'NULL'

        self._fecha_inicio_ejecucion = 'NULL'
        self._esta_ejecutando_pena = False
        self._fecha_ingreso_periodo_de_prueba = 'NULL'
        self._fecha_calificacion_BUENO = 'NULL'
        self._fecha_calificacion_EJEMPLAR = 'NULL'
        self._vuelve_a_restar_otras_detenciones_y_140_en_ST = False

        self.GetConsoleInput_PreguntasSobreSituacionProcesal()

    def GetConsoleInput_PreguntasSobreSituacionProcesal(self):                  

        print(Separadores._separadorComun)
        self._fecha_del_hecho = GetConsoleInput_Fecha('Ingresar la fecha del hecho (XX/XX/XXXX): ')
        self._regimen_normativo = RegimenNormativoAplicable(self._fecha_del_hecho)
        
        print(Separadores._separadorComun)
        self._fecha_de_detencion = GetConsoleInput_Fecha('Ingresar fecha de detención (XX/XX/XXXX): ')        
        
        print(Separadores._separadorComun)
        self._monto_de_pena = GetConsoleInput_MontoDePena_temporal()

        # PREGUNTAR SI ES REINCIDENTE        
        if self._regimen_normativo.LIBERTAD_CONDICIONAL(LC_KEYS._ask_esReincidente_KEY):            
            print(Separadores._separadorComun)
            while True:
                user_input = input('¿Hay declaración de reincidencia? (S/N): ')
                if user_input == "N" or user_input == "n" or user_input == '':
                    self._monto_de_pena.reincidencia = False
                    break
                if user_input == "S" or user_input == "s":
                    self._monto_de_pena.reincidencia = True
                    break
                print('ERROR: Solo se puede responder con "s" o "n"')

        print(Separadores._separadorComun)
        self._otras_detenciones = GetConsoleInput_OtrosTiemposDeDetencion()

        print(Separadores._separadorComun)
        self._estimulo_educativo = GetConsoleInput_EstimuloEducativo()                    
        
        # PREGUNTAR SI HAY ACCESORIA DEL 52 CP        
        # if self._regimen_normativo.SALIDAS_TRANSITORIAS(ST_KEYS._ask_siHayAccesoria52) or self._regimen_normativo.LIBERTAD_CONDICIONAL(LC_KEYS._ask_siHayAccesoria52):
        #     print(Separadores._separadorComun)
        #     while True:
        #         user_input = input('¿Hay accesoria del 52 CP? (S/N): ')
        #         if user_input == "N" or user_input == "n" or user_input == '':
        #             self._HayAccesoriaDel52 = False
        #             break
        #         if user_input == "S" or user_input == "s":
        #             self._HayAccesoriaDel52 = True
        #             break
        #         print('ERROR: Solo se puede responder con "s" o "n"')  

        #PREGUNTAR SI ES POR LIBERTAD REVOCADA        
        # if self._regimen_normativo.LIBERTAD_CONDICIONAL(LC_KEYS._ask_esComputoPorLCRevocada_KEY) or self._regimen_normativo.LIBERTAD_ASISTIDA(LA_KEYS._ask_nuevoComputoLArevoc_KEY) or self._regimen_normativo.SALIDAS_TRANSITORIAS(ST_KEYS._ask_esComputoPorEvasionDeST_KEY):
        #     print(Separadores._separadorComun)
        #     while True:
        #         print('¿Este cómputo es por una libertad revocada?')
        #         print(Separadores._separadorComun)
        #         print('1 --> No. Es un cómputo común')
        #         print('2 --> Si es por libertad condicional revocada')
        #         print('3 --> Si es por libertad asistida revocada')
        #         print('4 --> Si es por evasión estando en salidas transitorias')
        #         print(Separadores._separadorComun)
        #         user_input = input('INDICAR OPCIÓN: ')
        #         if user_input == "1" or user_input == '':
        #             self._EsComputoPorLCRevocada = False
        #             self._EsComputoPorSTRevocada = False
        #             self._EsComputoPorLARevocada = False
        #             break
        #         if user_input == "2":
        #             self._EsComputoPorLCRevocada = True
        #             self._EsComputoPorSTRevocada = False
        #             self._EsComputoPorLARevocada = False
        #             break
        #         if user_input == "3":
        #             self._EsComputoPorLCRevocada = False
        #             self._EsComputoPorSTRevocada = False
        #             self._EsComputoPorLARevocada = True
        #             break
        #         if user_input == "4":
        #             self._EsComputoPorLCRevocada = False
        #             self._EsComputoPorSTRevocada = True
        #             self._EsComputoPorLARevocada = False
        #             break
        #         print('ERROR: Solo se puede responder con números del 1 al 4')

        # PREGUNTAR SI ES POR DELITOS EXCLUIDOS LEY 25.892
        if self._regimen_normativo.LIBERTAD_CONDICIONAL(LC_KEYS._ask_delitosExcluidos25892_KEY):
            print(Separadores._separadorComun)
            while True:
                print('Delitos excluidos por la ley 25.892: ...')
                user_input = input('¿La condena es por alguno de los delitos enumerados en la ley 25.892? (S/N): ')
                if user_input == "N" or user_input == "n" or user_input == '':
                    self._monto_de_pena.delitosExcluidosLey25892 = False
                    break
                if user_input == "S" or user_input == "s":
                    self._monto_de_pena.delitosExcluidosLey25892 = True
                    break
                print('ERROR: Solo se puede responder con "s" o "n"')

        # PREGUNTAR SI ES POR DELITOS EXCLUIDOS LEY 25.948
        if self._regimen_normativo.SALIDAS_TRANSITORIAS(ST_KEYS._ask_delitosExcluidos25948_KEY) or self._regimen_normativo.LIBERTAD_ASISTIDA(LA_KEYS._ask_delitosExcluidos25948_KEY):
            print(Separadores._separadorComun)
            while True:
                print('Delitos excluidos por la ley 25.948: ...')
                user_input = input('¿La condena es por alguno de los delitos enumerados en la ley 25.948? (S/N): ')
                if user_input == "N" or user_input == "n" or user_input == '':
                    self._monto_de_pena.delitosExcluidosLey25948 = False
                    break
                if user_input == "S" or user_input == "s":
                    self._monto_de_pena.delitosExcluidosLey25948 = True
                    break
                print('ERROR: Solo se puede responder con "s" o "n"')

        # PREGUNTAR SI ES POR DELITOS EXCLUIDOS LEY 27.375
        if self._regimen_normativo.LIBERTAD_CONDICIONAL(LC_KEYS._ask_delitosExcluidos27375_KEY) or self._regimen_normativo.SALIDAS_TRANSITORIAS(ST_KEYS._ask_delitosExcluidos27375_KEY) or self._regimen_normativo.LIBERTAD_ASISTIDA(LA_KEYS._ask_delitosExcluidos27375_KEY) or self._regimen_normativo.REGIMEN_PREPARACION_LIBERTAD(REGPREPLIB_KEYS._ask_delitosExcluidos27375_KEY):
            print(Separadores._separadorComun)
            while True:
                print('Delitos excluidos por la ley 27.375: ...')
                user_input = input('¿La condena es por alguno de los delitos enumerados en la ley 27.375? (S/N): ')
                if user_input == "N" or user_input == "n" or user_input == '':
                    self._monto_de_pena.delitosExcluidosLey27375 = False
                    break
                if user_input == "S" or user_input == "s":
                    self._monto_de_pena.delitosExcluidosLey27375 = True
                    break
                print('ERROR: Solo se puede responder con "s" o "n"')

        # PREGUNTA FECHA DE INICIO DE EJECUCIÓN DE PENA
        if self._regimen_normativo._regimen_LC == LC_REGIMENES._Ley_27375.value or self._regimen_normativo._regimen_ST == ST_REGIMENES._Ley_27375.value:
            print(Separadores._separadorComun)
            self._fecha_inicio_ejecucion = GetConsoleInput_Fecha('Fecha de inicio de ejecución o de ingreso a REAV (Formato: XX/XX/XXXX. Dejar en blanco si aún no ejecuta pena): ', ENTER_devuelve_NULL=True)
            if self._fecha_inicio_ejecucion == 'NULL':
                print(' - No se ingresó fecha de inicio de ejecución. No se utilizará esta variable en el cómputo.')
                self._esta_ejecutando_pena = False
            else:
                print(f' - Fecha de inicio de ejecución: {Datetime_date_enFormatoXX_XX_XXXX(self._fecha_inicio_ejecucion)}')
                self._esta_ejecutando_pena = True
            # while True:                
            #     user_input = input('¿Se encuentra ejecutando pena, o en REAV? (S/N): ')
            #     if user_input == "N" or user_input == "n" or user_input == '':
            #         self._fecha_inicio_ejecucion = 'NULL'
            #         self._esta_ejecutando_pena = False
            #         break
            #     if user_input == "S" or user_input == "s":
            #         self._fecha_inicio_ejecucion = GetConsoleInput_Fecha('Ingresar fecha en la que comenzó la ejecución de pena (XX/XX/XXXX): ', ENTER_devuelve_NULL=True)
            #         self._esta_ejecutando_pena = True
            #         if self._fecha_inicio_ejecucion == 'NULL':
            #             self._esta_ejecutando_pena = False
            #             print('Como no se ingresó una fecha válida, no se utilizará para el cómputo esta variable.')
            #         break
            #     print('ERROR: Solo se puede responder con "s" o "n"')
        
        # Si está ejecutando pena, hace las otras preguntas
        if self._esta_ejecutando_pena == True:
            # PREGUNTAR SI ESTA EN PERIODO DE PRUEBA, Y DESDE CUÁNDO
            if self._regimen_normativo.SALIDAS_TRANSITORIAS(ST_KEYS._ask_siEstaPeriodoDePruebaYDesdeCuando):
                print(Separadores._separadorComun)
                self._fecha_ingreso_periodo_de_prueba = GetConsoleInput_Fecha('Fecha de ingreso al periodo de prueba (Formato: XX/XX/XXXX. Dejar en blanco si aún no ingresó al periodo de prueba): ', ENTER_devuelve_NULL=True)
                if self._fecha_ingreso_periodo_de_prueba == 'NULL':
                    print(' - No se ingresó fecha de ingreso al periodo de prueba. No se utilizará esta variable en el cómputo.')                    
                else:
                    print(f' - Fecha de ingreso al periodo de prueba: {Datetime_date_enFormatoXX_XX_XXXX(self._fecha_ingreso_periodo_de_prueba)}')                

            # PREGUNTAR SI TIENE CONCEPTO BUENO DURANTE 2/3 DE LA EJECUCIÓN
            if self._regimen_normativo.LIBERTAD_CONDICIONAL(LC_KEYS._ask_2_3ConCalifBUENO_KEY):
                print(Separadores._separadorComun)
                self._fecha_calificacion_BUENO = GetConsoleInput_Fecha('Fecha en la que se obtuvo calificación "BUENO" (Formato: XX/XX/XXXX. Dejar en blanco si aún no se obtuvo): ', ENTER_devuelve_NULL=True)
                if self._fecha_calificacion_BUENO == 'NULL':
                    print(' - No se ingresó fecha en la que se obtuvo calificación "BUENO". No se utilizará esta variable en el cómputo.')                    
                else:
                    print(f' - Fecha en la que se obtuvo calificación "BUENO": {Datetime_date_enFormatoXX_XX_XXXX(self._fecha_calificacion_BUENO)}')

            # PREGUNTAR POR REQUISITO DE CALIFICACIÓN PARA ST
            if self._regimen_normativo.SALIDAS_TRANSITORIAS(ST_KEYS._ask_requisitoDeCalificacion):
                print(Separadores._separadorComun)
                self._fecha_calificacion_EJEMPLAR = GetConsoleInput_Fecha('Fecha en la que se obtuvo calificación "EJEMPLAR" (Formato: XX/XX/XXXX. Dejar en blanco si aún no se obtuvo): ', ENTER_devuelve_NULL=True)
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

class Separadores():
    _separadorComun = ''

def Datetime_date_enFormatoXX_XX_XXXX(_date:datetime.date):
    if type(_date) is not datetime.date:
        return _date
    
    toRT = str(_date)
    return '{}/{}/{}'.format(toRT[8:10], toRT[5:7], toRT[0:4])

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

def GetConsoleInput_Fecha(mensaje_para_el_usuario="Ingrese fecha en formato año-mes-día (XX/XX/XXXX): ", ENTER_devuelve_NULL:bool=False):
    '''Hace ingresar por consola una fecha de detención en formato XX/XX/XXXX y la devuelve como un datetime.date\n
    ENTER_devuelve_NULL: En True, si no se ingresa una fecha válida, devuelve "NULL"'''
    if ENTER_devuelve_NULL:
        try:        
            fechaDeDetencionInput = input(mensaje_para_el_usuario)    
            fechaDeDetencionInput_dia = fechaDeDetencionInput[0:2]
            fechaDeDetencionInput_mes = fechaDeDetencionInput[3:5]
            fechaDeDetencionInput_año = fechaDeDetencionInput[6:10]
            if fechaDeDetencionInput[2] != "/" or fechaDeDetencionInput[5] != "/":
                raise Exception
            fechaDeDetencionInput = datetime.date(int(fechaDeDetencionInput_año), int(fechaDeDetencionInput_mes), int(fechaDeDetencionInput_dia))        
            return fechaDeDetencionInput
        except:
            return 'NULL'
    else:
        while True:
            try:        
                fechaDeDetencionInput = input(mensaje_para_el_usuario)    
                fechaDeDetencionInput_dia = fechaDeDetencionInput[0:2]
                fechaDeDetencionInput_mes = fechaDeDetencionInput[3:5]
                fechaDeDetencionInput_año = fechaDeDetencionInput[6:10]
                if fechaDeDetencionInput[2] != "/" or fechaDeDetencionInput[5] != "/":                    
                    raise Exception
                fechaDeDetencionInput = datetime.date(int(fechaDeDetencionInput_año), int(fechaDeDetencionInput_mes), int(fechaDeDetencionInput_dia))        
                return fechaDeDetencionInput
            except:
                print('ERROR: Fecha en formato inválido. La fecha ingresada no tiene formato XX/XX/XXXX o no es una fecha válida.')

def GetConsoleInput_MontoDePena_temporal():
    '''Hace ingresar por consola un monto de pena temporal y la devuelve como un MontoDePena()'''    
    montoDePena = MontoDePena()    
    
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

    return montoDePena

# def GetConsoleInput_MontoDePena():
#     '''Hace ingresar por consola un monto de pena temporal y la devuelve como un MontoDePena()'''
#     clear = lambda: os.system('cls')
#     montoDePena = MontoDePena()

#     solicitar_tipo_de_pena_a_calcular = '''Indicar tipo de pena a calcular:
# 1 --> Pena temporal
# 2 --> Pena perpetua
# '''
#     print(solicitar_tipo_de_pena_a_calcular)
#     opciones_validas = ['1', '2']
#     opcion_elegida = input('Elegir opción: ')    

#     while opcion_elegida not in opciones_validas:
#         clear()
#         print('La opción elegida no es válida. Intentar de nuevo.')
#         print(solicitar_tipo_de_pena_a_calcular)
#         opcion_elegida = input('Elegir opción: ')
    
#     if opcion_elegida == '1': # Pena temporal
#         # Ingresar monto de pena    
#         try:
#             montoDePena.años = int(input('Ingresar monto de pena (años): '))
#         except:
#             montoDePena.años = 0        
#         try:
#             montoDePena.meses = int(input('Ingresar monto de pena (meses): '))        
#         except:
#             montoDePena.meses = 0        
#         try:
#             montoDePena.dias = int(input('Ingresar monto de pena (días): '))        
#         except:
#             montoDePena.dias = 0
    
#     elif opcion_elegida == '2': # Pena perpetua
#         montoDePena.perpetua = True

#     return montoDePena

def GetConsoleInput_OtrosTiemposDeDetencion():
    OTDD = []
    seguir_preguntando = True
    init_query = input('Ingresar otros tiempos de detención a computar? (S/N): ')
    if init_query == "S" or init_query == "s":
        while seguir_preguntando:
            f_det = ''
            f_lib = ''
            f_det = GetConsoleInput_Fecha('Ingresar fecha de detención del otro tiempo a computar (XX/XX/XXXX): ')
            f_lib = GetConsoleInput_Fecha('Ingresar fecha de libertad (XX/XX/XXXX): ')
            este = OtraDetencion(f_det, f_lib)
            OTDD.append(este)
            seguir = input('Necesita ingresar otro tiempo de detención? (S/N): ')
            if seguir == "S" or seguir == "s":
                seguir_preguntando = True
            else:
                seguir_preguntando = False        
        return OTDD         
    else:
        return "NULL"

def GetConsoleInput_EstimuloEducativo():
    estimulo = TiempoEn_Años_Meses_Dias()
    try:
        estimulo.años = int(input('Ingresar estímulo educativo (años): '))
    except:
        estimulo.años = 0        
    try:
        estimulo.meses = int(input('Ingresar estímulo educativo (meses): '))        
    except:
        estimulo.meses = 0        
    try:
        estimulo.dias = int(input('Ingresar estímulo educativo (días): '))        
    except:
        estimulo.dias = 0
    return estimulo

def RestarOtrasDetenciones(fecha_de_requisito_temporal:datetime.date, otras_detenciones:list[OtraDetencion]):
        toreturn = fecha_de_requisito_temporal
        for otra_det in otras_detenciones:            
            toreturn += relativedelta(days=-otra_det._tiempoDeDetencion.dias)
            toreturn += relativedelta(months=-otra_det._tiempoDeDetencion.meses)
            toreturn += relativedelta(years=-otra_det._tiempoDeDetencion.años)
        return toreturn

if __name__ == '__main__':    
    x = Preguntas_Input()