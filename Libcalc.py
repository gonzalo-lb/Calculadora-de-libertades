import datetime
from dateutil.relativedelta import relativedelta

def es_multiplo(numero, multiplo):
    return numero % multiplo == 0

# Dummy dates
detencion1 = {"detencion":datetime.date(2010, 3, 4), "libertad":datetime.date(2010, 3, 27)}
detencion2 = {"detencion":datetime.date(2011, 5, 7), "libertad":datetime.date(2011, 7, 2)}
detencion3 = {"detencion":datetime.date(2012, 8, 25), "libertad":datetime.date(2013, 9, 19)}

# Ingresar fecha de detención   
fechaDeDetencionInput = input('Ingresar fecha de detención en formato año-mes-día (XXXX/XX/XX): ')
fechaDeDetencionInput_año = fechaDeDetencionInput[0:4]
fechaDeDetencionInput_mes = fechaDeDetencionInput[5:7]
fechaDeDetencionInput_dia = fechaDeDetencionInput[8:10]

# Implementar código para revisar que la fecha esté bien ingresada

fechaDeDetencion = datetime.date(int(fechaDeDetencionInput_año), int(fechaDeDetencionInput_mes), int(fechaDeDetencionInput_dia))

# Ingresar monto de pena
try:
    montoDePena_años = int(input('Ingresar monto de pena (años): '))
except:
    montoDePena_años = 0
try:
    montoDePena_meses = int(input('Ingresar monto de pena (meses): '))
except:
    montoDePena_meses = 0
try:
    montoDePena_dias = int(input('Ingresar monto de pena (días): '))
except:
    montoDePena_dias = 0

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

# SALIDAS TRANSITORIAS
# --------------------
salidasTransitorias = fechaDeDetencion

# Calcula la mitad de los días lo redondea para abajo si da con coma, y los suma
ST_dias = int(montoDePena_dias / 2) # Hace la mitad y lo redondea para abajo
salidasTransitorias +=relativedelta(days=ST_dias)

# Calcula la mitad de los meses
ST_meses = montoDePena_meses
ST_dias_resto = 0
if ST_meses == 1:
    ST_meses = 0
    ST_dias_resto = int(15)
elif ST_meses > 1:
    if es_multiplo(ST_meses, 2):
        ST_meses /= 2
    else:
        ST_meses = montoDePena_meses/2
        ST_meses = int(ST_meses)        
        ST_dias_resto = int(15)

salidasTransitorias += relativedelta(months=ST_meses)
salidasTransitorias += relativedelta(days=ST_dias_resto)

# Calcula la mitad de los años
ST_años = montoDePena_años
ST_meses_resto = 0
if ST_años == 1:
    ST_años = 0
    ST_meses_resto = int(6)
elif ST_años > 1:
    if es_multiplo(ST_años, 2):
        ST_años /= 2
    else:
        ST_años /= 2
        ST_años = int(ST_años)
        ST_meses_resto = int(6)

salidasTransitorias += relativedelta(years=ST_años)
salidasTransitorias += relativedelta(months=ST_meses_resto)

salidasTransitorias += relativedelta(days=-1)

# LIBERTAD ASISTIDA
# -----------------

libertadAsistida3meses = vencimientoDePena
libertadAsistida6meses = vencimientoDePena

libertadAsistida3meses += relativedelta(months=-3)
libertadAsistida6meses += relativedelta(months=-6)

# Se ajustan los resultados para que no tengan decimales
if type(LC_años) is not int and LC_años.is_integer():
    LC_años = int(LC_años)
if type(LC_meses) is not int and LC_meses.is_integer():
    LC_meses = int(LC_meses)
if type(LC_dias) is not int and LC_dias.is_integer():
    LC_dias = int(LC_dias)

# Se ajustan los resultados para que no tengan decimales
if type(ST_años) is not int and ST_años.is_integer():
    ST_años = int(ST_años)
if type(ST_meses) is not int and ST_meses.is_integer():
    ST_meses = int(ST_meses)
if type(ST_dias) is not int and ST_dias.is_integer():
    ST_dias = int(ST_dias)

# Imprimir resultados
print('Vencimiento de pena: {}'.format(vencimientoDePena))
print('La libertad condicional se obtiene a los {} año(s), {} mes(es) y {} día(s) de detención'.format(LC_años, LC_meses, LC_dias))
print('Libertad condicional: {}'.format(libertadCondicional))
print('Las salidas transitorias se obtienen a los {} año(s), {} mes(es) y {} día(s) de detención'.format(ST_años, ST_meses + ST_meses_resto, ST_dias + ST_dias_resto))
print('Salidas transitorias: {}'.format(salidasTransitorias))
print('Libertad asistida -3 meses-: {}'.format(libertadAsistida3meses))
print('Libertad asistida -6 meses-: {}'.format(libertadAsistida6meses))