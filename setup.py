from setuptools import setup, find_packages

setup(
    name="CifTools",
    version="0.2.0",
    url="https://github.com/molstar/ciftools-python",
    author="Ravi Jose Tristao Ramos, David Sehnal",
    author_email="souoravi@gmail.com, david.sehnal@gmail.com",
    description="A library for handling (Binary)CIF files.",
    packages=find_packages(exclude=['tests']),
    install_requires=["numpy >= 1.11.1", "msgpack >= 1.0.3", "numba >= 0.56.2"],
)
