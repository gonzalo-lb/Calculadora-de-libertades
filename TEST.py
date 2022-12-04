from typing import Union

def NumeroConSeparadorDeMiles(numero:Union[int, float]):
    
    if type(numero) is int:    
        return f"{numero:,}".replace(',', '.')
    
    if type(numero) is float:
        numero = f'{numero:,.2f}'.replace(',','h')
        numero = f'{numero}'.replace('.',',')
        numero = f'{numero}'.replace('h','.')
        return numero
    
    print('def NumeroConSeparadorDeMiles: WARNING: El valor ingresao no es ni float ni int. La función no va a hacer nada.')

print(NumeroConSeparadorDeMiles(25000.65))