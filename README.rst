=======
bitlist
=======

Minimal pure Python library for working with little-endian list representation of bit strings.

Purpose
-------
This library allows programmers to work with a little-endian representation of bit strings within Python. Its purpose is primarily pedagogical, although it can be useful under other circumstances.

Package Installation and Usage
------------------------------
The package is available on PyPI:

    python -m pip install bitlist

The library can be imported in the usual way:

    import bitlist
    from bitlist import bitlist

Testing
-------

The library comes with a number of tests:

    nosetests

Examples
--------
An example of usage (a bitwise addition function) is provided  below::

    from bitlist import bitlist
    def add(x, y):
        k = len(x)
        l = len(y)
        r = bitlist(0)
        c = 0
        for i in range(0, max(k,l)): # Upper bound is not inclusive.
            r[i] = (x[i] ^ y[i]) ^ c
            c = (x[i] & y[i]) | (x[i] & c) | (y[i] & c)
        r[max(k,l)] = c
        return r