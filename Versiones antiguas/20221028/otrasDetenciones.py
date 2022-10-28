# import datetime
# from dateutil.relativedelta import relativedelta
# from libcalc_methods import FechaAesMayorQueFechaB, TiempoEnAños_Meses_Dias, GetConsoleInput_Fecha

# class OtrasDetenciones():
#     def __init__(self, fecha_de_detencion:datetime.datetime, fecha_de_libertad:datetime.datetime, nombre:str="Sin nombre"):
#         self._nombre = nombre
#         self._detencion = fecha_de_detencion
#         self._libertad = fecha_de_libertad
#         self._tiempoDeDetencion = TiempoEnAños_Meses_Dias()
#         self._CalcularTiempoDeDetencion()
    
#     def _CalcularTiempoDeDetencion(self):
#         if FechaAesMayorQueFechaB(self._detencion, self._libertad):            
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

# if __name__ == '__main__':
#     # detencion = datetime.date(2020, 7, 30)
#     # libertad = datetime.date(2024, 9, 21)
#     # timeTest = OtroTiempoDeDetencion(detencion, libertad)

#     f_detencion = GetConsoleInput_Fecha('Fecha de detención (XXXX/XX/XX): ')
#     f_libertad = GetConsoleInput_Fecha('Fecha de libertad (XXXX/XX/XX): ')
#     calcular_lapso_temporal = OtrasDetenciones(f_detencion, f_libertad)
