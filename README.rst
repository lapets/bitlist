=======
bitlist
=======

Minimal Python library for working with bit vectors natively.

|pypi| |readthedocs| |actions| |coveralls|

.. |pypi| image:: https://badge.fury.io/py/bitlist.svg
   :target: https://badge.fury.io/py/bitlist
   :alt: PyPI version and link.

.. |readthedocs| image:: https://readthedocs.org/projects/bitlist/badge/?version=latest
   :target: https://bitlist.readthedocs.io/en/latest/?badge=latest
   :alt: Read the Docs documentation status.

.. |actions| image:: https://github.com/lapets/bitlist/workflows/lint-test-cover-docs/badge.svg
   :target: https://github.com/lapets/bitlist/actions/workflows/lint-test-cover-docs.yml
   :alt: GitHub Actions status.

.. |coveralls| image:: https://coveralls.io/repos/github/lapets/bitlist/badge.svg?branch=main
   :target: https://coveralls.io/github/lapets/bitlist?branch=main
   :alt: Coveralls test coverage summary.

Purpose
-------
This library allows programmers to work with a native representation of bit vectors within Python.

Installation and Usage
----------------------
The package is available on `PyPI <https://pypi.org/project/bitlist/>`_::

    python -m pip install bitlist

The library can be imported in the usual way::

    import bitlist
    from bitlist import bitlist

A basic example of usage (a bitwise addition function) is provided below::

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

The testing suite ``test/test_bitlist.py`` contains additional examples of bitwise arithmetic operations implemented with the help of this library.

Development
-----------
All installation and development dependencies are managed using `setuptools <https://pypi.org/project/setuptools>`__ and are fully specified in ``setup.py``. The ``extras_require`` parameter is used to `specify optional requirements <https://setuptools.pypa.io/en/latest/userguide/dependency_management.html#optional-dependencies>`__ for various development tasks. This makes it possible to specify additional options (such as ``docs``, ``lint``, and so on) when performing installation using `pip <https://pypi.org/project/pip>`__::

    python -m pip install .[docs,lint]

Documentation
^^^^^^^^^^^^^
.. include:: toc.rst

The documentation can be generated automatically from the source files using `Sphinx <https://www.sphinx-doc.org/>`_::

    python -m pip install .[docs]
    cd docs
    sphinx-apidoc -f -E --templatedir=_templates -o _source .. ../setup.py && make html

Testing and Conventions
^^^^^^^^^^^^^^^^^^^^^^^
All unit tests are executed and their coverage is measured when using `pytest <https://docs.pytest.org/>`_ (see ``setup.cfg`` for configuration details)::

    python -m pip install .[test]
    python -m pytest

The subset of the unit tests included in the module itself can be executed using `doctest <https://docs.python.org/3/library/doctest.html>`_::

    python bitlist/bitlist.py -v

Style conventions are enforced using `Pylint <https://www.pylint.org/>`_::

    python -m pip install .[lint]
    python -m pylint bitlist ./test/test_bitlist.py

Contributions
^^^^^^^^^^^^^
In order to contribute to the source code, open an issue or submit a pull request on the `GitHub page <https://github.com/lapets/bitlist>`_ for this library.

Versioning
^^^^^^^^^^
Beginning with version 0.3.0, the version number format for this library and the changes to the library associated with version number increments conform with `Semantic Versioning 2.0.0 <https://semver.org/#semantic-versioning-200>`_.

Publishing
^^^^^^^^^^
This library can be published as a `package on PyPI <https://pypi.org/project/bitlist>`__ by a package maintainer. First, install the dependencies required for packaging and publishing::

    python -m pip install .[publish]

Remove any old build/distribution files. Then, package the source into a distribution archive using the `wheel <https://pypi.org/project/wheel>`__ package::

    rm -rf dist *.egg-info
    python setup.py sdist bdist_wheel

Finally, upload the package distribution archive to `PyPI <https://pypi.org>`__ using the `twine <https://pypi.org/project/twine>`__ package::

    python -m twine upload dist/*
