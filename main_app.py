from libcalc import ComputoDePena
from libcalc_methods import *

fechaDelHecho = GetConsoleInput_Fecha('Ingresar fecha del hecho en formato día/mes/año (XX/XX/XXXX): ')
fechaDeDetencionInput = GetConsoleInput_Fecha('Ingresar fecha de detención en formato día/mes/año (XX/XX/XXXX): ')
montoDePena = GetConsoleInput_MontoDePena()
otrasDetenciones = GetConsoleInput_OtrosTiemposDeDetencion()
    
computo = ComputoDePena(fechaDelHecho, fechaDeDetencionInput, montoDePena, otrasDetenciones)    
computo._ImprimirResultados()