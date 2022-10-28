import datetime
from dateutil.relativedelta import relativedelta

class TiempoEnAños_Meses_Dias():
    def __init__(self):
        self.años = 0
        self.meses = 0
        self.dias = 0
    
    def __str__(self):
        return '...{} año(s), {} mes(es) y {} día(s)...'.format(self.años, self.meses, self.dias)

class OtraDetencion():
    def __init__(self, fecha_de_detencion:datetime.datetime, fecha_de_libertad:datetime.datetime, nombre:str="Sin nombre"):
        self._nombre = nombre
        self._detencion = fecha_de_detencion
        self._libertad = fecha_de_libertad
        self._tiempoDeDetencion = TiempoEnAños_Meses_Dias()
        self._CalcularTiempoDeDetencion()
    
    def _CalcularTiempoDeDetencion(self):
        if FechaAesMayorQueFechaB(self._detencion, self._libertad):            
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

def FechaAesMayorQueFechaB(fecha_a:datetime.date, fecha_b:datetime.date):
    temp = fecha_a - fecha_b    
    if temp.days > 0:
        return True
    else:
        return False

def FechaAesIgualQueFechaB(fecha_a:datetime.date, fecha_b:datetime.date):
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
    montoDePena = TiempoEnAños_Meses_Dias()
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