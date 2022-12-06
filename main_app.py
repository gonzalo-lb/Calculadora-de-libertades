from libcalc import ComputoPenaTemporal
from libcalc_methods import *

def GetConsoleInput_ComputoDePena_o_CalculoDeMulta():
    '''DEVUELVE:\n
       1: Cómputo de pena temporal\n
       2: Cómputo de pena perpetua\n
       3: Cálculo de unidades fijas'''
    
    print(Separadores._separadorComun)
    while True:        
        print('1 --> Cómputo de pena temporal')
        print('2 --> Cómputo de pena perpetua')
        print('3 --> Cálculo de unidades fijas (Ley 23.737)')        
        print(Separadores._separadorComun)
        user_input = input('INDICAR OPCIÓN: ')
        if user_input == "1" or user_input == '':
            print(' - Cómputo de pena temporal')
            return 1
        if user_input == "2":
            print(' - Cómputo de pena perpetua')
            return 2
        if user_input == "3":
            print(' - Cálculo de unidades fijas')
            return 3
        print('ERROR: Solo se puede responder con números del 1 al 3')

def UnidadesFijas():
    
    print(Separadores._separadorComun)
    fechaDelHecho = GetConsoleInput_Fecha('Fecha del hecho: ')
    print(f' - Fecha ingresada: {Datetime_date_enFormatoXX_XX_XXXX(fechaDelHecho)}')
    
    print(Separadores._separadorComun)        
    multa = GetConsoleInput_Multa_Unidades_Fijas()    

    regimenNormativo = RegimenNormativoAplicable(fechaDelHecho)
    multaEnPesos = multa * regimenNormativo.UNIDADES_FIJAS(UNIDADESFIJAS_KEYS._valorDeLaUnidadFija)

    print(Separadores._separadorComun)
    print('MULTA')
    print('-----')
    print(f'Régimen de la multa: {regimenNormativo.UNIDADES_FIJAS(UNIDADESFIJAS_KEYS._denominacion_KEY)}')
    print(f'Valor de la unidad fija: ${NumeroConSeparadorDeMiles(regimenNormativo.UNIDADES_FIJAS(UNIDADESFIJAS_KEYS._valorDeLaUnidadFija))}')
    print(f'Multa: ${NumeroConSeparadorDeMiles(multaEnPesos)}')

def MainApp():

    opcion_elegida = GetConsoleInput_ComputoDePena_o_CalculoDeMulta()

    if (opcion_elegida == 1 # Cómputo de pena temporal
        or opcion_elegida == 2): # Cómputo de pena perpetua

        # SOLICITA AL USUARIO SE INDIQUE TIPO DE PENA A CALCULAR    

        if opcion_elegida == 1:
            user_input = Preguntas_Input()
        
        if opcion_elegida == 2:
            user_input = Preguntas_Input(pena_perpetua=True)
        
        computo = ComputoPenaTemporal(fechaDelHecho=user_input._fecha_del_hecho, 
        fechaDeDetencion=user_input._fecha_de_detencion,
        montoDePena=user_input._monto_de_pena,
        montoUnidadesFijas=user_input._monto_multa,
        otrasDetenciones=user_input._otras_detenciones,
        estimuloEducativo=user_input._estimulo_educativo,
        fechaInicioEjecucion=user_input._fecha_inicio_ejecucion,
        fechaCalificacionBUENO=user_input._fecha_calificacion_BUENO,
        fechaIngresoPeriodoDePrueba=user_input._fecha_ingreso_periodo_de_prueba,
        fechaCalificacionEJEMPLAR=user_input._fecha_calificacion_EJEMPLAR,
        vuelveARestarOtrasDetencionesyAplicar140enST=user_input._vuelve_a_restar_otras_detenciones_y_140_en_ST)    
    
    if opcion_elegida == 3:

        UnidadesFijas()

if __name__ == '__main__':

    MainApp()
    input()    