from libcalc_methods import *

def UnidadesFijas():
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

if __name__ == '__main__':
    
    UnidadesFijas()