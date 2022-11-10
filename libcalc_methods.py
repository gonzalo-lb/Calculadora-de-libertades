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
        return self.__JSON_LC[self._regimen_LC][ask.value]
    
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
'''.format(self._regimen_LC, self._regimen_ST, self._regimen_LA, self._regimen_PREPLIB)

def Datetime_date_enFormatoXX_XX_XXXX(_date:datetime.date):
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
    fechaDeDetencionInput = input(mensaje_para_el_usuario)
    # fechaDeDetencionInput_año = fechaDeDetencionInput[0:4]
    # fechaDeDetencionInput_mes = fechaDeDetencionInput[5:7]
    # fechaDeDetencionInput_dia = fechaDeDetencionInput[8:10]
    fechaDeDetencionInput_dia = fechaDeDetencionInput[0:2]
    fechaDeDetencionInput_mes = fechaDeDetencionInput[3:5]
    fechaDeDetencionInput_año = fechaDeDetencionInput[6:10]
    fechaDeDetencionInput = datetime.date(int(fechaDeDetencionInput_año), int(fechaDeDetencionInput_mes), int(fechaDeDetencionInput_dia))
    return fechaDeDetencionInput

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
    init_query = input('Ingresar tiempos de detención? (Y/N): ')
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
            seguir = input('Necesita ingresar otro tiempo de detención? (Y/N): ')
            if seguir == "Y" or seguir == "y":
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
    pass