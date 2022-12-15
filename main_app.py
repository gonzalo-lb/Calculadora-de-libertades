from libcalc import ComputoPenaTemporalOPerpetua, ComputPenaEjecucionCondicional, ComputPenaLibertadRevocada
from libcalc_methods import *

def GetConsoleInput_ComputoDePena_o_CalculoDeMulta():
    '''DEVUELVE:\n
       1: Cómputo de pena temporal\n
       2: Cómputo de pena perpetua\n
       3: Cómputo de pena de ejecución condicional\n
       4: Nuevo cómputo por libertad revocada\n
       5: Cálculo de unidades fijas'''
    
    print(Separadores._separadorComun)
    while True:        
        print('1 --> Cómputo de pena temporal')
        print('2 --> Cómputo de pena perpetua')
        print('3 --> Cómputo de pena de ejecución condicional')
        print('4 --> Nuevo cómputo por libertad revocada')
        print('5 --> Cálculo de unidades fijas (Ley 23.737)')        
        print(Separadores._separadorComun)
        user_input = input('INDICAR OPCIÓN: ')
        if user_input == "1":
            print(' - Cómputo de pena temporal')
            return 1
        if user_input == "2":
            print(' - Cómputo de pena perpetua')
            return 2
        if user_input == "3":
            print(' - Cómputo de pena de ejecución condicional')
            return 3
        if user_input == "4":
            print(' - Nuevo cómputo por libertad revocada')
            return 4
        if user_input == "5":
            print(' - Cálculo de unidades fijas')
            return 5
        print('ERROR: Solo se puede responder con números del 1 al 5')

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

    while True:
        opcion_elegida = GetConsoleInput_ComputoDePena_o_CalculoDeMulta()

        if (opcion_elegida == 1 # Cómputo de pena temporal
            or opcion_elegida == 2): # Cómputo de pena perpetua        

            if opcion_elegida == 1:
                user_input = Preguntas_Input_Pena_TemporalOPerpetua()
            
            if opcion_elegida == 2:
                user_input = Preguntas_Input_Pena_TemporalOPerpetua(pena_perpetua=True)
            
            computo = ComputoPenaTemporalOPerpetua(fechaDelHecho=user_input._fecha_del_hecho, 
            fechaDeDetencion=user_input._fecha_de_detencion,
            montoDePena=user_input._monto_de_pena,
            montoUnidadesFijas=user_input._monto_multa,
            otrasDetenciones=user_input._otras_detenciones,
            estimuloEducativo=user_input._estimulo_educativo,
            fechaInicioEjecucion=user_input._fecha_inicio_ejecucion,
            fechaCalificacionBUENO=user_input._fecha_calificacion_BUENO,
            fechaIngresoPeriodoDePrueba=user_input._fecha_ingreso_periodo_de_prueba,
            fechaCalificacionEJEMPLAR=user_input._fecha_calificacion_EJEMPLAR,
            vuelveARestarOtrasDetencionesyAplicar140enST=user_input._vuelve_a_restar_otras_detenciones_y_140_en_ST,
            imprimirComputoEnConsola=True)    
        
        if opcion_elegida == 3: # Cómputo de pena de ejecución condicional

            user_input = Preguntas_Input_Pena_EjecucionCondicional()

            computo = ComputPenaEjecucionCondicional(
                fechaDeSentencia=user_input._fecha_de_sentencia,
                fechaFirmezaDeSentencia=user_input._fecha_firmeza_de_sentencia,
                montoDePena=user_input._monto_de_pena,
                imprimirComputoEnConsola=True
            )
        
        if opcion_elegida == 4: # Nuevo cómputo por libertad revocada

            user_input = Preguntas_Input_NuevoComputoPorLibertadRevocada()

            computo = ComputPenaLibertadRevocada(
                fechaDelHecho=user_input._fecha_del_hecho,
                fechaEgreso=user_input._fecha_de_egreso,
                fechaNuevaDetencion=user_input._fecha_nueva_detencion,
                fechaLibertadCondicional=user_input._fecha_libertad_condicional,
                fechaSalidasTransitorias=user_input._fecha_salidas_transitorias,
                vencimientoDePena=user_input._vencimiento_de_pena,
                libertadEvadida=user_input._libertad_evadida,
                computaTiempoEnLibertad=user_input._computa_tiempo_en_libertad,
                imprimirEnConsola=True
            )

        if opcion_elegida == 5: # Cálculo de unidades fijas

            UnidadesFijas()
        
        print(Separadores._separadorComun)            
        input_otroComputo = input('¿Calcular otro cómputo? (S/N): ')        
        if input_otroComputo != "S" and input_otroComputo != "s" and input_otroComputo != "":
            break        

if __name__ == '__main__':

    MainApp()    