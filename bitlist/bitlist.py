"""Simple bit string data structure.

Minimal Python library for working with little-endian list
representation of bit vectors.
"""

from __future__ import annotations
from typing import Sequence
from parts import parts
import doctest

class bitlist():
    """
    Class for bit vectors.

    >>> bitlist(123)
    bitlist('1111011')
    >>> int(bitlist('1111011'))
    123
    >>> bitlist(bytes([123]))
    bitlist('01111011')
    >>> bitlist(bytes([123, 123]))
    bitlist('0111101101111011')
    >>> bitlist(bytes([1, 2, 3]))
    bitlist('000000010000001000000011')
    >>> int.from_bytes(bitlist('10000000').to_bytes(), 'big')
    128
    >>> int.from_bytes(bitlist('1000000010000011').to_bytes(), 'big')
    32899
    >>> int.from_bytes(bitlist('110000000').to_bytes(), 'big')
    384
    >>> bitlist(129 + 128*256).to_bytes()
    b'\x80\x81'
    >>> int(bitlist(bytes([128,129]))) == int.from_bytes(bytes([128,129]), 'big')
    True

    >>> bitlist('11') + bitlist('10')
    bitlist('1110')
    >>> bitlist(256)*2
    bitlist('100000000100000000')
    >>> bitlist('11010001') / 2
    [bitlist('1101'), bitlist('0001')]
    >>> bitlist('11010001') / [4]
    [bitlist('1101'), bitlist('0001')]
    >>> bitlist('11010001') / [2]
    [bitlist('11'), bitlist('01'), bitlist('00'), bitlist('01')]
    >>> bitlist('11010001') / [3]
    Traceback (most recent call last):
        ...
    ValueError: cannot split into parts of equal length given the supplied length

    >>> bitlist('1111011')[2]
    1
    >>> bitlist('0111011')[0]
    0
    >>> x = bitlist('1111011')
    >>> x[2] = 0
    >>> x
    bitlist('1101011')
    >>> bitlist('10101000')[0:5]
    bitlist('10101')

    >>> bitlist('11') << 2
    bitlist('1100')
    >>> bitlist('1111') >> 2
    bitlist('11')

    >>> bitlist('111') == bitlist(7)
    True
    >>> bitlist(123) == bitlist(0)
    False
    >>> bitlist(123) == bitlist('0001111011')
    True
    >>> bitlist('001') == bitlist('1')
    True
    >>> bitlist(123) > bitlist(0)
    True
    >>> bitlist(123) < bitlist(0)
    False
    >>> bitlist(123) <= bitlist(0)
    False

    """

    def __init__(self: bitlist, argument = None):
        """
        Parse argument depending on its type and build bit string.
        """
        if argument is None:
            # By default, always return the bit vector representing zero.
            self.bits = bytearray([0])

        elif isinstance(argument, int):
            # Convert any integer into its bit representation,
            # starting with the first non-zero digit.
            self.bits =\
                bytearray(\
                    reversed([int(b) for b in "{0:b}".format(argument)])
                )

        elif isinstance(argument, str) and len(argument) > 0:
            # Convert string of binary digit characters.
            self.bits =\
                bytearray(reversed([int(b) for b in argument]))

        elif isinstance(argument, bytearray) or\
             isinstance(argument, bytes):
            # Convert bytes-like object into its constituent bits,
            # with exactly eight bits per byte (i.e., leading zeros
            # are included).
            self.bits =\
                bytearray([\
                    b
                    for byte in reversed(argument)
                    for b in [(byte >> i) % 2 for i in range(0, 8)]
                ])

        elif isinstance(argument, list) and\
             all(isinstance(x, int) and x in (0, 1) for x in argument):
            # Convert list of binary digits represented as integers.
            self.bits =\
                bytearray(argument) if len(argument) > 0 else bytearray([0])

        else:
            raise ValueError("bitlist constructor received unsupported argument")

    def __str__(self: bitlist) -> str:
        return "bitlist('" + "".join(list(reversed([str(b) for b in self.bits]))) + "')"

    def __repr__(self: bitlist) -> str:
        return str(self)

    def __int__(self: bitlist) -> int:
        return sum(b*(2**i) for (i,b) in enumerate(self.bits))

    def to_bytes(self: bitlist) -> bytes:
        return bytes(reversed([int(bitlist(list(bs))) for bs in parts(self.bits, length=8)]))

    def __truediv__(self: bitlist, other) -> Sequence[bitlist]:
        """
        Break up a bit list into a number of parts or parts of a
        certain length.
        """
        if type(other) is list and len(other) > 0 and type(other[0]) is int:
            if other[0] <= 0:
                raise ValueError("can only split into parts of positive non-zero length")
            elif len(self.bits) % other[0] != 0:
                raise ValueError("cannot split into parts of equal length given the supplied length")
            else:
                return list(reversed([
                    bitlist(list(p)) 
                    for p in parts(self.bits, length=other[0])
                ]))
        elif type(other) is int:
            if other <= 0:
                raise ValueError("can only split into a positive non-zero number of parts")
            elif len(self.bits) % other != 0:
                raise ValueError("cannot split into specified number of parts of equal length")
            else:
                return list(reversed([
                    bitlist(list(p)) 
                    for p in parts(self.bits, other)
                ]))
        else:
            raise ValueError("splitting parameter is not valid")

    def __add__(self: bitlist, other: bitlist) -> bitlist:
        return bitlist([b for b in other.bits]+[b for b in self.bits])

    def __mul__(self: bitlist, other) -> bitlist:
        if isinstance(other, int):
            return bitlist([b for b in self.bits]*other)
        else:
            raise ValueError("repetition parameter must be an integer")

    def __getitem__(self: bitlist, key):
        if isinstance(key, int):
            if key < 0: # Support "big-endian" interface using negative indices.
                return self.bits[abs(key)-1] if abs(key) <= len(self.bits) else 0
            elif key < len(self.bits):
                return self.bits[len(self.bits) - 1 - key]
            else:
                raise IndexError("bitlist index out of range")
        elif isinstance(key, slice):
            return bitlist(list(reversed((list(reversed(self.bits))[key]))))
        else:
            raise TypeError("bitlist indices must be integers or slices")

    def __setitem__(self: bitlist, i: int, b):
        if i < 0: # Support "big-endian" interface using negative indices.
            self.bits =\
                bytearray([
                    (self[j] if j != i else b)
                    for j in range(-1, min(-len(self.bits), -abs(i)) - 1, -1)
                ])
        elif i < len(self.bits):
            i = len(self.bits) - 1 - i
            self.bits =\
                bytearray([
                    (self.bits[j] if j != i else b) 
                    for j in range(0, len(self.bits))
                ])
        else:
            raise IndexError("bitlist index out of range")

    def __len__(self: bitlist) -> int:
        return len(self.bits)

    def __lshift__(self: bitlist, n: int) -> bitlist:
        return bitlist(list([0] * n) + list(self.bits))

    def __rshift__(self: bitlist, n: int) -> bitlist:
        return bitlist(list(self.bits[n:len(self.bits)]))

    def __eq__(self: bitlist, other: bitlist) -> bool:
        # Ignores leading zeros in representation.
        return int(self) == int(other)

    def __ne__(self: bitlist, other: bitlist) -> bool:
        # Ignores leading zeros in representation.
        return int(self) != int(other)

    def __lt__(self: bitlist, other: bitlist) -> bool:
        return int(self) < int(other)

    def __le__(self: bitlist, other: bitlist) -> bool:
        return int(self) <= int(other)

    def __gt__(self: bitlist, other: bitlist) -> bool:
        return int(self) > int(other)

    def __ge__(self: bitlist, other: bitlist) -> bool:
        return int(self) >= int(other)

if __name__ == "__main__":
    doctest.testmod()
