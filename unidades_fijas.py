from libcalc_methods import *

with open('Regimenes/unidadesFijas.json', encoding='utf-8') as reg_unidadesFijas:
    JSON_UNIDADESFIJAS = json.load(reg_unidadesFijas)            

fechaDelHecho = GetConsoleInput_Fecha('Fecha del hecho: ')

regimenNormativo = RegimenNormativoAplicable(fechaDelHecho)
regimenNormativo._Imprimir()