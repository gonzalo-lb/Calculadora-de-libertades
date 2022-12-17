# **CALCULADORA DE CÓMPUTOS**

## Vencimiento de pena de ejecución condicional

> Vencimiento ("se tiene por no pronunciada"): Suma 4 años desde la fecha de la sentencia<br />
Caducidad: Suma 10 años desde la fecha de la sentencia<br />
Vencimiento del plazo de control: Suma los años/meses/días del plazo de control ingresado desde la fecha de la firmeza de la sentencia

## Vencimiento de pena temporal
> Vencimiento: A la fecha de detención se le suma el monto de pena, y luego se le restan las otras detenciones (si hay)<br/>
Caducidad: A la fecha del vencimiento de pena, suma 10 años

## Cálculo de requisito de calificación en la libertad condicional (ley 27.375)
> 1) No hay fecha de inicio de ejecución:<br/>
No hace cálculos, e indica que en esa condición no es posible determinar el requisito
> 2) Se comenzó con la ejecución de la pena pero aún no se obtuvo la calificación "BUENO":<br/>
En ese caso determina la fecha mínima para obtener el requisito, y que coincida con la fecha del requisito temporal de la LC
> 3) Se comenzó con la ejecución de pena y se obtuvo el requisito "BUENO":<br/>
En ese caso determina la fecha en la que se obtendrán los 2/3 con ese requisito.

## Cálculo de cómputo integral (ley 27.375)
> Se trata de comparar el cómputo de la libertad por LC o ST con la fecha en la que se cumplirán los requisitos temporales de calificación.<br/>
El cómputo integral es el mayor de esos dos valores.<br/>
Si falta la fecha del requisito temporal de calificación, no se puede calcular este cómputo.

## Régimen preparatorio para la liberación
> Es la fecha de vencimiento, menos un año (resta aritmética).
> No resta otras detenciones porque ya fueron restadas para calcular el vencimiento de pena.
> Realiza la aplicación del estímulo educativo.

## Cálculos generales que se realizan en todos los casos
> Siempre que se suma una fecha, al resultado final se le resta un día

## [class OtraDetencion()] Cálculo de tiempo de detención en función de la diferencia entre una fecha de libertad y una de detención. Casos:
> 1) La detención y la libertad son en el mismo mes y año:<br/>
En ese caso se aplica la diferencia entre días, y se suma un día. Ejemplos:<br/>
detención = 1/1/19; libertad = 1/1/19 --> 1 día<br/>
detención = 1/1/19; libertad = 2/1/19 --> 2 días<br/>
detención = 1/1/19; libertad = 31/1/19 --> 31 días<br/>
> 2) La detención y la libertad no son en el mismos mes o año:<br/>
1.- Primero suma de a un mes hasta igualar o superar el mes/año, y va acumulando ese resultado en otra variable.<br/>
2.- Luego, suma de a un día hasta igualar esa fecha con la fecha de libertad. Para hacer esta suma tiene en cuenta la fecha calendario (es decir, al utilizar fechas reales, el resultado varía si va de un mes a otro y ese mes tiene 28, 29, 30 o 31 días)<br/>
En este caso no se suma un día extra, ya que ese día ya se tiene en cuenta cuando se sumó el mes. Ejemplos:<br/>
detención = 1/2/19; libertad = 1/3/19 --> 1 mes<br/>
detención = 1/2/19; libertad = 2/3/19 --> 1 mes y un día<br/>
