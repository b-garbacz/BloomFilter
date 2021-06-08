from bitarray import bitarray
from Crypto.Hash import keccak
import numpy as np

# https://www.eecs.harvard.edu/~michaelm/postscripts/tr-02-05.pdf
#TODO Modyfikacja zależnie od wymagań, testy jednostkowe

def keccak_256(string):
    keccak_hash = keccak.new(digest_bits = 256)
    keccak_hash.update(str.encode(string))
    h = keccak_hash.hexdigest()
    return h


class BloomFilter(object):
    def __init__(self, n, k, false_possitive):
        self.n = n
        self.m = int(np.ceil(-(n * np.log(false_possitive)) / (2 ** np.log(2)))) # optymalna liczba bitów w tablicy
        self.k = k #liczba haszów
        self.bloom_array = bitarray(self.m)  #utworzenie bitowej tablicy m-elementowej
        self.bloom_array.setall(False) #ustawienie wszystkich bitów na 0
        self.counter = 0

    #funkcja haszujaca

    def hash(self, element):
        list_of_hashes = []

        ''' 
        keccak_hash = keccak.new(digest_bits = 256)  # narazie keccak 256
        keccak_hash2 = keccak.new(digest_bits = 256)
        keccak_hash.update(str.encode(element))
        keccak_hash2.update(str.encode(keccak_hash.hexdigest()))  # ewentualnie h2(element) ale nad tym potem pomysl bo generalnie hash od hasha nic raczej nie da.Weryfikacja
        h1 = int(keccak_hash.hexdigest(), 16)  # konwert z hexa na inta
        h2 = int(keccak_hash2.hexdigest(), 16)

        '''
        h1 = keccak_256(element)
        h2 = keccak_256(element)
        for i in range(self.k):
            list_of_hashes.append((int(h1, 16) + i * int(h2, 16)) % self.m)
        return list_of_hashes

    def update_counter(self):
        self.counter = self.counter + 1
        return self.counter

    def check_counter(self):
        print(self.counter ,"elements has been added")

    def add_element(self, element):
        list_of_hashes = self.hash(element)
        for index in list_of_hashes:
            self.bloom_array[index] = True
        self.update_counter()
        print("counter", self.counter)
        #print(self.bittab)

    def query(self, possible_element):
        list_of_hashes = self.hash(possible_element)
        for index in list_of_hashes:
            if self.bloom_array[index] == True:
                return True
        return False






bl =  BloomFilter(10000,2,0.1)
bl.add_element("name1")
bl.check_counter()
bl.add_element("name2")
bl.add_element("name3")

print(bl.query("name1"),"tuuuuu")
print(bl.query("name4"),"tuuuuuu2")
print(bl.query("name5"))

bl.check_counter()