import math
import random
import collections

Pt = collections.namedtuple("Pt", ["x", "y"])

class Persona():
    def __init__(self, name, ecc):
        self.name = name
        self.ecc = ecc
        self.priv = self.choose_priv()
        self.pub = self.get_pub()
        
    def choose_priv(self):
        return random.randint(1, self.ecc.curve.p-1)
    
    def get_pub(self):
        return self.ecc.gen_public(self.priv)
    #TODO
    

class EllipticCurve():
    
    
    def __init__(self, a, b, p):
        if (0 < a and a < p and 0 < b and b < p and p > 2):
            self.a = a
            self.b = b
            self.p = p
        else:
            print("invalid curve parameters")
    
    
    def inv(self, n, p):
        for i in range(p):
            if (n * i) % p == 1:
                print("returning i from inv")
                return i
    
    def func(self, x):
        #TODO when to mod?
        y = math.sqrt(x**3 + self.a*x + self.b) % self.p
        return y 
    
    def reflect_x(self, pt):
        """
        negate y coordinate of pt
        """
        return pt
    
    def validate(self, pt):
        #TODO redundant?
            
        # return self.func(pt.y) == math.sqrt(pt.x**3 + self.a*pt.x + self.b) % self.p
        return True
    
    def add_op(self, pt, n):
        """
        recursively calculate additions
        """
        #TODO cover edge cases where x values are equal
        
        if n == 0:
            print("base case")
            print(type(pt))
            return pt
        else:
            #calc tangent at from_pt
            #get intersection of tangent
            #to_pt = negate y coord of intersection
            from_pt = self.add_op(pt, n-1)
            l = (3 * from_pt.x**2 + self.a) * self.inv(2 * from_pt.y, self.p) % self.p
            x = (l * l - 2*from_pt.x) % self.p
            y = (l * (from_pt.x - x) - from_pt.y) % self.p
            
            return Pt(x, y)
        
        
class ECDH():
    def __init__(self, curve, gtr):
        self.curve = curve
        if self.curve.validate(gtr):
            self.gtr = gtr
        else:
            print("invalid generator")
            # choose new one and print what it is?
            
    def gen_public(self, private):
        print("generator before add_op recursion")
        print(self.gtr.x)
        print(self.gtr.y)
        return self.curve.add_op(self.gtr, private)

        


def main():
    # watching this:
    # https://www.youtube.com/watch?v=yDXiDOJgxmg
    
    G_x = 7
    a = 5
    b = 10
    p = 100
    
    ec = EllipticCurve(a,b,p)
    G_y = ec.func(G_x)
    G = Pt(G_x, G_y)
    print("generator point: {} {}".format(G.x, G.y))
    ecc = ECDH(ec, G)
    
    alice = Persona("alice", ecc)
    bob = Persona("bob", ecc)
    
    for per in enumerate([alice, bob]):
        print("Persona:\t{}\npriv-key:\t{}\npub-key:\t{}\n".format(per.name, per.priv, per.pub))
    
    
    

if __name__ == '__main__':
    main()
    