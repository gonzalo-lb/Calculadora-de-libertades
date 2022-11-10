import datetime

def GetConsoleInput_Fecha(mensaje_para_el_usuario="Ingrese fecha en formato año-mes-día (XX/XX/XXXX): "):
    '''Hace ingresar por consola una fecha de detención en formato XX/XX/XXXX y la devuelve como un datetime.date'''
    while True:
        try:        
            fechaDeDetencionInput = input(mensaje_para_el_usuario)    
            fechaDeDetencionInput_dia = fechaDeDetencionInput[0:2]
            fechaDeDetencionInput_mes = fechaDeDetencionInput[3:5]
            fechaDeDetencionInput_año = fechaDeDetencionInput[6:10]
            if fechaDeDetencionInput[2] != "/" or fechaDeDetencionInput[5]:
                raise Exception
            fechaDeDetencionInput = datetime.date(int(fechaDeDetencionInput_año), int(fechaDeDetencionInput_mes), int(fechaDeDetencionInput_dia))        
            return fechaDeDetencionInput
        except:
            print('ERROR: Fecha en formato inválido. La fecha ingresada no tiene formato XX/XX/XXXX o no es una fecha válida.')

a = GetConsoleInput_Fecha()