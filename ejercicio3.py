"""
Kasiski method
"""

from typing import List, Dict
from math import sqrt
from collections import defaultdict, Counter

MIN_COUNT = 3
MAX_COUNT = 10

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

def count_distance_divisors(distance:int, divisors:Dict[int, int]):

    div = 2
    while div < int(sqrt(distance)):

        if distance % div == 0:
            divisors[div] += 1
            divisors[distance//div] += 1
            distance = distance // div 
        else:
            div += 1 

def find_distances_divisors(divisors:Dict[int, int], distances:set):

    for dist in distances:
        count_distance_divisors(dist, divisors)


def cracker(msg):

    # First we use kazinski method
    pass

intxt = """UECWKDVLOTTVACKTPVGEZQMDAMRNPDDUXLBUICAMRHOECBHSPQLVIWOFFEAILPNTESMLDRUURIFAEQTTPXADWIAWLACCRPBHSRZIVQWOFROGTTNNXEVIVIBPDTTGAHVIACLAYKGJIEQHGECMESNNOCTHSGGNVWTQHKBPRHMVUOYWLIAFIRIGDBOEBQLIGWARQHNLOISQKEPEIDVXXNETPAXNZGDXWWEYQCTIGONNGJVHSQGEATHSYGSDVVOAQCXLHSPQMDMETRTMDUXTEQQJMFAEEAAIMEZREGIMUECICBXRVQRSMENNWTXTNSRNBPZHMRVRDYNECGSPMEAVTENXKEQKCTTHSPCMQQHSQGTXMFPBGLWQZRBOEIZHQHGRTOBSGTATTZRNFOSMLEDWESIWDRNAPBFOFHEGIXLFVOGUZLNUSRCRAZGZRTTAYFEHKHMCQNTZLENPUCKBAYCICUBNRPCXIWEYCSIMFPRUTPLXSYCBGCCUYCQJMWIEKGTUBRHVATTLEKVACBXQHGPDZEANNTJZTDRNSDTFEVPDXKTMVNAIQMUQNOHKKOAQMTBKOFSUTUXPRTMXBXNPCLRCEAEOIAWGGVVUSGIOEWLIQFOZKSPVMEBLOHLXDVCYSMGOPJEFCXMRUIGDXNCCRPMLCEWTPZMOQQSAWLPHPTDAWEYJOGQSOAVERCTNQQEAVTUGKLJAXMRTGTIEAFWPTZYIPKESMEAFCGJILSBPLDABNFVRJUXNGQSWIUIGWAAMLDRNNPDXGNPTTGLUHUOBMXSPQNDKBDBTEECLECGRDPTYBVRDATQHKQJMKEFROCLXNFKNSCWANNAHXTRGKCJTTRRUEMQZEAEIPAWEYPAJBBLHUEHMVUNFRPVMEDWEKMHRREOGZBDBROGCGANIUYIBNZQVXTGORUUCUTNBOEIZHEFWNBIGOZGTGWXNRHERBHPHGSIWXNPQMJVBCNEIDVVOAGLPONAPWYPXKEFKOCMQTRTIDZBNQKCPLTTNOBXMGLNRRDNNNQKDPLTLNSUTAXMNPTXMGEZKAEIKAGQ"""
substrings = dict()
divisors = defaultdict(int)
distances = set()
find_repeated_substrings(intxt, substrings, distances)
find_distances_divisors(divisors, distances)
#print(divisors)

c = Counter(divisors)
print(c.most_common(5))