from fractions import Fraction

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


#print(exponenciacion(256,120)==exponenciacion_iterativa(256,120))

# apartado b

# a^(-b) == (a^b)^(-1)
def exp_inverse(a,b):
    return Fraction(1,exponenciacion_iterativa(a,b))

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
    f_inverse=False
    if b<0:
        b=-b
        f_inverse = True

    exp = exponenciacion_iterativa(a%n,b)
    if f_inverse:
        mcd, inverse, t1 = bezout(exp%n, n)
        
        # Si el maximo comun divisor es 1, hay solución
        if mcd == 1:
            if inverse<0:
                return inverse+n
            return inverse
        else:
            raise Exception("Inverse doesn't exists")
    
    return exp%n


def exp(a,b,n=None):
    if n:
        return exp_mod_n(a,b,n)
    if b<0:
        return exp_inverse(a,-b)
    return exponenciacion_iterativa(a,b)
        
    



#print(exp_mod_n(256,120, 8597)+8597)
assert(exp_mod_n(256,120,8597)==3696)
assert(exp_mod_n(256,-120,8597)==7748)
assert(exp(256,120,8597)==3696)
assert(exp(256,-120,8597)==7748)
assert(exp(256,120)==256**120)
assert(exp(256,-120)==Fraction(1,256**120))
