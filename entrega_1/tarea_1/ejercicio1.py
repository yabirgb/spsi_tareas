from fractions import Fraction

"""
Ejercicio 1. 

En este fichero se tienen las distintas modificaciones del algoritmo descrito y
una versión final que incluye a todas y que calcula a^b con la posibilidad de
hacer a^b mod n.
"""

# En primer lugar presentamos la versión de la función tal y como se describe

def exponenciacion(a,b):

    """
    Calcula a^b de forma recursiva
    """

    # Introducimos el caso base
    if b == 0:
        return 1
    
    # Aplicamos al recursión según la paridad de b
    if b > 0 and (b % 2 == 0):
        # Aquí utilizamos el corrimiento de bits para dividir entre 2
        return exponenciacion(a**2, b >> 1)
    elif b>0 and (b % 2 == 1):
        return a*exponenciacion(a**2, (b-1)>>1)



def exponenciacion_iterativa(s,t):

    """
    Calculamos a^b implementando el algoritmo descrito pero esta vez
    de manera iterativa. Esto lo hacemos porque python funciona peor
    al trabajar con funciones recursivas.
    """

    # Introducimos una variable acumulador que 
    # almacena el resultado que vamos a devolver
    acumulador = 1

    # creamos una copia de las variables.
    a,b = s,t

    # Traducimos la confición de parada del caso recursivo
    while b != 0:
        if b%2 == 0:
            # En lugar de hacer la llamada recursiva modificamos las variables
            # a y b
            a,b = a**2, b>>1
        else:
            # En nuestra función recursiva multiplicavamos el valor de la
            # recursión por a. En esta versión multiplicamos el acumulador por a
            # y actualizamos los valores de la iteración
            acumulador *= a 
            a,b = a**2, (b-1)>>1
    # Devolvemos a^b
    return acumulador



def exp_inverse(a,b):

    """
    Calculamos el valor de a^(-b). Nos damos cuenta de que este valor coincide
    con (a^b)^(-1) y por tanto podemos utilizar la función que ya habíamos
    definido anteriormente. Utilizamos el modulo fractions de python para
    representar el número que se obtiene.
    """

    return Fraction(1,exponenciacion_iterativa(a,b))


"""
Definimos ahora el algoritmo de euclides extendido que utilizamos para calcular
los coeficientes de Bezout. Esto nos hará falta cuando queramos calcular la potencia
(a^(-b)) mod n
"""

def bezout(a, b):
    # Hacemos que a sea el mayor de los dos numeros
    flag = a<b
    if flag:
        a,b = b,a

    r1,r2 = a,b
    s1,s2 = 1,0
    t1,t2 = 0,1

    while r2 > 0:
        q,r = divmod(r1,r2)
        r1,r2 = r2,r
        s1,s2 = s2,s1 - q * s2
        t1,t2 = t2,t1 - q * t2

    if flag:
        return r1,t1,s1
    else:
        return r1,s1,t1

def exp_mod_n(a,b,n):

    """
    Función para calcular el valor de [(a^b) mod n] con n >= 0 entero.
    """

    # Nuestro objetivo va aser calcular (a^abs(b)) y si b es negativo tomaremos
    # la precaución de calcular el inverso de (a^b) mod n
    
    # Si b es negativo lo hacemos positivo y advertimos de que b era negativo
    f_inverse=False
    if b<0:
        b=-b
        f_inverse = True

    # Calculamos a^b. Aqui tenemos la precaucion de hacer a%n antes de operar.
    exp = exponenciacion_iterativa(a%n,b)

    # Si tenemos que calcular el inverso
    if f_inverse:
        # Calculamos los coeficientes de bezout siendo el primero que devolvemos
        # el inverso de exp
        mcd, inverse, t1 = bezout(exp%n, n)
        
        # Si el maximo comun divisor es 1, hay solución
        if mcd == 1:
            # Si el inverso es negativo mod n lo potemos positivo
            if inverse<0:
                return inverse+n
            return inverse
        else:
            # En otro caso levantamos una excepcion indicando que no existe solucion
            raise Exception("Inverse doesn't exists")
    
    return exp%n


def exp(a,b,n=None):

    """
    Función para calcular [a^b mod n] o [a^b]
    """

    # Si n no es None es que queremos calcular exp mod n
    if n:
        # usamos la funcion definida
        return exp_mod_n(a,b,n)
    if b<0:
        # Si b es negativo calculamos el inverso de a^b
        return exp_inverse(a,-b)
    # En otro caso podemos calcular a^b de manera directa
    return exponenciacion_iterativa(a,b)
        
    


# Algunas pruebas. Si todo funciona bien al ejecutar este script no debería producirse ningun fallo

if __name__ == '__main__':
    assert(exp_mod_n(256,120,8597)==3696)
    assert(exp_mod_n(256,-120,8597)==7748)
    assert(exp(256,120,8597)==3696)
    assert(exp(256,-120,8597)==7748)
    assert(exp(256,120)==256**120)
    assert(exp(256,-120)==Fraction(1,256**120))
