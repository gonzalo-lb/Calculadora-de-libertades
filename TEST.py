import datetime

def GetConsoleInput_Fecha():    
    user_input = input('Fecha: ')
    if len(user_input) < 6 or len(user_input) > 10:
        print('ERROR: No se ingresó una fecha válida')
        return

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
        print('ERROR: No se ingresó una fecha válida')
        return
    
    year = int(user_input[number_start:number_end+1])

    # Si el año ingresado es de dos dígitos, lo pasa a formato de 4 dígitos
    if year_digits == 2:
        if year <= 60:
            year += 2000
        else:
            year += 1900

    fecha.append(year)

    print(fecha)


GetConsoleInput_Fecha()
a = '1/1/22'
b = '01/01/2022'

print(len(a))
print(len(b))

    