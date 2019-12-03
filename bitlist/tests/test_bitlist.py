from unittest import TestCase

from bitlist import bitlist

def add(x, y):
    """Bitwise addition algorithm."""
    k = len(x)
    l = len(y)
    r = bitlist(0)
    c = 0
    for i in range(0, max(k,l)): # Upper bound is not inclusive.
        r[i] = (x[i] ^ y[i]) ^ c
        c = (x[i] & y[i]) | (x[i] & c) | (y[i] & c)
    r[max(k,l)] = c
    return r

def mul(x, y):
    """Bitwise multiplication algorithm."""
    k = len(x)
    l = len(y)
    r = bitlist()
    for i in range(0, k): # Upper bound is not inclusive.
        if x[i] == 1:
            r = add(r, y)
        y = y << 1
    return r

def exp(x, y):
    """Bitwise exponentiation algorithm."""
    k = len(x)
    l = len(y)
    r = bitlist(1)
    for i in range(0, l): # Upper bound is not inclusive.
        if y[i] == 1:
            r = mul(r, x)
        x = mul(x, x)
    return r

def div(x, y):
    """Bitwise division algorithm."""
    k = len(x)
    l = len(y)
    if y > x:
        return bitlist(0)
    for i in range(0, k):
        y = y << 1
    t = bitlist(0)
    q = bitlist(0)
    p = bitlist(2**k)
    for i in range(0, k+1):
        if add(t, y) <= x:
            t = add(t, y)
            q = add(q, p)
        y = y >> 1
        p = p >> 1
    return q

class TestBitList(TestCase):
    def test_from_integer(self):
        self.assertEqual(bitlist(123), bitlist('1111011'))

    def test_add(self):
        op = lambda a,b: int(add(bitlist(a), bitlist(b)))
        for (x,y) in [(a+b, op(a,b)) for a in range(0,100) for b in range(0,100)]:
            self.assertEqual(x, y)

    def test_mul(self):
        op = lambda a,b: int(mul(bitlist(a), bitlist(b)))
        for (x,y) in [(a*b, op(a,b)) for a in range(0,30) for b in range(0,30)]:
            self.assertEqual(x, y)

    def test_exp(self):
        op = lambda a,b: int(exp(bitlist(a), bitlist(b)))
        for (x,y) in [(a**b, op(a,b)) for a in range(0,12) for b in range(0,4)]:
            self.assertEqual(x, y)

    def test_div(self):
        op = lambda a,b: int(div(bitlist(a), bitlist(b)))
        for (x,y) in [(a//b, op(a,b)) for a in range(0,12) for b in range(1,12)]:
            self.assertEqual(x, y)
