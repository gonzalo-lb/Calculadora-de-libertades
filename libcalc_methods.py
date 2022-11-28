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
            self.__JSON_LC = json.load(reg_LC)

        with open('Regimenes/salidasTransitorias.json') as reg_ST:
            self.__JSON_ST = json.load(reg_ST)
        
        with open('Regimenes/libertadAsistida.json') as reg_LA:
            self.__JSON_LA = json.load(reg_LA)
        
        with open('Regimenes/regimenPrepLib.json') as reg_PrepLib:
            self.__JSON_PREPLIB = json.load(reg_PrepLib)

        # DETERMINA RÉGIMEN DE LIBERTAD CONDICIONAL

        self._regimen_LC = 'No aplica'
        for key in self.__JSON_LC:            
            fecha_implementacion = datetime.date(self.__JSON_LC[key][LC_KEYS._fechaImplementacion_YEAR_KEY.value], self.__JSON_LC[key][LC_KEYS._fechaImplementacion_MONTH_KEY.value], self.__JSON_LC[key][LC_KEYS._fechaImplementacion_DAY_KEY.value])
            if FechaA_es_Mayor_O_Igual_Que_FechaB(_fechaDelHecho, fecha_implementacion):
                self._regimen_LC = key        

        # DETERMINA RÉGIMEN DE SALIDAS TRANSITORIAS

        self._regimen_ST = 'No aplica'
        for key in self.__JSON_ST:            
            fecha_implementacion = datetime.date(self.__JSON_ST[key][ST_KEYS._fechaImplementacion_YEAR_KEY.value], self.__JSON_ST[key][ST_KEYS._fechaImplementacion_MONTH_KEY.value], self.__JSON_ST[key][ST_KEYS._fechaImplementacion_DAY_KEY.value])
            if FechaA_es_Mayor_O_Igual_Que_FechaB(_fechaDelHecho, fecha_implementacion):
                self._regimen_ST = key        

        # DETERMINA RÉGIMEN DE LIBERTAD ASISTIDA

        self._regimen_LA = 'No aplica'
        for key in self.__JSON_LA:            
            fecha_implementacion = datetime.date(self.__JSON_LA[key][LA_KEYS._fechaImplementacion_YEAR_KEY.value], self.__JSON_LA[key][LA_KEYS._fechaImplementacion_MONTH_KEY.value], self.__JSON_LA[key][LA_KEYS._fechaImplementacion_DAY_KEY.value])
            if FechaA_es_Mayor_O_Igual_Que_FechaB(_fechaDelHecho, fecha_implementacion):
                self._regimen_LA = key
        
        # DETERMINA RÉGIMEN DE PREPARACIÓN PARA LA LIBERTAD

        self._regimen_PREPLIB = 'No aplica'
        for key in self.__JSON_PREPLIB:            
            fecha_implementacion = datetime.date(self.__JSON_PREPLIB[key][REGPREPLIB_KEYS._fechaImplementacion_YEAR_KEY.value], self.__JSON_PREPLIB[key][REGPREPLIB_KEYS._fechaImplementacion_MONTH_KEY.value], self.__JSON_PREPLIB[key][REGPREPLIB_KEYS._fechaImplementacion_DAY_KEY.value])
            if FechaA_es_Mayor_O_Igual_Que_FechaB(_fechaDelHecho, fecha_implementacion):
                self._regimen_PREPLIB = key    
    
    def LIBERTAD_CONDICIONAL(self, ask:LC_KEYS):
        return self.__JSON_LC[self._regimen_LA][ask.value]
    
    def SALIDAS_TRANSITORIAS(self, ask:ST_KEYS):
        return self.__JSON_ST[self._regimen_ST][ask.value]
    
    def LIBERTAD_ASISTIDA(self, ask:LA_KEYS):
        return self.__JSON_LA[self._regimen_LA][ask.value]
    
    def REGIMEN_PREPARACION_LIBERTAD(self, ask:REGPREPLIB_KEYS):
        return self.__JSON_PREPLIB[self._regimen_PREPLIB][ask.value]
    
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

class SituacionProcesal():
    def __init__(self, _regimenNormativo:RegimenNormativoAplicable, _getInputPreguntas:bool=True):
        self._RegimenNormativo = _regimenNormativo
        self._EsReincidente = False
        self._EsComputoPorLCRevocada = False
        self._EsComputoPorLARevocada = False
        self._EsComputoPorSTRevocada = False
        self._EsPorDelitosExcluidosLey25892 = False
        self._EsPorDelitosExcluidosLey25948 = False
        self._EsPorDelitosExcluidosLey27375 = False
        self._2_3ConCalifBueno = False
        self._HayAccesoriaDel52 = False
        self._EstaEnPeriodoDePrueba = False
        self._EstaEnPeriodoDePruebaDesde = False
        self._RequisitoDeCalificacionDuranteElUltimoAño_ST = False

        if _getInputPreguntas:
            self.GetConsoleInput_PreguntasSobreSituacionProcesal()

    def GetConsoleInput_PreguntasSobreSituacionProcesal(self):                  

        # PREGUNTAR SI ES REINCIDENTE        
        if self._RegimenNormativo.LIBERTAD_CONDICIONAL(LC_KEYS._ask_esReincidente_KEY):            
            print(Separadores._separadorComun)
            while True:
                user_input = input('¿Hay declaración de reincidencia? (S/N): ')
                if user_input == "N" or user_input == "n" or user_input == '':
                    self._EsReincidente = False
                    break
                if user_input == "S" or user_input == "s":
                    self._EsReincidente = True
                    break
                print('ERROR: Solo se puede responder con "s" o "n"')            
        
        # PREGUNTAR SI HAY ACCESORIA DEL 52 CP        
        if self._RegimenNormativo.SALIDAS_TRANSITORIAS(ST_KEYS._ask_siHayAccesoria52) or self._RegimenNormativo.LIBERTAD_CONDICIONAL(LC_KEYS._ask_siHayAccesoria52):
            print(Separadores._separadorComun)
            while True:
                user_input = input('¿Hay accesoria del 52 CP? (S/N): ')
                if user_input == "N" or user_input == "n" or user_input == '':
                    self._HayAccesoriaDel52 = False
                    break
                if user_input == "S" or user_input == "s":
                    self._HayAccesoriaDel52 = True
                    break
                print('ERROR: Solo se puede responder con "s" o "n"')  

        #PREGUNTAR SI ES POR LIBERTAD REVOCADA        
        if self._RegimenNormativo.LIBERTAD_CONDICIONAL(LC_KEYS._ask_esComputoPorLCRevocada_KEY) or self._RegimenNormativo.LIBERTAD_ASISTIDA(LA_KEYS._ask_nuevoComputoLArevoc_KEY) or self._RegimenNormativo.SALIDAS_TRANSITORIAS(ST_KEYS._ask_esComputoPorEvasionDeST_KEY):
            print(Separadores._separadorComun)
            while True:
                print('¿Este cómputo es por una libertad revocada?')
                print(Separadores._separadorComun)
                print('1 --> No. Es un cómputo común')
                print('2 --> Si es por libertad condicional revocada')
                print('3 --> Si es por libertad asistida revocada')
                print('4 --> Si es por evasión estando en salidas transitorias')
                print(Separadores._separadorComun)
                user_input = input('INDICAR OPCIÓN: ')
                if user_input == "1" or user_input == '':
                    self._EsComputoPorLCRevocada = False
                    self._EsComputoPorSTRevocada = False
                    self._EsComputoPorLARevocada = False
                    break
                if user_input == "2":
                    self._EsComputoPorLCRevocada = True
                    self._EsComputoPorSTRevocada = False
                    self._EsComputoPorLARevocada = False
                    break
                if user_input == "3":
                    self._EsComputoPorLCRevocada = False
                    self._EsComputoPorSTRevocada = False
                    self._EsComputoPorLARevocada = True
                    break
                if user_input == "4":
                    self._EsComputoPorLCRevocada = False
                    self._EsComputoPorSTRevocada = True
                    self._EsComputoPorLARevocada = False
                    break
                print('ERROR: Solo se puede responder con números del 1 al 4')

        # PREGUNTAR SI ES POR DELITOS EXCLUIDOS LEY 25.892
        if self._RegimenNormativo.LIBERTAD_CONDICIONAL(LC_KEYS._ask_delitosExcluidos25892_KEY):
            print(Separadores._separadorComun)
            while True:
                print('Delitos excluidos por la ley 25.892: ...')
                user_input = input('¿La condena es por alguno de los delitos enumerados en la ley 25.892? (S/N): ')
                if user_input == "N" or user_input == "n" or user_input == '':
                    self._EsPorDelitosExcluidosLey25892 = False
                    break
                if user_input == "S" or user_input == "s":
                    self._EsPorDelitosExcluidosLey25892 = True
                    break
                print('ERROR: Solo se puede responder con "s" o "n"')

        # PREGUNTAR SI ES POR DELITOS EXCLUIDOS LEY 25.948
        if self._RegimenNormativo.SALIDAS_TRANSITORIAS(ST_KEYS._ask_delitosExcluidos25948_KEY) or self._RegimenNormativo.LIBERTAD_ASISTIDA(LA_KEYS._ask_delitosExcluidos25948_KEY):
            print(Separadores._separadorComun)
            while True:
                print('Delitos excluidos por la ley 25.948: ...')
                user_input = input('¿La condena es por alguno de los delitos enumerados en la ley 25.948? (S/N): ')
                if user_input == "N" or user_input == "n" or user_input == '':
                    self._EsPorDelitosExcluidosLey25948 = False
                    break
                if user_input == "S" or user_input == "s":
                    self._EsPorDelitosExcluidosLey25948 = True
                    break
                print('ERROR: Solo se puede responder con "s" o "n"')

        # PREGUNTAR SI ES POR DELITOS EXCLUIDOS LEY 27.375
        if self._RegimenNormativo.LIBERTAD_CONDICIONAL(LC_KEYS._ask_delitosExcluidos27375_KEY) or self._RegimenNormativo.SALIDAS_TRANSITORIAS(ST_KEYS._ask_delitosExcluidos27375_KEY) or self._RegimenNormativo.LIBERTAD_ASISTIDA(LA_KEYS._ask_delitosExcluidos27375_KEY) or self._RegimenNormativo.REGIMEN_PREPARACION_LIBERTAD(REGPREPLIB_KEYS._ask_delitosExcluidos27375_KEY):
            print(Separadores._separadorComun)
            while True:
                print('Delitos excluidos por la ley 27.375: ...')
                user_input = input('¿La condena es por alguno de los delitos enumerados en la ley 27.375? (S/N): ')
                if user_input == "N" or user_input == "n" or user_input == '':
                    self._EsPorDelitosExcluidosLey27375 = False
                    break
                if user_input == "S" or user_input == "s":
                    self._EsPorDelitosExcluidosLey27375 = True
                    break
                print('ERROR: Solo se puede responder con "s" o "n"')

        # PREGUNTAR SI TIENE CONCEPTO BUENO DURANTE 2/3 DE LA EJECUCIÓN
        if self._RegimenNormativo.LIBERTAD_CONDICIONAL(LC_KEYS._ask_2_3ConCalifBUENO_KEY):
            print(Separadores._separadorComun)
            while True:                
                user_input = input('¿Logró alcanzar como mínimo conducta y concepto "BUENO" durante al menos 2/3 partes de la condena? (S/N): ')
                if user_input == "N" or user_input == "n" or user_input == '':
                    self._2_3ConCalifBueno = False
                    break
                if user_input == "S" or user_input == "s":
                    self._2_3ConCalifBueno = True
                    break
                print('ERROR: Solo se puede responder con "s" o "n"')

        # PREGUNTAR POR REQUISITO DE CALIFICACIÓN PARA ST
        if self._RegimenNormativo.SALIDAS_TRANSITORIAS(ST_KEYS._ask_requisitoDeCalificacion):
            print(Separadores._separadorComun)
            while True:                
                user_input = input('¿Logró alcanzar conducta "EJEMPLAR" (o el grado máximo de ser alcanzado durante el tiempo de ejecución) durante el último año de cumplimiento de pena? (S/N): ')
                if user_input == "N" or user_input == "n" or user_input == '':
                    self._RequisitoDeCalificacionDuranteElUltimoAño_ST = False
                    break
                if user_input == "S" or user_input == "s":
                    self._RequisitoDeCalificacionDuranteElUltimoAño_ST = True
                    break
                print('ERROR: Solo se puede responder con "s" o "n"')

        # PREGUNTAR SI ESTA EN PERIODO DE PRUEBA, Y DESDE CUÁNDO
        if self._RegimenNormativo.SALIDAS_TRANSITORIAS(ST_KEYS._ask_siEstaPeriodoDePruebaYDesdeCuando):
            print(Separadores._separadorComun)
            while True:                
                user_input = input('¿Logró alcanzar el periodo de prueba? (S/N): ')
                if user_input == "N" or user_input == "n" or user_input == '':
                    self._EstaEnPeriodoDePrueba = False
                    break
                if user_input == "S" or user_input == "s":
                    self._EstaEnPeriodoDePrueba = True
                    self._EstaEnPeriodoDePruebaDesde = GetConsoleInput_Fecha('¿Desde cuándo? (Ingresar fecha en formato XX/XX/XXXX: ')
                    break
                print('ERROR: Solo se puede responder con "s" o "n"')

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

def GetConsoleInput_Fecha(mensaje_para_el_usuario="Ingrese fecha en formato año-mes-día (XX/XX/XXXX): "):
    '''Hace ingresar por consola una fecha de detención en formato XX/XX/XXXX y la devuelve como un datetime.date'''
    while True:
        try:        
            fechaDeDetencionInput = input(mensaje_para_el_usuario)    
            fechaDeDetencionInput_dia = fechaDeDetencionInput[0:2]
            fechaDeDetencionInput_mes = fechaDeDetencionInput[3:5]
            fechaDeDetencionInput_año = fechaDeDetencionInput[6:10]
            if fechaDeDetencionInput[2] != "/" or fechaDeDetencionInput[5]:
                raise Exception
            fechaDeDetencionInput = datetime.date(int(fechaDeDetencionInput_año), int(fechaDeDetencionInput_mes), int(fechaDeDetencionInput_dia))        
            return fechaDeDetencionInput
        except:
            print('ERROR: Fecha en formato inválido. La fecha ingresada no tiene formato XX/XX/XXXX o no es una fecha válida.')

def GetConsoleInput_MontoDePena():
    '''Hace ingresar por consola un monto de pena temporal y la devuelve como un MontoDePena()'''
    clear = lambda: os.system('cls')
    montoDePena = MontoDePena()

    solicitar_tipo_de_pena_a_calcular = '''Indicar tipo de pena a calcular:
1 --> Pena temporal
2 --> Pena perpetua
'''
    print(solicitar_tipo_de_pena_a_calcular)
    opciones_validas = ['1', '2']
    opcion_elegida = input('Elegir opción: ')    

    while opcion_elegida not in opciones_validas:
        clear()
        print('La opción elegida no es válida. Intentar de nuevo.')
        print(solicitar_tipo_de_pena_a_calcular)
        opcion_elegida = input('Elegir opción: ')
    
    if opcion_elegida == '1': # Pena temporal
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
    
    elif opcion_elegida == '2': # Pena perpetua
        montoDePena.perpetua = True

    return montoDePena

def GetConsoleInput_OtrosTiemposDeDetencion():
    OTDD = []
    seguir_preguntando = True
    init_query = input('Ingresar tiempos de detención? (S/N): ')
    if init_query == "N" or init_query == "n":
        return "NULL"
    else:
        while seguir_preguntando:
            f_det = ''
            f_lib = ''
            f_det = GetConsoleInput_Fecha('Ingresar fecha de detención (XXXX/XX/XX): ')
            f_lib = GetConsoleInput_Fecha('Ingresar fecha de libertad (XXXX/XX/XX): ')
            este = OtraDetencion(f_det, f_lib)
            OTDD.append(este)
            seguir = input('Necesita ingresar otro tiempo de detención? (S/N): ')
            if seguir == "S" or seguir == "s":
                seguir_preguntando = True
            else:
                seguir_preguntando = False        
        return OTDD    

def RestarOtrasDetenciones(fecha_de_requisito_temporal:datetime.date, otras_detenciones:list[OtraDetencion]):
        toreturn = fecha_de_requisito_temporal
        for otra_det in otras_detenciones:            
            toreturn += relativedelta(days=-otra_det._tiempoDeDetencion.dias)
            toreturn += relativedelta(months=-otra_det._tiempoDeDetencion.meses)
            toreturn += relativedelta(years=-otra_det._tiempoDeDetencion.años)
        return toreturn

if __name__ == '__main__':
    regnorm = RegimenNormativoAplicable(datetime.date(2018, 1, 20))
    x = SituacionProcesal(regnorm)