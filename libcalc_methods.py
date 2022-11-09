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

        self._regimen_LC = 'Sin determinar'
        for key in self.__JSON_LC:            
            fecha_implementacion = datetime.date(self.__JSON_LC[key][LC_KEYS._fechaImplementacion_YEAR_KEY.value], self.__JSON_LC[key][LC_KEYS._fechaImplementacion_MONTH_KEY.value], self.__JSON_LC[key][LC_KEYS._fechaImplementacion_DAY_KEY.value])
            if FechaA_es_Mayor_O_Igual_Que_FechaB(_fechaDelHecho, fecha_implementacion):
                self._regimen_LC = key        

        # DETERMINA RÉGIMEN DE SALIDAS TRANSITORIAS

        self._regimen_ST = 'Sin determinar'
        for key in self.__JSON_ST:            
            fecha_implementacion = datetime.date(self.__JSON_ST[key][ST_KEYS._fechaImplementacion_YEAR_KEY.value], self.__JSON_ST[key][ST_KEYS._fechaImplementacion_MONTH_KEY.value], self.__JSON_ST[key][ST_KEYS._fechaImplementacion_DAY_KEY.value])
            if FechaA_es_Mayor_O_Igual_Que_FechaB(_fechaDelHecho, fecha_implementacion):
                self._regimen_ST = key        

        # DETERMINA RÉGIMEN DE LIBERTAD ASISTIDA

        self._regimen_LA = 'Sin determinar'
        for key in self.__JSON_LA:            
            fecha_implementacion = datetime.date(self.__JSON_LA[key][LA_KEYS._fechaImplementacion_YEAR_KEY.value], self.__JSON_LA[key][LA_KEYS._fechaImplementacion_MONTH_KEY.value], self.__JSON_LA[key][LA_KEYS._fechaImplementacion_DAY_KEY.value])
            if FechaA_es_Mayor_O_Igual_Que_FechaB(_fechaDelHecho, fecha_implementacion):
                self._regimen_LA = key
        
        # DETERMINA RÉGIMEN DE PREPARACIÓN PARA LA LIBERTAD

        self._regimen_PREPLIB = 'Sin determinar'
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

class InformacionNormativaVIEJO():
    def __init__(self):
        
        self._libertadCondicional_ley_11179_requisito_temporal_LC = 20
        self._libertadCondicional_ley_11179_texto_art_13_CP ='''Art. 13. - El condenado a reclusión o prisión perpetua que hubiere cumplido veinte años de condena, el condenado a reclusión temporal o a prisión por más de tres años que hubiere cumplido los dos tercios de su condena y el condenado a reclusión o prisión. por menos de tres años, que por los menos hubiere cumplido un año de reclusión u ocho meses de prisión, observando con regularidad los reglamentos carcelarios, podrán obtener la libertad por resolución judicial, previo informe de la dirección del establecimiento, bajo las siguientes condiciones:

1º. Residir en el lugar que determine el auto de soltura;

2º. Observar las reglas de inspección que fije el mismo auto, especialmente la obligación de abstenerse de consumir bebidas alcohólicas;

3º. Adoptar en el plazo que el auto determine, oficio, arte, industria o profesión, si no tuviere medios propios de subsistencia;

4º. No cometer nuevos delitos;

5º. Someterse al cuidado de un patronato, indicado por las autoridades competentes;

Estas condiciones regirán hasta el vencimiento de los términos de las penas temporales y e  las que el juez podrá añadir cualquiera de las reglas de conducta contempladas en el artículo 27 bis, regirán hasta el vencimiento de los términos de las penas temporales y en las perpetuas hasta cinco años más, a contar del día de la libertad condicional.'''
        
        # La ley 25.892 se publicó en el BO 24/05/2004. No tiene fecha expresa de implementación, por lo que rigen los 8 días del CC,
        # que sería el 01/06/2004.
        self._libertadCondicional_ley_25892_fecha_vigencia = datetime.date(2004, 6, 1)
        self._libertadCondicional_ley_25892_requisito_temporal_LC = 35
        self._libertadCondicional_ley_25892_texto_art_13_CP = '''Artículo 13. El condenado a reclusión o prisión perpetua que hubiere cumplido treinta y cinco (35) años de condena, el condenado a reclusión o a prisión por más de tres (3) años que hubiere cumplido los dos tercios, y el condenado a reclusión o prisión, por tres (3) años o menos, que hubiere cumplido un (1) año de reclusión u ocho (8) meses de prisión, observando con regularidad los reglamentos carcelarios, podrán obtener la libertad por resolución judicial, previo informe de la dirección del establecimiento e informe de peritos que pronostique en forma individualizada y favorable su reinserción social, bajo las siguientes condiciones:

1º.- Residir en el lugar que determine el auto de soltura;

2º.- Observar las reglas de inspección que fije el mismo auto, especialmente la obligación de abstenerse de consumir bebidas alcohólicas o utilizar sustancias estupefacientes;

3º.- Adoptar en el plazo que el auto determine, oficio, arte, industria o profesión, si no tuviere medios propios de subsistencia;

4º.- No cometer nuevos delitos;

5º.- Someterse al cuidado de un patronato, indicado por las autoridades competentes;

6º.- Someterse a tratamiento médico, psiquiátrico o psicológico, que acrediten su necesidad y eficacia de acuerdo al consejo de peritos.

Estas condiciones, a las que el juez podrá añadir cualquiera de las reglas de conducta contempladas en el artículo 27 bis, regirán hasta el vencimiento de los términos de las penas temporales y hasta diez (10) años más en las perpetuas, a contar desde el día del otorgamiento de la libertad condicional.'''

        # La ley 27.375 se publicó en el BO 28/07/2017. No tiene fecha expresa de implementación, por lo que rigen los 8 días del CC,
        # que sería el 05/08/2017.
        self._libertadCondicional_ley_27375_fecha_vigencia = datetime.date(2017, 8, 5)
        self._libertadCondicional_ley_27375_requisito_temporal_LC = 35

class RegimenNormativoAplicableVIEJO():
    def __init__(self, fechaDelHecho:int):
        infNorm = InformacionNormativaVIEJO()
        
        self._preguntarSiEsReincidente = False
        self._preguntarSiEsComputoPorLC_Revocada = False
        self._preguntarSiSeCondenoPorDelitosExcluidos_14CP_Ley25892 = False
        self._preguntarSiSeCondenoPorDelitosExcluidos_14CP_Ley27375 = False
        self._preguntarPorCondYCocept_Bueno_paraLC_art28_Ley24660 = False

        # REGIMEN DE LIBERTAD CONDICIONAL
        self._libertadCondicional = "Ley 11.179"
        if FechaA_es_Mayor_O_Igual_Que_FechaB(fechaDelHecho, infNorm._libertadCondicional_ley_25892_fecha_vigencia):
            self._libertadCondicional = "Ley 25.892"
        if FechaA_es_Mayor_O_Igual_Que_FechaB(fechaDelHecho, infNorm._libertadCondicional_ley_27375_fecha_vigencia):
            self._libertadCondicional = "Ley 27.375"
    
    def __str__(self):
        return '''
        REGIMEN LEGAL APLICABLE AL CASO
        -------------------------------
        Régimen de libertad condicional: {}'''.format(self._libertadCondicional)

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