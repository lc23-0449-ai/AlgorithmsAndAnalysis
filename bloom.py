#Coded by Toby, Diego, and Owen

class BloomFilter:

    def __init__(self, bit_size=100_000):
        self.bloom = 0
        self.bit_size = bit_size

    def my_hash(self,x):
        i = 0
        j = x
        while (x>>i) is not 0:
            i +=1
            j += (x>>i&0b1) * ((i*10)+i)
        return j


    def add(self, key):
        k1 = abs(hash(key)) % self.bit_size
        k2 = self.my_hash(k1) % self.bit_size
        self.bloom |= 1 << k1
        self.bloom |= 1 << k2

    def might_contain(self,key):
        k1 = abs(hash(key)) % self.bit_size
        k2 = self.my_hash(k1) % self.bit_size
        return bool((self.bloom >> k1 & 1) and (self.bloom >> k2 & 1))

    def _true_bits(self):
        return bin(self.bloom).count("1")