"""
Kasiski method
"""

from typing import List, Dict
from math import sqrt, gcd
from collections import defaultdict, Counter
from ejercicio2 import Vigenere
import string

MIN_COUNT = 3
MAX_COUNT = 6

def get_distance(substring, offset, substring_map, distances):

    if substring in substring_map:
        last_offset = substring_map.get(substring)
        distances.add(offset-last_offset)
    else:
        substring_map[substring] = offset


def find_repeated_substrings(text:str, substring_map:Dict[str, int], distances:set):

    count, offset = MIN_COUNT, 0

    while (offset + count < len(text)):
        while (offset + count < len(text) and MAX_COUNT >= count):
            substring = text[offset:offset+count]
            get_distance(substring, offset, substring_map, distances)
            count +=1

        offset += 1
        count = MIN_COUNT

def gcd_distance(distances):
    dst=list(distances)
    g=dst[0]
    for i in dst[1:]:
        prev = g
        g=gcd(g,i)
        if g == 1:
            g=prev
    return g

def count_distance_divisors(distance:int):
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

'''def find_distances_divisors(divisors:Dict[int, int], distances:set):

    for dist in distances:
        count_distance_divisors(dist, divisors)
'''
def extract_frequencies(s:str, alph:str):
    n_app=Counter(s)
    freq=[]
    for char in alph:
        n=n_app.get(char)
        if n:
            freq.append(n/len(s))
        else:
            freq.append(0)
    return freq   

def MIC(p, s:str, alph:str):
    s_freq = extract_frequencies(s, alph)
    return sum(map(lambda x:x[0]*x[1],zip(p,s_freq)))/len(s)

def shift_by_n(s:str, n:int, alph:str):
    return "".join([alph[(alph.index(char)+n)%len(alph)] for char in s])

def compute_most_probable(s:str,p, alph:str):
    mic=[]
    for i in range(len(alph)):
        mic.append(MIC(p, shift_by_n(s,i,alph), alph))
    #print(mic)
    candidate=max(enumerate(mic), key=lambda x: x[1])[0]
    return (len(alph)-candidate)%len(alph)


def cracker(msg, k, alph, p):
    
    s_i=[[]for i in range(k)]
    pos=0
    for c in msg:
        s_i[pos].append(c)
        pos+=1
        if pos==k:
            pos=0
    
    for i,lst in enumerate(s_i):
        s_i[i]="".join(lst)

    keys=[]
    for lst in s_i:
        keys.append(compute_most_probable(lst,p,alph))
    #print(keys)
    return "".join([alph[i] for i in keys]) 
    #return keys

def kasiski(intxt):
    substrings = dict()
    divisors = defaultdict(int)
    distances = set()
    find_repeated_substrings(intxt, substrings, distances)
    distance=gcd_distance(distances)
    #print(distance)
    #print(count_distance_divisors(distance))
    return count_distance_divisors(distance)

p=[0.1253, 0.014199999999999999, 0.046799999999999994, 0.058600000000000006, 0.1368, 0.0069, 0.0101, 0.006999999999999999, 0.0625, 0.0044, 0.0002, 0.049699999999999994, 0.0315, 0.06709999999999999, 0.0868, 0.025099999999999997, 0.0088, 0.0687, 0.07980000000000001, 0.0463, 0.0393, 0.009000000000000001, 0.0001, 0.0022, 0.009000000000000001, 0.0052]

#intxt = """UECWKDVLOTTVACKTPVGEZQMDAMRNPDDUXLBUICAMRHOECBHSPQLVIWOFFEAILPNTESMLDRUURIFAEQTTPXADWIAWLACCRPBHSRZIVQWOFROGTTNNXEVIVIBPDTTGAHVIACLAYKGJIEQHGECMESNNOCTHSGGNVWTQHKBPRHMVUOYWLIAFIRIGDBOEBQLIGWARQHNLOISQKEPEIDVXXNETPAXNZGDXWWEYQCTIGONNGJVHSQGEATHSYGSDVVOAQCXLHSPQMDMETRTMDUXTEQQJMFAEEAAIMEZREGIMUECICBXRVQRSMENNWTXTNSRNBPZHMRVRDYNECGSPMEAVTENXKEQKCTTHSPCMQQHSQGTXMFPBGLWQZRBOEIZHQHGRTOBSGTATTZRNFOSMLEDWESIWDRNAPBFOFHEGIXLFVOGUZLNUSRCRAZGZRTTAYFEHKHMCQNTZLENPUCKBAYCICUBNRPCXIWEYCSIMFPRUTPLXSYCBGCCUYCQJMWIEKGTUBRHVATTLEKVACBXQHGPDZEANNTJZTDRNSDTFEVPDXKTMVNAIQMUQNOHKKOAQMTBKOFSUTUXPRTMXBXNPCLRCEAEOIAWGGVVUSGIOEWLIQFOZKSPVMEBLOHLXDVCYSMGOPJEFCXMRUIGDXNCCRPMLCEWTPZMOQQSAWLPHPTDAWEYJOGQSOAVERCTNQQEAVTUGKLJAXMRTGTIEAFWPTZYIPKESMEAFCGJILSBPLDABNFVRJUXNGQSWIUIGWAAMLDRNNPDXGNPTTGLUHUOBMXSPQNDKBDBTEECLECGRDPTYBVRDATQHKQJMKEFROCLXNFKNSCWANNAHXTRGKCJTTRRUEMQZEAEIPAWEYPAJBBLHUEHMVUNFRPVMEDWEKMHRREOGZBDBROGCGANIUYIBNZQVXTGORUUCUTNBOEIZHEFWNBIGOZGTGWXNRHERBHPHGSIWXNPQMJVBCNEIDVVOAGLPONAPWYPXKEFKOCMQTRTIDZBNQKCPLTTNOBXMGLNRRDNNNQKDPLTLNSUTAXMNPTXMGEZKAEIKAGQ"""
intxt = "zpgdlrjlajkpylxzpyyglrjgdlrzhzqyjzqrepvmswrzyrigzhzvregkwivssaoltnliuwoldieaqewfiiykhbjowrhdogcqhkwajyaggemisrzqoqhoavlkbjofrylvpsrtgiuavmswlzgmsevwpcdmjsvjqbrnklpcfiowhvkxjbjpmfkrqthtkozrgqihbmqsbivdardymqmpbunivxmtzwqvgefjhucborvwpcdxuwftqmoowjipdsfluqmoeavljgqealrktiwvextvkrrgxani"

#print(intxt)

"""substrings = dict()
divisors = defaultdict(int)
distances = set()
find_repeated_substrings(intxt, substrings, distances)
find_distances_divisors(divisors, distances)
#print(divisors)

c = Counter(divisors)
print(c.most_common(5))"""

def break_code(intxt, alph, p):
    keys = []
    for length in kasiski(intxt):
        keys.append(cracker(intxt,length,alph,p))

    return keys

alph = string.ascii_lowercase
#alph = string.ascii_uppercase

for key in break_code(intxt, alph, p):
    V = Vigenere(alph, cracker(intxt,len(key),alph,p))
    print(f"Llave con longitud {len(key)}: {key}")
    print("Texto: ")
    print(V.decipher(intxt))