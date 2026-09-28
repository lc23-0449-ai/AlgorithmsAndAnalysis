#Made by Toby S, Owen E, and Diego
#2250 - Toby S
#6456 - Diego
#1652 - Owen E


import math

class Fraction:
    def __init__(self,a,b):
        self.a = a
        self.b = b
        gcd = math.gcd(self.a, self.b)
        self.a = self.a // gcd
        self.b = self.b // gcd


    def __repr__(self):
        gcd = math.gcd(self.a, self.b)
        self.a = self.a // gcd
        self.b = self.b // gcd
        neg = ""

        if self.a*self.b < 0:
            neg = "-"
        return neg + str(abs(self.a)) + '/' + str(abs(self.b))


    def __eq__(self, other):
        if float(self) == float(other):
            return True
        else:
            return False

    def __lt__(self, other):
        if float(self) < float(other):
            return True
        else:
            return False


    def __gt__(self, other):
        if float(self) > float(other):
            return True
        else:
            return False
    def __le__(self, other):
        if float(self) <= float(other):
            return True
        else:
            return False
    def __ge__(self, other):
        if float(self) >= float(other):
            return True
        else:
            return False

    def __add__ (self,other):
        sn = self.a
        sd = self.b
        tn = other.a
        td = other.b

        sn = sn * td + tn * sd
        sd = sd * td
        self.a = sn
        self.b = sd
        return self

    def __sub__(self,other):
        sn = self.a
        sd = self.b
        tn = other.a
        td = other.b

        sn = sn * td - tn * sd
        sd = sd * td
        self.a = sn
        self.b = sd
        return self

    def __mul__(self, other):
        sn = self.a
        sd = self.b
        tn = other.a
        td = other.b

        self.a = sn * tn
        self.b = sd * td
        return self

    def __truediv__(self, other):
        sn = self.a
        sd = self.b
        tn = other.a
        td = other.b

        self.a = sn * td
        self.b = sd * tn
        return self
        pass


    def __float__(self):
        return self.a / self.b
        pass


a = Fraction(2, 3)
b = Fraction(1, 2)
print(a)
print(b)
