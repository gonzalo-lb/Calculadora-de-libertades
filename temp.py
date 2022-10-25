import datetime
from dateutil.relativedelta import relativedelta

# Dummy dates
detencion1 = {"detencion":datetime.date(2010, 3, 4), "libertad":datetime.date(2010, 3, 27)}
detencion2 = {"detencion":datetime.date(2011, 5, 7), "libertad":datetime.date(2011, 7, 2)}
detencion3 = {"detencion":datetime.date(2012, 8, 25), "libertad":datetime.date(2013, 9, 19)}


detencion = datetime.date(2020, 7, 21)
libertad = datetime.date(2022, 7, 23)

print(libertad - detencion)
print(detencion - libertad)
x= detencion.day
y= detencion.month
z= detencion.year
print(type(x))
print(type(y))
print(type(z))
