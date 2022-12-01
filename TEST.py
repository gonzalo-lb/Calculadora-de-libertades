import datetime

def GetConsoleInput_Fecha(mensaje_para_el_usuario='Fecha: ', ENTER_devuelve_NULL=False):
    '''Hace ingresar por consola una fecha (formatos XX/XX/XXXX ó X/X/XX) y la devuelve como un datetime.date\n    
    ENTER_devuelve_NULL=True: Si no se ingresa una fecha válida, devuelve "NULL"\n
    ENTER_devuelve_NULL=False: Si se ingresa una fecha inválida, la vuelve a solicitar'''
    while True:
        seImprimioError=False
        try:
            user_input = input(mensaje_para_el_usuario)
            if len(user_input) < 6 or len(user_input) > 10:                
                if ENTER_devuelve_NULL:
                    return 'NULL'
                else:
                    print('ERROR: No se ingresó una fecha válida')
                    seImprimioError=True
                    raise Exception

            cursor = 0
            number_start = 0
            number_end = 0    
            fecha = []

            for x in range(2):
                for y in range(3):
                    if user_input[cursor] == "/":
                        number_end = cursor - 1
                        break
                    else:
                        cursor += 1
                if number_start == number_end:
                    fecha.append(int(user_input[number_start]))
                else:
                    fecha.append(int(user_input[number_start:number_end+1]))
                
                cursor += 1
                number_start = cursor
            
            # Para el año, busca desde el fondo
            number_end = cursor = len(user_input) - 1
            for y in range(5):
                if user_input[cursor] == "/":
                    number_start = cursor + 1
                    break
                else:
                    cursor -= 1
            
            # Revisa que los años tengan 2 dígitos o 4
            year_digits = len(user_input[number_start:number_end+1])
            if year_digits != 2 and year_digits != 4:
                if ENTER_devuelve_NULL:
                    return 'NULL'
                else:
                    print('ERROR: No se ingresó una fecha válida')
                    seImprimioError=True
                    raise Exception                
            
            year = int(user_input[number_start:number_end+1])

            # Si el año ingresado es de dos dígitos, lo pasa a formato de 4 dígitos
            if year_digits == 2:
                if year <= 60:
                    year += 2000
                else:
                    year += 1900

            fecha.append(year)
            return datetime.date(fecha[2], fecha[1], fecha[0])
        except:
            if ENTER_devuelve_NULL:
                return 'NULL'
            else:
                if seImprimioError == False:
                    print('ERROR: No se ingresó una fecha válida')

print(GetConsoleInput_Fecha())

    