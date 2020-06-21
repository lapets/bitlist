"""Simple bit string data structure.

Minimal Python library for working with little-endian list
representation of bit vectors.
"""

from __future__ import annotations
from typing import Sequence
import doctest
from parts import parts

class bitlist():
    """
    Class for bit vectors.

    >>> bitlist(123)
    bitlist('1111011')
    >>> int(bitlist('1111011'))
    123
    >>> bitlist(bytes([123]))
    bitlist('01111011')
    >>> bitlist(bytes([123]), 16)
    bitlist('0000000001111011')
    >>> bitlist(16, 64)
    bitlist('0000000000000000000000000000000000000000000000000000000000010000')
    >>> bitlist(bitlist('1010'))
    bitlist('1010')
    >>> bitlist(bitlist(123), 8)
    bitlist('01111011')
    >>> xs = bitlist(123, 8)
    >>> ys = bitlist(xs)
    >>> ys[0] = 1
    >>> xs
    bitlist('01111011')
    >>> ys
    bitlist('11111011')
    >>> bitlist(bytes([123]), 4)
    bitlist('1011')
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


    >>> bitlist(bytes([123])).hex()
    '7b'
    >>> bitlist.fromhex('abcd')
    bitlist('1010101111001101')

    >>> bitlist('11') + bitlist('10')
    bitlist('1110')
    >>> bitlist(256)*2
    bitlist('100000000100000000')
    >>> bitlist('11010001') / 2
    [bitlist('1101'), bitlist('0001')]
    >>> bitlist('11010001') / [2,6]
    [bitlist('11'), bitlist('010001')]
    >>> bitlist('11010001') / {4}
    [bitlist('1101'), bitlist('0001')]
    >>> bitlist('11010001') / 3
    [bitlist('110'), bitlist('100'), bitlist('01')]

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
    >>> bitlist('10101000101010001010100010101000')[0:16]
    bitlist('1010100010101000')

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

    @staticmethod
    def fromhex(s):
        """Build a bitlist from a hexadecimal string."""
        return bitlist(bytes.fromhex(s))

    def __init__(self: bitlist, argument=None, length=None):
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
                bytearray(
                    reversed([int(b) for b in "{0:b}".format(argument)])
                )

        elif isinstance(argument, str) and len(argument) > 0:
            # Convert string of binary digit characters.
            self.bits =\
                bytearray(reversed([int(b) for b in argument]))

        elif isinstance(argument, (bytes, bytearray)):
            # Convert bytes-like object into its constituent bits,
            # with exactly eight bits per byte (i.e., leading zeros
            # are included).
            self.bits =\
                bytearray([
                    b
                    for byte in reversed(argument)
                    for b in [(byte >> i) % 2 for i in range(0, 8)]
                ])

        elif isinstance(argument, list) and\
             all(isinstance(x, int) and x in (0, 1) for x in argument):
            # Convert list of binary digits represented as integers.
            self.bits =\
                bytearray(reversed(argument))\
                if len(argument) > 0 else\
                bytearray([0])

        elif isinstance(argument, bitlist):
            # Make constructor idempotent (but have it iterate
            # to reflect the behavior of `list(...)`.
            self.bits = bytearray(list(argument.bits))

        else:
            raise ValueError("bitlist constructor received unsupported argument")

        if length is not None:
            # Pad or truncate the bit vector to ensure the specified length.
            if length > len(self.bits):
                self.bits = self.bits + bytes([0] * (length - len(self.bits)))
            elif length < len(self.bits):
                self.bits = self.bits[0:length]

    def __str__(self: bitlist) -> str:
        return "bitlist('" + "".join(list(reversed([str(b) for b in self.bits]))) + "')"

    def __repr__(self: bitlist) -> str:
        return str(self)

    def __int__(self: bitlist) -> int:
        return sum(b*(2**i) for (i, b) in enumerate(self.bits))

    def to_bytes(self: bitlist) -> bytes:
        """
        Return a bytes-like object representation. Note that the
        number of bits will be padded to a multiple of eight.
        """
        return bytes(reversed([
            int(bitlist(list(reversed(bs))))
            for bs in parts(self.bits, length=8)
        ]))

    def hex(self):
        """
        Return a hexadecimal string representation. Note that the
        number of bits will be padded to a multiple of eight.
        """
        return self.to_bytes().hex()

    def __len__(self: bitlist) -> int:
        return len(self.bits)

    def __add__(self: bitlist, other: bitlist) -> bitlist:
        return bitlist(list(reversed(list(other.bits)+list(self.bits))))

    def __mul__(self: bitlist, other) -> bitlist:
        if isinstance(other, int):
            return bitlist(list(reversed(list(self.bits)))*other)
        else:
            raise ValueError("repetition parameter must be an integer")

    def __truediv__(self: bitlist, other: int) -> Sequence[bitlist]:
        """
        Break up a bit list into the specified number of parts.
        """
        if isinstance(other, set) and len(other) == 1 and isinstance(list(other)[0], int):
            ps = parts(self.bits, length=list(other)[0])
        elif isinstance(other, list):
            ps = parts(self.bits, length=list(reversed(other)))
        else:
            ps = parts(self.bits, other)
        return list(reversed([bitlist(list(reversed(p))) for p in ps]))

    def __getitem__(self: bitlist, key):
        if isinstance(key, int):
            if key < 0: # Support "big-endian" interface using negative indices.
                return self.bits[abs(key)-1] if abs(key) <= len(self.bits) else 0
            elif key < len(self.bits):
                return self.bits[len(self.bits) - 1 - key]
            else:
                raise IndexError("bitlist index out of range")
        elif isinstance(key, slice):
            return bitlist(list(reversed(self.bits))[key])
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

    def __lshift__(self: bitlist, n: int) -> bitlist:
        return bitlist(list(reversed(list([0] * n) + list(self.bits))))

    def __rshift__(self: bitlist, n: int) -> bitlist:
        return bitlist(list(reversed(self.bits[n:len(self.bits)])))

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
