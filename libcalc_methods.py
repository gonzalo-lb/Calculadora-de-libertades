import os
import datetime
import json
from dateutil.relativedelta import relativedelta
from enum_keys import LC_KEYS, ST_KEYS, LA_KEYS, REGPREPLIB_KEYS

class TiempoEnAños_Meses_Dias():
    def __init__(self, es_perpetua:bool=False, _años:int=0, _meses:int=0, _dias:int=0):
        self.perpetua = es_perpetua
        self.años = _años
        self.meses = _meses
        self.dias = _dias

        if self.perpetua:
            self.años = self.meses = self.dias = 0
    
    def __str__(self):
        if self.perpetua:
            return 'Es una pena perpetua'        
        return '...{} año(s), {} mes(es) y {} día(s)...'.format(self.años, self.meses, self.dias)

class OtraDetencion():    
    def __init__(self, fecha_de_detencion:datetime.datetime, fecha_de_libertad:datetime.datetime, nombre:str="Sin nombre"):
        self._nombre = nombre
        self._detencion = fecha_de_detencion
        self._libertad = fecha_de_libertad
        self._tiempoDeDetencion = TiempoEnAños_Meses_Dias()
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

        self._regimen_LA = 'No aplica'
        for key in self.__JSON_LC:            
            fecha_implementacion = datetime.date(self.__JSON_LC[key][LC_KEYS._fechaImplementacion_YEAR_KEY.value], self.__JSON_LC[key][LC_KEYS._fechaImplementacion_MONTH_KEY.value], self.__JSON_LC[key][LC_KEYS._fechaImplementacion_DAY_KEY.value])
            if FechaA_es_Mayor_O_Igual_Que_FechaB(_fechaDelHecho, fecha_implementacion):
                self._regimen_LA = key        

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
    
    def __str__(self):
        return '''REGIMEN LEGAL APLICABLE
-----------------------
Libertad condicional: {}
Salidas transitorias: {}
Libertad asistida: {}
Régimen preparatorio para la liberación: {}
'''.format(self._regimen_LA, self._regimen_ST, self._regimen_LA, self._regimen_PREPLIB)

class GetConsoleInput_PreguntasSobreSituacionProcesal():
    def __init__(self, _regimenNormativo:RegimenNormativoAplicable):
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

        # PREGUNTAR SI ES REINCIDENTE        
        if _regimenNormativo.LIBERTAD_CONDICIONAL(LC_KEYS._ask_esReincidente_KEY):            
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
        if _regimenNormativo.SALIDAS_TRANSITORIAS(ST_KEYS._ask_siHayAccesoria52):
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
        if _regimenNormativo.LIBERTAD_CONDICIONAL(LC_KEYS._ask_esComputoPorLCRevocada_KEY) or _regimenNormativo.LIBERTAD_ASISTIDA(LA_KEYS._ask_nuevoComputoLArevoc_KEY) or _regimenNormativo.SALIDAS_TRANSITORIAS(ST_KEYS._ask_esComputoPorEvasionDeST_KEY):
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
        if _regimenNormativo.LIBERTAD_CONDICIONAL(LC_KEYS._ask_delitosExcluidos25892_KEY):
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
        if _regimenNormativo.SALIDAS_TRANSITORIAS(ST_KEYS._ask_delitosExcluidos25948_KEY) or _regimenNormativo.LIBERTAD_ASISTIDA(LA_KEYS._ask_delitosExcluidos25948_KEY):
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
        if _regimenNormativo.LIBERTAD_CONDICIONAL(LC_KEYS._ask_delitosExcluidos27375_KEY) or _regimenNormativo.SALIDAS_TRANSITORIAS(ST_KEYS._ask_delitosExcluidos27375_KEY) or _regimenNormativo.LIBERTAD_ASISTIDA(LA_KEYS._ask_delitosExcluidos27375_KEY) or _regimenNormativo.REGIMEN_PREPARACION_LIBERTAD(REGPREPLIB_KEYS._ask_delitosExcluidos27375_KEY):
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
        if _regimenNormativo.LIBERTAD_CONDICIONAL(LC_KEYS._ask_2_3ConCalifBUENO_KEY):
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
        if _regimenNormativo.SALIDAS_TRANSITORIAS(ST_KEYS._ask_requisitoDeCalificacion):
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
        if _regimenNormativo.SALIDAS_TRANSITORIAS(ST_KEYS._ask_siEstaPeriodoDePruebaYDesdeCuando):
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
    '''Hace ingresar por consola un monto de pena temporal y la devuelve como un TiempoEnAños_Meses_Dias()'''
    clear = lambda: os.system('cls')
    montoDePena = TiempoEnAños_Meses_Dias()

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
    x = GetConsoleInput_PreguntasSobreSituacionProcesal(regnorm)