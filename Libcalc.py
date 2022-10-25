import datetime
from dateutil.relativedelta import relativedelta

# Ingresar fecha de detención   
fechaDeDetencionInput = input('Ingresar fecha de detención en formato año-mes-día (XXXX/XX/XX): ')
fechaDeDetencionInput_año = fechaDeDetencionInput[0:4]
fechaDeDetencionInput_mes = fechaDeDetencionInput[5:7]
fechaDeDetencionInput_dia = fechaDeDetencionInput[8:10]

# Implementar código para revisar que la fecha esté bien ingresada

fechaDeDetencion = datetime.date(int(fechaDeDetencionInput_año), int(fechaDeDetencionInput_mes), int(fechaDeDetencionInput_dia))

# Ingresar monto de pena
montoDePena_años = int(input('Ingresar monto de pena (años): '))
montoDePena_meses = int(input('Ingresar monto de pena (meses): '))
montoDePena_dias = int(input('Ingresar monto de pena (días): '))

# Implementar código para revisar que las fechas estén bien ingresadas

# VENCIMIENTO DE PENA
# -------------------
vencimientoDePena = fechaDeDetencion
vencimientoDePena += relativedelta(days=montoDePena_dias)
vencimientoDePena += relativedelta(months=montoDePena_meses)
vencimientoDePena += relativedelta(years=montoDePena_años)
vencimientoDePena += relativedelta(days=-1)

# LIBERTAD CONDICIONAL
# --------------------
libertadCondicional = fechaDeDetencion

# Calcula los 2/3 de los días, lo redondea para abajo si da con coma, y los suma
LC_dias = int((montoDePena_dias * 2) / 3) # Hace los dos tercios y lo redondea para abajo
libertadCondicional +=relativedelta(days=LC_dias)

# Calcula los 2/3 de los meses
LC_meses = montoDePena_meses
LC_meses = (LC_meses * 2) / 3
dias_resto = 0
if LC_meses.is_integer() is False:
    dias_resto = LC_meses - int(LC_meses)
    LC_meses = int(LC_meses)
    if dias_resto > 0.3 and dias_resto < 0.4:
        dias_resto = int(10)
    elif dias_resto > 0.6 and dias_resto < 0.7:
        dias_resto = int(20)
    else:
        print('ERROR: Al calcular los 2/3 de los meses, los decimales no son ni 0.3333 ni 0.6666!')
    libertadCondicional +=relativedelta(days=dias_resto)
    libertadCondicional +=relativedelta(months=LC_meses)
else:
    libertadCondicional +=relativedelta(months=LC_meses)

while dias_resto >= 30:
    LC_meses += 1
    dias_resto -= 30
LC_dias += dias_resto

# 2/3 de los años
LC_años_en_meses = montoDePena_años * 12
LC_años_en_meses = (LC_años_en_meses * 2) / 3
libertadCondicional +=relativedelta(months=LC_años_en_meses)

LC_años = 0
while LC_años_en_meses >= 12:
    LC_años_en_meses -=12
    LC_años +=1
LC_meses += LC_años_en_meses
if LC_meses >= 12:
    LC_meses -=12
    LC_años +=1

libertadCondicional += relativedelta(days=-1)

# Se ajustan los resultados para que no tengan decimales
if LC_años.is_integer():    
    LC_años = int(LC_años)
if LC_meses.is_integer():
    LC_meses = int(LC_meses)
if LC_dias.is_integer():
    LC_dias = int(LC_dias)

# Imprimir resultados
print('Vencimiento de pena: {}'.format(vencimientoDePena))
print('La libertad condicional se obtiene a los {} año(s), {} mes(es) y {} día(s) de detención'.format(LC_años, LC_meses, LC_dias))
print('Libertad condicional: {}'.format(libertadCondicional))