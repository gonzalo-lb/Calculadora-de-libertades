from libcalc_methods import *

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

if __name__ == '__main__':

    fecha_det = GetConsoleInput_Fecha(forceInput='12/2/19')
    fecha_lib = GetConsoleInput_Fecha(forceInput='2/3/21')

    x = OtraDetencion(fecha_det, fecha_lib)