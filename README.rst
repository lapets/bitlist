=======
bitlist
=======

Minimal Python library for working with bit vectors natively.

.. image:: https://badge.fury.io/py/bitlist.svg
   :target: https://badge.fury.io/py/bitlist
   :alt: PyPI version and link.

Purpose
-------
This library allows programmers to work with a native representation of bit vectors within Python.

Package Installation and Usage
------------------------------
The package is available on PyPI::

    python -m pip install bitlist

The library can be imported in the usual way::

    import bitlist
    from bitlist import bitlist

Testing
-------

The library comes with a number of tests::

    nosetests
    bitlist/bitlist.py -v

Examples
--------
An example of usage (a bitwise addition function) is provided below::

    from bitlist import bitlist
    def add(x, y):
        """Bitwise addition algorithm."""
        k = len(x)
        l = len(y)
        r = bitlist(0)

        # Upper bound is not inclusive.
        # Use negative indices for big-endian interface.
        carry = 0
        for i in range(1, max(k, l) + 1):
            r[-i] = (x[-i] ^ y[-i]) ^ carry
            carry = (x[-i] & y[-i]) | (x[-i] & carry) | (y[-i] & carry)
        r[-(max(k, l) + 1)] = carry
