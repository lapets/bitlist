=======
bitlist
=======

Minimal Python library for working with bit vectors natively.

|pypi| |travis| |coveralls|

.. |pypi| image:: https://badge.fury.io/py/bitlist.svg
   :target: https://badge.fury.io/py/bitlist
   :alt: PyPI version and link.

.. |travis| image:: https://travis-ci.com/lapets/bitlist.svg?branch=master
   :target: https://travis-ci.com/lapets/bitlist

.. |coveralls| image:: https://coveralls.io/repos/github/lapets/bitlist/badge.svg?branch=master
   :target: https://coveralls.io/github/lapets/bitlist?branch=master

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

An example of usage (a bitwise addition function) is provided below::

    from bitlist import bitlist
    def add(x, y):
        """Bitwise addition algorithm."""
        r = bitlist(0)

        # Upper bound is not inclusive.
        # Use negative indices for big-endian interface.
        carry = 0
        for i in range(1, max(len(x), len(y)) + 1):
            r[-i] = (x[-i] ^ y[-i]) ^ carry
            carry = (x[-i] & y[-i]) | (x[-i] & carry) | (y[-i] & carry)
        r[-(max(len(x), len(y)) + 1)] = carry

        return r

Testing and Conventions
-----------------------
All unit tests are executed and their coverage is measured when using `nose <https://nose.readthedocs.io/>`_ (see ``setup.cfg`` for configution details)::

    nosetests

The subset of the unit tests included in the module itself can be executed using `doctest <https://docs.python.org/3/library/doctest.html>`_::

    python bitlist/bitlist.py -v

Style conventions are enforced using `Pylint <https://www.pylint.org/>`_::

    pylint bitlist

Contributions
-------------
In order to contribute to the source code, open an issue or submit a pull request on the GitHub page for this library.

Versioning
----------
Beginning with version 0.3.0, the version number format for this library and the changes to the library associated with version number increments conform with `Semantic Versioning 2.0.0 <https://semver.org/#semantic-versioning-200>`_.
