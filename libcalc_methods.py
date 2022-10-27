# import datetime
# from dateutil.relativedelta import relativedelta
# from otrasDetenciones import OtrasDetenciones

# def FechaAesMayorQueFechaB(fecha_a:datetime.date, fecha_b:datetime.date):
#     temp = fecha_a - fecha_b    
#     if temp.days > 0:
#         return True
#     else:
#         return False

# def FechaAesIgualQueFechaB(fecha_a:datetime.date, fecha_b:datetime.date):
#     temp = fecha_a - fecha_b    
#     if temp.days == 0:
#         return True
#     else:
#         return False

# def es_multiplo(numero, multiplo):
#     return numero % multiplo == 0

# class TiempoEnAños_Meses_Dias():
#     def __init__(self):
#         self.años = 0
#         self.meses = 0
#         self.dias = 0
    
#     def __str__(self):
#         return '...{} año(s), {} mes(es) y {} día(s)...'.format(self.años, self.meses, self.dias)

# def GetConsoleInput_Fecha(mensaje_para_el_usuario="Ingrese fecha en formato año-mes-día (XXXX/XX/XX): "):
#     '''Hace ingresar por consola una fecha de detención y la devuelve como un datetime.date'''
#     fechaDeDetencionInput = input(mensaje_para_el_usuario)
#     fechaDeDetencionInput_año = fechaDeDetencionInput[0:4]
#     fechaDeDetencionInput_mes = fechaDeDetencionInput[5:7]
#     fechaDeDetencionInput_dia = fechaDeDetencionInput[8:10]
#     fechaDeDetencionInput = datetime.date(int(fechaDeDetencionInput_año), int(fechaDeDetencionInput_mes), int(fechaDeDetencionInput_dia))
#     return fechaDeDetencionInput

# def GetConsoleInput_MontoDePena():
#     '''Hace ingresar por consola un monto de pena temporal y la devuelve como un TiempoEnAños_Meses_Dias()'''
#     montoDePena = TiempoEnAños_Meses_Dias()
#     # Ingresar monto de pena    
#     try:
#         montoDePena.años = int(input('Ingresar monto de pena (años): '))
#     except:
#         montoDePena.años = 0        
#     try:
#         montoDePena.meses = int(input('Ingresar monto de pena (meses): '))        
#     except:
#         montoDePena.meses = 0        
#     try:
#         montoDePena.dias = int(input('Ingresar monto de pena (días): '))        
#     except:
#         montoDePena.dias = 0
#     return montoDePena

# def GetConsole_OtrosTiemposDeDetencion():
#     OTDD = []
#     seguir_preguntando = True
#     init_query = input('Ingresar tiempos de detención? (Y/N): ')
#     if init_query == "N" or init_query == "n":
#         return "NULL"
#     else:
#         while seguir_preguntando:
#             f_det = GetConsoleInput_Fecha('Ingresar fecha de detención (XXXX/XX/XX): ')
#             f_lib = GetConsoleInput_Fecha('Ingresar fecha de libertad (XXXX/XX/XX): ')
#             este = OtrasDetenciones(f_det, f_lib)
#             OTDD.append(este)
#             seguir = input('Necesita ingresar otro tiempo de detención? (Y/N): ')
#             if seguir == "Y" or seguir == "y":
#                 seguir_preguntando = True
#             else:
#                 seguir_preguntando = False
#         return OTDD

# if __name__ == '__main__':
#     pass