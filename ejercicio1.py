# Apartado a

def exponenciacion(a,b):

    if b == 0:
        return 1
    
    if b > 0 and (b % 2 == 0):
        return exponenciacion(a**2, b >> 1)
    elif b>0 and (b % 2 == 1):
        return a*exponenciacion(a**2, (b-1)>>1)

def exponenciacion_iterativa(s,t):

    acumulador = 1

    a,b = s,t

    while b != 0:
        if b%2 == 0:
            a,b = a**2, b>>1
        else:
            acumulador *= a 
            a,b = a**2, (b-1)>>1

    return acumulador


print(exponenciacion(256,120)==exponenciacion_iterativa(256,120))

# apartado b

# a^(-b) == (a^b)^(-1)

# apartado c

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

# print(bezout(23, 48))

def exp_mod_n(a,b,n):
    
    exp = exponenciacion(a,b)
    mcd, inverse, t1 = bezout(exp%n, n)
    
    # Si el maximo comun divisor es 1, hay solución
    if mcd == 1:
        return inverse
    else:
        raise Exception("Inverse doesn't exists")

print(exp_mod_n(256,120, 8597)+8597)