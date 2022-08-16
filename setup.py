from setuptools import find_packages, setup

setup(
    name="CifTools",
    version="0.1.2",
    url="https://github.com/molstar/ciftools-python",
    author="Ravi Jose Tristao Ramos",
    author_email="souoravi@gmail.com",
    description="A library for handling (Binary)CIF files.",
    packages=["ciftools"],
    install_requires=["numpy >= 1.11.1", "msgpack >= 1.0.3", "requests >= 2.27.1", "pydantic >= 1.9.0"],
)
