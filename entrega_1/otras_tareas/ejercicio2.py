"""
Laura Sanchez Parra
Yabir Garcia Benchakhtir
"""

from string import ascii_lowercase

class Vigenere:
    """
    Clase para manejar las funcionalidades basicas del cifrado con Vigenere.

    Para inicializar la clase se necesita proporcionar:

    - Un alfabeto en formato string
    - Una clave en formato string

    Se proporcionan los metodos

    - encode(msg)
    - cipher(msg)
    - decipher(msg)

    """

    def __init__(self, alphabet, key):

        self.alphabet=alphabet
        self.key = key

    def encode(self, msg):
        """
        Codificamos el menaje de entrada eliminando los caracteres que no
        pertenecen al alfabeto.
        """
        
        return "".join([x for x in msg if x in self.alphabet])

    def _set_key_length(self, target_length):
        """
        Función auxiliar para repetir la clave tantas veces como sea neceario
        hasta completar una cadena que sea tan larga como el mensaje que se
        quiere codificar.
        """

        n, r = divmod(target_length,len(self.key))
        return self.key*n + self.key[:r]

    def _add_chars(self, a,b):
        """
        Operación para sumar caracteres dentro del alfabeto proporcionado
        """

        ai = self.alphabet.index(a)
        bi = self.alphabet.index(b)

        return self.alphabet[(ai + bi) % len(self.alphabet)]

    def _diff_chars(self, a,b):
        """
        Operación para restar caracteres dentro del alfabeto proporcionado
        """

        ai = self.alphabet.index(a)
        bi = self.alphabet.index(b)

        return self.alphabet[(ai - bi) % len(self.alphabet)]

    def cipher(self, msg):
        """
        Metodo para codificar un mensaje
        """

        # En primer lugar codificamos el mensaje
        msg_encoded = self.encode(msg)
        # Repetimos la clave hasta que tiene la longitud del mensaje codificado
        key = self._set_key_length(len(msg_encoded))
        # Sumamos caracter a carater mensaje codificado y clave
        return "".join(map(lambda x: self._add_chars(x[0],x[1]), zip(key, msg_encoded)))

    def decipher(self, msg):
        """
        Metodo para decodifar un mensaje
        """
        
        # En primer lugar elimanamos caracteres que no pertenezcan al alfabeto elegido
        msg_encoded = self.encode(msg)
        # Repetimos la clave hasta que alcanza una longitud deseada
        key = self._set_key_length(len(msg_encoded))
        # Aplicamos la operación de diferencia entre el mensaje cifrado y la clave
        return "".join(map(lambda x: self._diff_chars(x[0],x[1]), zip(msg_encoded, key)))


if __name__ == '__main__':

    # Ejemplo de uso

    # Inicializamos la clase con el alphabeto de los caracteres en minuscula y
    # la clabe lauranover

    V = Vigenere(ascii_lowercase, "lauranover")
    #text = "era una noche de verano cuando el asesino y la victima se cruzaron en lo que se conocia como el jardin de los tristes. era un momento en el que ambos supieron quie se acercaba una desgracia pero ninguno podía hacer nada para evitar el desastre, tres segundos más tarde solo quedaba un alma en la tierra y una nueva andaba por los jardines del paraiso."
    
    # Texto que vamos a cifrar
    text = """the inmesurable days were comming to an end while the people in the village were thinking about a possible solution to the big problem. Many were sad because the crops didnt provide enought food for the children, other were sad because they could scape from
    the reallity that a inmense monster called the death was walking in the streets waiting for someone to exist their houses to 
    end their suffering."""

    # Lo ciframos
    ciph=V.cipher(text)
    # Imprimimos el texto cifrado
    print(ciph)
    #Imprimimos el texto descifrado
    print("------")
    print(V.decipher(ciph))