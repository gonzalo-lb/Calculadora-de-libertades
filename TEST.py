_text = []
_text.append('Linea 1')
_text.append('Linea 2')
_text.append('Linea 3')

_text1 = []
_text1.append('Nueva linea 1')
_text1.append('Nueva linea 2')

def imprimir(*loslist):
    for esteList in loslist:
        for text in esteList:
            print(text)

suma = []
suma.extend(_text)
suma.extend(_text1)


print(suma)