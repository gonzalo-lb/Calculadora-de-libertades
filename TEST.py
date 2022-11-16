from dateutil.relativedelta import relativedelta
import datetime

fecha = datetime.date(2018, 5, 30)
fecha -= relativedelta(months=4)
print(fecha)