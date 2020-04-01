"""Simple bit string data structure.

Minimal Python library for working with little-endian list
representation of bit vectors.
"""

import doctest

class bitlist():
    """
    Class for bit vectors.

    >>> bitlist(123)
    bitlist('1111011')
    >>> int(bitlist('1111011'))
    123

    >>> bitlist('1111011')[2]
    1
    >>> bitlist('1111011')[0]
    1
    >>> bitlist('1111011')[2] = 1

    >>> bitlist('11') << 2
    bitlist('1100')
    >>> bitlist('1111') >> 2
    bitlist('11')

    >>> bitlist('111') == bitlist(7)
    True
    >>> bitlist(123) == bitlist(0)
    False
    >>> bitlist(123) > bitlist(0)
    True
    >>> bitlist(123) < bitlist(0)
    False
    >>> bitlist(123) <= bitlist(0)
    False

    """

    def __init__(self, argument = None):
        """
        Parse argument depending on its type and build bit string.
        """
        if argument is None:
            self.bits = bytearray([0])
        elif isinstance(argument, int):
            self.bits = bytearray(reversed([int(b) for b in "{0:b}".format(arg)]))
        elif isinstance(argument, str) and len(argument) > 0:
            bytearray(reversed([int(b) for b in arg]))
        elif isinstance(argument, bytearray) and\
             len(argument) > 0 and\
             all(x in [0, 1] for x in argument):
            self.bits = argument
        else:
            raise ValueError("bitlist constructor received unsupported argument")

    def __str__(self):
        return "bitlist('" + "".join(list(reversed([str(b) for b in self.bits]))) + "')"

    def __repr__(self):
        return str(self)

    def __int__(self):
        return int("".join(reversed([str(b) for b in self.bits])), 2)

    def __getitem__(self, i):
        if i < 0: # Support "big-endian" interface using negative indices.
            return self.bits[abs(i)-1] if abs(i) <= len(self.bits) else 0
        elif i < len(self.bits):
            return self.bits[len(self.bits) - 1 - i]
        else:
            raise IndexError("bitlist index out of range")

    def __setitem__(self, i, b):
        if i < 0: # Support "big-endian" interface using negative indices.
            self.bits =\
                bytearray([
                    (self[j] if j != i else b)
                    for j in range(-1, min(-len(self.bits), -abs(i)) - 1, -1)
                ])
        elif i < len(self.bits):
            self.bits =\
                bytearray([
                    (self.bits[j] if j != i else b) 
                    for j in range(0, len(self.bits))
                ])
        else:
            raise IndexError("bitlist index out of range")

    def __len__(self):
        return len(self.bits)

    def __lshift__(self, n):
        return bitlist(bytearray([0] * n) + self.bits)

    def __rshift__(self, n):
        return bitlist(self.bits[n:len(self.bits)])

    def __eq__(self, other):
        return int(self) == int(other)

    def __lt__(self, other):
        return int(self) < int(other)

    def __le__(self, other):
        return int(self) <= int(other)

if __name__ == "__main__":
    doctest.testmod()
