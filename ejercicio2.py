from string import ascii_lowercase

class Vigenere:

    def __init__(self, alphabet, key):

        self.alphabet=alphabet
        self.key = key

    def encode(self, msg):
        
        return "".join([x for x in msg if x in self.alphabet])

    def _set_key_length(self, target_length):

        n, r = divmod(target_length,len(self.key))
        return self.key*n + self.key[:r]

    def _add_chars(self, a,b):

        ai = self.alphabet.index(a)
        bi = self.alphabet.index(b)

        return self.alphabet[(ai + bi) % len(self.alphabet)]

    def _diff_chars(self, a,b):
    
        ai = self.alphabet.index(a)
        bi = self.alphabet.index(b)

        return self.alphabet[(ai - bi) % len(self.alphabet)]

    def cipher(self, msg):
        msg_encoded = self.encode(msg)
        key = self._set_key_length(len(msg_encoded))
        #print(msg_encoded)
        #print(len(key),len(msg_encoded))
        return "".join(map(lambda x: self._add_chars(x[0],x[1]), zip(key, msg_encoded)))

    def decipher(self, msg):
        msg_encoded = self.encode(msg)
        key = self._set_key_length(len(msg_encoded))
        #print(msg_encoded)
        #print(len(key),len(msg_encoded))
        return "".join(map(lambda x: self._diff_chars(x[0],x[1]), zip(msg_encoded, key)))

V = Vigenere(ascii_lowercase, "lauraguapa")
ciph=V.cipher("era una noche de verano cuando el asesino y la victima se cruzaron en lo que se conocia como el jardin de los tristes. era un momento en el que ambos supieron quie se acercaba una desgracia pero ninguno podía hacer nada para evitar el desastre, tres segundos más tarde solo quedaba un alma en la tierra y una nueva andaba por los jardines del paraiso.")
print(V.decipher(ciph))