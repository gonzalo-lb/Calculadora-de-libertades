from libcalc_methods import *

if __name__ == '__main__':
    
    fechaDelHecho = GetConsoleInput_Fecha('Fecha del hecho: ')
    print(f' - Fecha ingresada: {Datetime_date_enFormatoXX_XX_XXXX(fechaDelHecho)}')
    
    print('')
    multa = GetConsoleInput_Multa_Unidades_Fijas()    

    regimenNormativo = RegimenNormativoAplicable(fechaDelHecho)
    multaEnPesos = multa * regimenNormativo.UNIDADES_FIJAS(UNIDADESFIJAS_KEYS._valorDeLaUnidadFija)

    print('')
    print('MULTA')
    print('-----')
    print(f'Régimen de la multa: {regimenNormativo.UNIDADES_FIJAS(UNIDADESFIJAS_KEYS._denominacion_KEY)}')
    print(f'Valor de la unidad fija: ${NumeroConSeparadorDeMiles(regimenNormativo.UNIDADES_FIJAS(UNIDADESFIJAS_KEYS._valorDeLaUnidadFija))}')
    print(f'Multa: ${NumeroConSeparadorDeMiles(multaEnPesos)}')