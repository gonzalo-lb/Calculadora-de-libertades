from libcalc_methods import *

if __name__ == '__main__':
    fechaDelHecho = GetConsoleInput_Fecha('Fecha del hecho: ')
    multa = GetConsoleInput_Multa_Unidades_Fijas()

    regimenNormativo = RegimenNormativoAplicable(fechaDelHecho)
    print(f'Régimen de la multa: {regimenNormativo.UNIDADES_FIJAS(UNIDADESFIJAS_KEYS._denominacion_KEY)}')
    print(f'Valor de la unidad fija: {regimenNormativo.UNIDADES_FIJAS(UNIDADESFIJAS_KEYS._valorDeLaUnidadFija)}')
    print(f'Multa: ${multa * regimenNormativo.UNIDADES_FIJAS(UNIDADESFIJAS_KEYS._valorDeLaUnidadFija)}')