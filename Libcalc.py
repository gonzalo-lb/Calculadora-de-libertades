import datetime
from dateutil.relativedelta import relativedelta
# from libcalc_methods import es_multiplo, TiempoEnAños_Meses_Dias, GetConsoleInput_Fecha, GetConsoleInput_MontoDePena, GetConsole_OtrosTiemposDeDetencion

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

class TiempoEnAños_Meses_Dias():
    def __init__(self):
        self.años = 0
        self.meses = 0
        self.dias = 0
    
    def __str__(self):
        return '...{} año(s), {} mes(es) y {} día(s)...'.format(self.años, self.meses, self.dias)

def GetConsoleInput_Fecha(mensaje_para_el_usuario="Ingrese fecha en formato año-mes-día (XXXX/XX/XX): "):
    '''Hace ingresar por consola una fecha de detención y la devuelve como un datetime.date'''
    fechaDeDetencionInput = input(mensaje_para_el_usuario)
    fechaDeDetencionInput_año = fechaDeDetencionInput[0:4]
    fechaDeDetencionInput_mes = fechaDeDetencionInput[5:7]
    fechaDeDetencionInput_dia = fechaDeDetencionInput[8:10]
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

def GetConsole_OtrosTiemposDeDetencion():
    OTDD = []
    seguir_preguntando = True
    init_query = input('Ingresar tiempos de detención? (Y/N): ')
    if init_query == "N" or init_query == "n":
        return "NULL"
    else:
        while seguir_preguntando:
            f_det = GetConsoleInput_Fecha('Ingresar fecha de detención (XXXX/XX/XX): ')
            f_lib = GetConsoleInput_Fecha('Ingresar fecha de libertad (XXXX/XX/XX): ')
            este = OtrasDetenciones(f_det, f_lib)
            OTDD.append(este)
            seguir = input('Necesita ingresar otro tiempo de detención? (Y/N): ')
            if seguir == "Y" or seguir == "y":
                seguir_preguntando = True
            else:
                seguir_preguntando = False
        return OTDD

class OtrasDetenciones():
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

def RestarOtrasDetenciones(fecha_de_requisito_temporal:datetime.date, otras_detenciones:list[OtrasDetenciones]):
        toreturn = fecha_de_requisito_temporal
        for otra_det in otras_detenciones:
            toreturn += relativedelta(days=-otra_det._tiempoDeDetencion.dias)
            toreturn += relativedelta(days=-otra_det._tiempoDeDetencion.meses)
            toreturn += relativedelta(days=-otra_det._tiempoDeDetencion.años)
        return toreturn 

class ComputoDePena():
    
    def __init__(self, fechaDeDetencion:datetime.date, montoDePena:TiempoEnAños_Meses_Dias, otrosTiemposDeDetencion='NULL'):
        self._fecha_de_detencion = fechaDeDetencion
        self._monto_de_pena = montoDePena
        self._vencimiento_de_pena = datetime.date
        self._vencimiento_de_pena_sinRestarOtrasDetenciones = datetime.date
        self._otros_tiempos_de_detencion = otrosTiemposDeDetencion
        self._computo_libertad_condicional = datetime.date
        self._computo_libertad_condicional_sinRestarOtrasDetenciones = datetime.date
        self._requisito_libertad_condicional = TiempoEnAños_Meses_Dias()
        self._computo_salidas_transitorias = datetime.date
        self._computo_salidas_transitorias_sinRestarOtrasDetenciones = datetime.date
        self._requisito_salidas_transitorias = TiempoEnAños_Meses_Dias()
        self._computo_libertad_asistida_3meses = datetime.date
        self._computo_libertad_asistida_3meses_sinRestarOtrasDetenciones = datetime.date
        self._requisito_libertad_asistida_3meses = TiempoEnAños_Meses_Dias()
        self._computo_libertad_asistida_6meses = datetime.date
        self._computo_libertad_asistida_6meses_sinRestarOtrasDetenciones = datetime.date
        self._requisito_libertad_asistida_6meses = TiempoEnAños_Meses_Dias()        

        # Luego tiene que hacer todos los cálculos
        self.__CalcularVencimientoDePena()
        self.__CalcularLibertadCondicional()
        self.__CalcularSalidasTransitorias()
        self.__CalcularLibertadAsistida_3meses()
        self.__CalcularLibertadAsistida_6meses()
        print(otrosTiemposDeDetencion)
        print(type(otrosTiemposDeDetencion))

    def __CalcularVencimientoDePena(self):

        self._vencimiento_de_pena = datetime.date
        self._vencimiento_de_pena = self._fecha_de_detencion        
        self._vencimiento_de_pena += relativedelta(days=self._monto_de_pena.dias)
        self._vencimiento_de_pena += relativedelta(months=self._monto_de_pena.meses)
        self._vencimiento_de_pena += relativedelta(years=self._monto_de_pena.años)
        self._vencimiento_de_pena += relativedelta(days=-1)
        self._vencimiento_de_pena_sinRestarOtrasDetenciones = self._vencimiento_de_pena
        if self._otros_tiempos_de_detencion != "NULL":
            self._vencimiento_de_pena = RestarOtrasDetenciones(self._vencimiento_de_pena, self._otros_tiempos_de_detencion)
    
    def __CalcularLibertadCondicional(self):

        self._computo_libertad_condicional = self._fecha_de_detencion

        if self._monto_de_pena.años < 3 or (self._monto_de_pena.años == 3 and self._monto_de_pena.meses == 0 and self._monto_de_pena.dias == 0):
            self._requisito_libertad_condicional.años = 0
            self._requisito_libertad_condicional.meses = 8
            self._requisito_libertad_condicional.dias = 0
            self._fecha_de_detencion += relativedelta(months=8)
        else:
            # Calcula los 2/3 de los días, lo redondea para abajo si da con coma, y los suma
            self._requisito_libertad_condicional.dias = int((self._monto_de_pena.dias * 2) / 3) # Hace los dos tercios y lo redondea para abajo
            self._computo_libertad_condicional +=relativedelta(days=self._requisito_libertad_condicional.dias)

            # Calcula los 2/3 de los meses
            self._requisito_libertad_condicional.meses = self._monto_de_pena.meses
            self._requisito_libertad_condicional.meses = (self._requisito_libertad_condicional.meses * 2) / 3
            dias_resto = 0
            if self._requisito_libertad_condicional.meses.is_integer() is False:
                dias_resto = self._requisito_libertad_condicional.meses - int(self._requisito_libertad_condicional.meses)
                self._requisito_libertad_condicional.meses = int(self._requisito_libertad_condicional.meses)
                if dias_resto > 0.3 and dias_resto < 0.4:
                    dias_resto = int(10)
                elif dias_resto > 0.6 and dias_resto < 0.7:
                    dias_resto = int(20)
                else:
                    print('ERROR: Al calcular los 2/3 de los meses, los decimales no son ni 0.3333 ni 0.6666!')
                self._computo_libertad_condicional +=relativedelta(days=dias_resto)
                self._computo_libertad_condicional +=relativedelta(months=self._requisito_libertad_condicional.meses)
            else:
                self._computo_libertad_condicional +=relativedelta(months=self._requisito_libertad_condicional.meses)

            while dias_resto >= 30:
                self._requisito_libertad_condicional.meses += 1
                dias_resto -= 30
            self._requisito_libertad_condicional.dias += dias_resto

            # 2/3 de los años
            LC_años_en_meses = self._monto_de_pena.años * 12
            LC_años_en_meses = (LC_años_en_meses * 2) / 3
            self._computo_libertad_condicional +=relativedelta(months=LC_años_en_meses)

            self._requisito_libertad_condicional.años = 0
            while LC_años_en_meses >= 12:
                LC_años_en_meses -=12
                self._requisito_libertad_condicional.años +=1
            self._requisito_libertad_condicional.meses += LC_años_en_meses
            if self._requisito_libertad_condicional.meses >= 12:
                self._requisito_libertad_condicional.meses -=12
                self._requisito_libertad_condicional.años +=1
            
            if type(self._requisito_libertad_condicional.años) is not int and self._requisito_libertad_condicional.años.is_integer():
                self._requisito_libertad_condicional.años = int(self._requisito_libertad_condicional.años)
            if type(self._requisito_libertad_condicional.meses) is not int and self._requisito_libertad_condicional.meses.is_integer():
                self._requisito_libertad_condicional.meses = int(self._requisito_libertad_condicional.meses)
            if type(self._requisito_libertad_condicional.dias) is not int and self._requisito_libertad_condicional.dias.is_integer():
                self._requisito_libertad_condicional.dias = int(self._requisito_libertad_condicional.dias)

            self._computo_libertad_condicional += relativedelta(days=-1)

            self._computo_libertad_condicional_sinRestarOtrasDetenciones = self._computo_libertad_condicional            
            if self._otros_tiempos_de_detencion != "NULL":
                self._computo_libertad_condicional = RestarOtrasDetenciones(self._computo_libertad_condicional, self._otros_tiempos_de_detencion)

    def __CalcularSalidasTransitorias(self):
        self._computo_salidas_transitorias = self._fecha_de_detencion        

        # Calcula la mitad de los días lo redondea para abajo si da con coma, y los suma
        self._requisito_salidas_transitorias.dias = int(self._monto_de_pena.dias / 2) # Hace la mitad y lo redondea para abajo
        self._computo_salidas_transitorias +=relativedelta(days=self._requisito_salidas_transitorias.dias)

        # Calcula la mitad de los meses
        self._requisito_salidas_transitorias.meses = self._monto_de_pena.meses
        ST_dias_resto = 0
        if self._requisito_salidas_transitorias.meses == 1:
            self._requisito_salidas_transitorias.meses = 0
            ST_dias_resto = int(15)
        elif self._requisito_salidas_transitorias.meses > 1:
            if es_multiplo(self._requisito_salidas_transitorias.meses, 2):
                self._requisito_salidas_transitorias.meses /= 2
            else:
                self._requisito_salidas_transitorias.meses = self._monto_de_pena.meses/2
                self._requisito_salidas_transitorias.meses = int(self._requisito_salidas_transitorias.meses)        
                ST_dias_resto = int(15)

        self._computo_salidas_transitorias += relativedelta(months=self._requisito_salidas_transitorias.meses)
        self._computo_salidas_transitorias += relativedelta(days=ST_dias_resto)

        # Calcula la mitad de los años
        self._requisito_salidas_transitorias.años = self._monto_de_pena.años
        ST_meses_resto = 0
        if self._requisito_salidas_transitorias.años == 1:
            self._requisito_salidas_transitorias.años = 0
            ST_meses_resto = int(6)
        elif self._requisito_salidas_transitorias.años > 1:
            if es_multiplo(self._requisito_salidas_transitorias.años, 2):
                self._requisito_salidas_transitorias.años /= 2
            else:
                self._requisito_salidas_transitorias.años /= 2
                self._requisito_salidas_transitorias.años = int(self._requisito_salidas_transitorias.años)
                ST_meses_resto = int(6)

        self._computo_salidas_transitorias += relativedelta(years=self._requisito_salidas_transitorias.años)
        self._computo_salidas_transitorias += relativedelta(months=ST_meses_resto)

        self._computo_salidas_transitorias += relativedelta(days=-1)

        # Resta las otras detenciones, si hay
        self._computo_salidas_transitorias_sinRestarOtrasDetenciones = self._computo_salidas_transitorias
        if self._otros_tiempos_de_detencion != "NULL":
            self._computo_salidas_transitorias = RestarOtrasDetenciones(self._computo_salidas_transitorias, self._otros_tiempos_de_detencion)

        # Se ajustan los resultados para que no tengan decimales
        if type(self._requisito_salidas_transitorias.años) is not int and self._requisito_salidas_transitorias.años.is_integer():
            self._requisito_salidas_transitorias.años = int(self._requisito_salidas_transitorias.años)
        if type(self._requisito_salidas_transitorias.meses) is not int and self._requisito_salidas_transitorias.meses.is_integer():
            self._requisito_salidas_transitorias.meses = int(self._requisito_salidas_transitorias.meses)
        if type(self._requisito_salidas_transitorias.dias) is not int and self._requisito_salidas_transitorias.dias.is_integer():
            self._requisito_salidas_transitorias.dias = int(self._requisito_salidas_transitorias.dias)

    def __CalcularLibertadAsistida_3meses(self):
        
        self._computo_libertad_asistida_3meses = self._vencimiento_de_pena
        self._computo_libertad_asistida_3meses += relativedelta(months=-3)

        self._computo_libertad_asistida_3meses_sinRestarOtrasDetenciones = self._computo_libertad_asistida_3meses
        if self._otros_tiempos_de_detencion != "NULL":
            self._computo_libertad_asistida_3meses = RestarOtrasDetenciones(self._computo_libertad_asistida_3meses, self._otros_tiempos_de_detencion)
        
    def __CalcularLibertadAsistida_6meses(self):
        self._computo_libertad_asistida_6meses = self._vencimiento_de_pena
        self._computo_libertad_asistida_6meses += relativedelta(months=-6)

        self._computo_libertad_asistida_6meses_sinRestarOtrasDetenciones = self._computo_libertad_asistida_6meses
        if self._otros_tiempos_de_detencion != "NULL":
            self._computo_libertad_asistida_6meses = RestarOtrasDetenciones(self._computo_libertad_asistida_6meses, self._otros_tiempos_de_detencion)

    def _ImprimirResultados(self):
        resultadosFinales = '''
Cómputo de pena
---------------
Vencimiento de pena: {}
La libertad condicional se obtiene a los {} año(s), {} mes(es) y {} día(s) de detención.
Libertad condicional: {}
Las salidas transitorias se obtienen a los {} año(s), {} mes(es) y {} día(s) de detención.
Salidas transitorias: {}
Libertad asistida -3 meses-: {}
Libertad asistida -6 meses-: {}
'''.format(self._vencimiento_de_pena,
        self._requisito_libertad_condicional.años, self._requisito_libertad_condicional.meses, self._requisito_libertad_condicional.dias,
        self._computo_libertad_condicional,
        self._requisito_salidas_transitorias.años, self._requisito_salidas_transitorias.meses, self._requisito_salidas_transitorias.dias,
        self._computo_salidas_transitorias,
        self._computo_libertad_asistida_3meses,
        self._computo_libertad_asistida_6meses)

        resultadosSinRestarOtrasDetenciones = '''
Resultados sin restar otras detenciones
---------------------------------------
Vencimiento de pena: {}
Libertad condicional: {}
Salidas transitorias: {}
Libertad asistida -3 meses-: {}
Libertad asistida -6 meses-: {}
'''.format(self._vencimiento_de_pena_sinRestarOtrasDetenciones,        
        self._computo_libertad_condicional_sinRestarOtrasDetenciones,        
        self._computo_salidas_transitorias_sinRestarOtrasDetenciones,
        self._computo_libertad_asistida_3meses_sinRestarOtrasDetenciones,
        self._computo_libertad_asistida_6meses_sinRestarOtrasDetenciones)

        print(resultadosFinales)
        print(resultadosSinRestarOtrasDetenciones)

def _DEBUG():    
    
    fechaDeDetencionInput = GetConsoleInput_Fecha('Ingresar fecha de detención en formato año-mes-día (XXXX/XX/XX): ')
    montoDePena = GetConsoleInput_MontoDePena()
    otrasDetenciones = GetConsole_OtrosTiemposDeDetencion()
    
    computo = ComputoDePena(fechaDeDetencionInput, montoDePena, otrasDetenciones)    
    computo._ImprimirResultados()    

if __name__ == '__main__':
    _DEBUG()