from setuptools import setup

with open("README.rst", "r") as fh:
    long_description = fh.read()

setup(
    name="bitlist",
    version="0.1.0.3",
    packages=["bitlist",],
    install_requires=[],
    license="MIT",
    url="https://github.com/lapets/bitlist",
    author="Andrei Lapets",
    author_email="a@lapets.io",
    description="Minimal Python library for working with "+\
                "little-endian list representation of bit strings.",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    test_suite="nose.collector",
    tests_require=["nose"],
)
