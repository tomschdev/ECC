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
        self.secret = None
        
    def choose_priv(self):
        # return random.randint(1, 10)
        return random.randint(1, self.ecc.curve.p-1)
    
    def get_pub(self):
        print("\n--- {} is generating public from priv: {} ---*".format(self.name, self.priv))
        pk = self.ecc.gen_public(self.priv, None)
        return pk    
    
    def calc_secret(self, rcvd_pub):
        self.secret = self.ecc.gen_public(self.priv, rcvd_pub)
        return self.secret
  
        
        
class ECDH():
    def __init__(self, curve, gtr):
        self.curve = curve
        if self.curve.contains_point(gtr):
            self.gtr = gtr
        else:
            print("invalid generator")
            # choose new one and print what it is?
            
    def gen_public(self, private, rcvd_pub):
        if rcvd_pub is None:
            return self.curve.double_op_for(self.gtr, private)
            # print("recursive:{}\nfor loop:{}\n".format(rec, fo))
        else:
            return self.curve.double_op_for(rcvd_pub, private)
    
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
    
    def contains_point(self, pt):
        """Is the point (x,y) on this curve?"""
        # return (pt.y * pt.y - ((pt.x * pt.x + self.a) * pt.x + self.b)) % self.__p == 0
            
        return True
    
    # def double_op(self, pt, n, t):
    #     """
    #     recursively calculate additions
    #     """
    #     t+="-"
    #     print("{}call".format(t))
    #     if n == 0:
    #         print("{}base case".format(t))
    #         return pt
    #     else:
    #         from_pt = self.double_op(pt, n-1, t)
    #         xp, yp = from_pt.x, from_pt.y 
    #         m = (3 * xp ** 2 + self.a) / (2 * yp) 
    #         xr = m**2 - 2*xp 
    #         yr = yp + m * (xr - xp) 
    #         to_pt = Pt(xr, -yr)
    #         print("{}return: {} {}".format(t, round(to_pt.x,2), round(to_pt.y, 2)))
    #         return to_pt
        
    def double_op_for(self, pt, n):
        from_pt = pt
        for i in range(n):
            xp, yp = from_pt.x, from_pt.y 
            m = (3 * xp ** 2 + self.a) / (2 * yp) 
            xr = m**2 - 2*xp 
            yr = yp + m * (xr - xp) 
            from_pt = Pt(xr, -yr)
            
        return from_pt
    
    def add_op(self, P, Q):
        xp, yp = P.x, P.y
        xq, yq = Q.x, Q.y
        if xp == xq:
            return double_op_for(P, 1, " ")
        m = (yp - yq) / (xp - xq)
        xr = m**2 - xp - xq
        yr = yp + m * (xr - xp)
        return Pt(xr, -yr)
        
            
            


        


def main():
    # watching this:
    # https://www.youtube.com/watch?v=yDXiDOJgxmg
    
    G_x = 7
    a = 5
    b = 10
    p = 980
    
    ec = EllipticCurve(a,b,p)
    G_y = ec.func(G_x)
    G = Pt(G_x, G_y)
    print("generator point: {} {}".format(G.x, G.y))
    ecc = ECDH(ec, G)
    
    alice = Persona("alice", ecc)
    bob = Persona("bob", ecc)
    
    for per in [alice, bob]:
        print("\nPersona:\t{}\npriv-key:\t{}\npub-key:\t{}\n".format(per.name, per.priv, per.pub))
    
    alice.calc_secret(bob.pub)
    bob.calc_secret(alice.pub)

    for per in [alice, bob]:
        print("\nPersona:\t{}\npriv-key:\t{}\npub-key:\t{}\nsecret:\t{}\n".format(per.name, per.priv, per.pub, per.secret))


if __name__ == '__main__':
    main()
    