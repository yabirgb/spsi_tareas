"""
Kasiski method

Laura Sanchez Parra
Yabir Garcia Benchakhtir
"""

from typing import List, Dict
from math import sqrt, gcd, inf
from collections import defaultdict, Counter
from ejercicio2 import Vigenere
import string

class Cracker:

    """
    Ataque al cifrado de vigenere.

    La clase toma dos cadenas de texto como argumento:

    - alph: Alfabeto que se quiere usar
    - p: Vector de numeros con las probabilidades en el lenguaje de cada simbolo del alfabeto
    - kp: Valor del lenguaje para IC,
    - r: radio de numeros para buscar en friedman
    - minc: Longitud minima para buscar coincidencias en kasiski
    - maxc: Longitud maxima para buscar coincidencias en kasiski
    Se exponen los siguientes metodos

    attack(text): Intenta obtener el texto cifrado correspondiente a text
    """

    def __init__(self, alph, p, kp, r = 4, minc=3, maxc=6):
        self.alph = alph 
        self.p = p
        self.kp = kp
        self.r = r

        self.MIN_COUNT = minc
        self.MAX_COUNT = maxc


    def _get_distance(self, substring, offset, substring_map, distances):
        """
        Encuentra la distancia entre una cadena de texto y la ultima vez que aparecio
        """
        if substring in substring_map:
            last_offset = substring_map.get(substring)
            distances.add(offset-last_offset)
        else:
            substring_map[substring] = offset

    def _find_repeated_substrings(self, text:str, substring_map:Dict[str, int], distances:set):
        
        """
        Dado un texto busca las cadenas que se reptien. Busca por cadenas que se
        repitan con una longitud minima de MIN_COUNT y una longitud maxima de
        MAX_COUNT. 

        Para buscar las ocurrencias realizamos un desplazamiento que empieza en
        0 y se mueve una posicion en cada iteracion y buscamos por repeticiones
        de las distintas posiciones posibles.
        """

        count, offset = self.MIN_COUNT, 0

        while (offset + count < len(text)):
            while (offset + count < len(text) and self.MAX_COUNT >= count):
                substring = text[offset:offset+count]
                self._get_distance(substring, offset, substring_map, distances)
                count +=1

            offset += 1
            count = self.MIN_COUNT

    def _gcd_distance(self,distances):
        """
        Calcula el maximo comun divisor de una lista de numeros
        """
        dst=list(distances)
        g=dst[0]
        for i in dst[1:]:
            prev = g
            g=gcd(g,i)
            if g == 1:
                g=prev
        return g

    def _count_distance_divisors(self, distance:int):
        """
        Funcion para extraer los divisores de un numero.
        Buscamos los divisores hasta la raiz
        """

        divisors=defaultdict(int)
        divisors[distance] =1
        div = 2
        while div < int(sqrt(distance)):

            if distance % div == 0:
                divisors[div] += 1
                divisors[distance//div] += 1
                distance = distance // div 
            else:
                div += 1
    
        return divisors

    def _extract_frequencies(self, s:str):
        """
        Calcular la frecuencia de cada caracter del alfabeto 
        en el texto
        """
        # Obtenemos el numero de veces que aparece cada caracter en el texto
        n_app=Counter(s)
        # Lista que vamos a devolver con las frecuencias
        freq=[]
        # Para cada caracter del alfabeto comprobamos si esta o no en el texto.
        # Si esta su frecuencia es el numero de veces que aparece entre el
        # numero de caracteres del texto. Si no esta, su frecuencia es 0
        for char in self.alph:
            n=n_app.get(char)
            if n:
                freq.append(n/len(s))
            else:
                freq.append(0)
        return freq   

    def _extract_occurencies(self, s):
        n_app=Counter(s)
        occ = []
        for char in self.alph:
            n = n_app.get(char)
            if n:
                occ.append(n)
            else:
                occ.append(0)

        return occ

    def MIC(self, s:str):
        # Funcion MIC tal y como se define en el articulo
        s_freq = self._extract_frequencies(s)
        return sum(map(lambda x:x[0]*x[1],zip(self.p,s_freq)))/len(s)

    def _shift_by_n(self, s:str, n:int):
        # Desplaza los caracteres de una cadena de texto por una cantidad fija
        return "".join([self.alph[(self.alph.index(char)+n)%len(self.alph)] for char in s])

    def compute_most_probable(self, s:str):
        mic=[]
        # usamos la funcion MIC para calcular cuanto se parecen las
        # distribuciones del lenguaje a las que aparecen en la cadena de texto
        # estudiada. Para ello rotamos la cadena s_i todas las cantidades
        # posibles y guardamos el valor obtenido
        for i in range(len(self.alph)):
            mic.append(self.MIC(self._shift_by_n(s,i)))
        
        # Obtenemos el mayor valor obtenido para la funcion MIC. Los valores
        # estan ordenados en funcion de su posicion asi que usamos la funcion
        # enumerate para obtener las posiciones, elegimos el maximo por valor de
        # la funcion y nos quedamos con su posicion que corresponde con la cantidad desplazada
        candidate=max(enumerate(mic), key=lambda x: x[1])[0]

        # Devolvemos como se deice en el articulo el candidado a desplazamiento
        return (len(self.alph)-candidate)%len(self.alph)

    def kasiski(self, intxt):
        substrings = dict()
        divisors = defaultdict(int)
        distances = set()
        self._find_repeated_substrings(intxt, substrings, distances)
        distance=self._gcd_distance(distances)
        return self._count_distance_divisors(distance)

    def _split_n_chars(self, msg, k):
        # En s_i almacenamos las cadenas de caracteres que aparecen cada i
        # posiciones en el texto de partida
        s_i=[[]for i in range(k)]
        pos=0
        for c in msg:
            s_i[pos].append(c)
            pos+=1
            if pos==k:
                pos=0
        # Los caracacteres estan almacenados como una lista y los queremos como
        # una cadena de texto
        for i,lst in enumerate(s_i):
            s_i[i]="".join(lst)

        return s_i 

    def cracker(self, msg, k):
        # En s_i almacenamos las cadenas de caracteres que aparecen cada i
        # posiciones en el texto de partida
        s_i=self._split_n_chars(msg, k)

        # Ahora obtenemos las claves que se consideran posibles
        keys=[]
        for lst in s_i:
            keys.append(self.compute_most_probable(lst))

        # La clave la hemos obtenido como una cadena de posiciones. Traducimos
        # dichas posiciones a una clave de caracteres del alfabeto
        return "".join([self.alph[i] for i in keys]) 

    def _break_code(self, intxt, method="kasiski"):
        """
        En funcion del metodo que se elija obtenemos una lista de longitudes
        candidatas y a continuacion usamos  el test del articulo para buscar la clave
        """
        
        keys = []

        # Elegimos le metodo correcto
        alg = self.kasiski
        if method == "friedman":
            alg = self.friedman_analysis

        # Obtenemos las posibles longitudes para la clave
        possibilities = alg(intxt)

        # friedman solo devuelve una longitud asi que para que el codigo valga
        # para ambos codigos lo englobamos en una lista
        if type(possibilities) == int:
            possibilities = [possibilities]

        for length in possibilities:
            keys.append(self.cracker(intxt, length))

        return keys


    def _friedman_formula(self, k0):
        kr = 1/len(self.alph)

        return (self.kp-kr)/(k0-kr)

    def _friedman_IC(self, text):
        """
        Calcular el valor de k0 utilizado en el test de friedman
        """
        freq = self._extract_occurencies(text)
        return sum([f*(f-1) for f in freq])/len(text)/(len(text)-1)

    def friedman_analysis(self, text):
        """
        Metodo para obtener una aproximancion de la longitud de la clave
        usando el test de friedman
        """

        r = self.r

        # calculamos ic para el texto original
        k0 = self._friedman_IC(text)
        estimation = self._friedman_formula(k0)
        #print(k0, estimation)
        # Buscamos el valor que mas se aproxime a 1
        averages = []

        # En un radio de la primera aproxumacion encontrada
        print(f"Friedman: Obtenemos como punto central {estimation}. Buscamos en [{int(round(estimation))-r}, {int(round(estimation))+r}]")
        for l in range(int(round(estimation))-r, int(round(estimation))+r+1):
            s_i = self._split_n_chars(text, l)
            ic = [self._friedman_formula(self._friedman_IC(s)) for s in s_i]

            # calculamos la media de las columnas
            averages.append(sum(ic)/len(ic))

            #print(l, "-", value)
        # Buscamos el valor mas proximo a uno, para ello calculamos la distancia 
        # y tomamos la posicion

        # En esta linea tomamos la media que mas se aproxime a 1. Para ello
        # aplicamos la funcion distancia a 1 al conjunto de medias, las
        # numeramos, buscamos el minimo en funcion de la distancia y nos
        # quedamos la posicion. Finalmente esto nos da una posicion entre 0 y el
        # diametro del radio de busqueda, para encontrar la longitud de clave a
        # la que se corresponde sumamos el menor elemento del intervalo de
        # busqueda int(round(estimation))-r
        return min(enumerate(map(lambda x: abs(1-x), averages)), key=lambda x: x[1])[0] + int(round(estimation))-r

    def attack_kasiski(self, intxt):
        # ataque al cifrado de vigenere

        # Para cada clave candidata obtenida usamos la clase vigenre
        # para descifrar usando dicha clave e imprimos el texto obtenido
        for key in self._break_code(intxt):
            V = Vigenere(self.alph, self.cracker(intxt,len(key)))
            print(f"Llave con longitud {len(key)}: {key}")
            print("Texto: ")
            print(V.decipher(intxt))

    def attack_friedman(self, intxt):
        # ataque al cifrado de vigenere

        # Para cada clave candidata obtenida usamos la clase vigenre
        # para descifrar usando dicha clave e imprimos el texto obtenido
        for key in self._break_code(intxt, method = "friedman"):
            V = Vigenere(self.alph, self.cracker(intxt,len(key)))
            print(f"Llave con longitud {len(key)}: {key}")
            print("Texto: ")
            print(V.decipher(intxt))


p = [0.1253, 0.014199999999999999, 0.046799999999999994, 0.058600000000000006, 
        0.1368, 0.0069, 0.0101, 0.006999999999999999, 0.0625, 0.0044, 0.0002, 
        0.049699999999999994, 0.0315, 0.06709999999999999, 0.0868, 0.025099999999999997, 
        0.0088, 0.0687, 0.07980000000000001, 0.0463, 0.0393, 0.009000000000000001, 0.0001, 
        0.0022, 0.009000000000000001, 0.0052]

kp_en = 0.067
kp_es = 0.071851

intxt = """UECWKDVLOTTVACKTPVGEZQMDAMRNPDDUXLBUICAMRHOECBHSPQLVIWOFFEAILPNTESMLDRUURIFAEQTTPXADWIAWLACCRPBHSRZIVQWOFROGTTNNXEVIVIBPDTTGAHVIACLAYKGJIEQHGECMESNNOCTHSGGNVWTQHKBPRHMVUOYWLIAFIRIGDBOEBQLIGWARQHNLOISQKEPEIDVXXNETPAXNZGDXWWEYQCTIGONNGJVHSQGEATHSYGSDVVOAQCXLHSPQMDMETRTMDUXTEQQJMFAEEAAIMEZREGIMUECICBXRVQRSMENNWTXTNSRNBPZHMRVRDYNECGSPMEAVTENXKEQKCTTHSPCMQQHSQGTXMFPBGLWQZRBOEIZHQHGRTOBSGTATTZRNFOSMLEDWESIWDRNAPBFOFHEGIXLFVOGUZLNUSRCRAZGZRTTAYFEHKHMCQNTZLENPUCKBAYCICUBNRPCXIWEYCSIMFPRUTPLXSYCBGCCUYCQJMWIEKGTUBRHVATTLEKVACBXQHGPDZEANNTJZTDRNSDTFEVPDXKTMVNAIQMUQNOHKKOAQMTBKOFSUTUXPRTMXBXNPCLRCEAEOIAWGGVVUSGIOEWLIQFOZKSPVMEBLOHLXDVCYSMGOPJEFCXMRUIGDXNCCRPMLCEWTPZMOQQSAWLPHPTDAWEYJOGQSOAVERCTNQQEAVTUGKLJAXMRTGTIEAFWPTZYIPKESMEAFCGJILSBPLDABNFVRJUXNGQSWIUIGWAAMLDRNNPDXGNPTTGLUHUOBMXSPQNDKBDBTEECLECGRDPTYBVRDATQHKQJMKEFROCLXNFKNSCWANNAHXTRGKCJTTRRUEMQZEAEIPAWEYPAJBBLHUEHMVUNFRPVMEDWEKMHRREOGZBDBROGCGANIUYIBNZQVXTGORUUCUTNBOEIZHEFWNBIGOZGTGWXNRHERBHPHGSIWXNPQMJVBCNEIDVVOAGLPONAPWYPXKEFKOCMQTRTIDZBNQKCPLTTNOBXMGLNRRDNNNQKDPLTLNSUTAXMNPTXMGEZKAEIKAGQ"""
#intxt = "zpgdlrjlajkpylxzpyyglrjgdlrzhzqyjzqrepvmswrzyrigzhzvregkwivssaoltnliuwoldieaqewfiiykhbjowrhdogcqhkwajyaggemisrzqoqhoavlkbjofrylvpsrtgiuavmswlzgmsevwpcdmjsvjqbrnklpcfiowhvkxjbjpmfkrqthtkozrgqihbmqsbivdardymqmpbunivxmtzwqvgefjhucborvwpcdxuwftqmoowjipdsfluqmoeavljgqealrktiwvextvkrrgxani"

c = Cracker(string.ascii_uppercase, p=p, kp=kp_es, r = 4)
print("Utilizando kasiski")
c.attack_kasiski(intxt) # calculamos 

print("\nUtilizando friedman\n")
c.attack_friedman(intxt)
#print(c.friedmann_analysis(intxt))