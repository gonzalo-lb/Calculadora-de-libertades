import os
from libcalc import ComputoDePena
from libcalc_methods import *

clear = lambda: os.system('cls')

def SolicitarPenaACalcular():
    solicitar_tipo_de_pena_a_calcular = '''
Indicar tipo de pena a calcular:
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
    
    return opcion_elegida


if __name__ == '__main__':

    # SOLICITA AL USUARIO SE INDIQUE TIPO DE PENA A CALCULAR
    
    opcion_elegida = SolicitarPenaACalcular()
    print('Opcion elegida = {}'.format(opcion_elegida))

    fechaDelHecho = GetConsoleInput_Fecha('Ingresar fecha del hecho en formato día/mes/año (XX/XX/XXXX): ')
    fechaDeDetencionInput = GetConsoleInput_Fecha('Ingresar fecha de detención en formato día/mes/año (XX/XX/XXXX): ')
    montoDePena = GetConsoleInput_MontoDePena()
    otrasDetenciones = GetConsoleInput_OtrosTiemposDeDetencion()
        
    computo = ComputoDePena(fechaDelHecho, fechaDeDetencionInput, montoDePena, otrasDetenciones)    
    computo._ImprimirResultados()