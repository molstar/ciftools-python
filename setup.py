from setuptools import setup, find_packages

setup(
    name="CifTools",
    version="0.1.2",
    url="https://github.com/molstar/ciftools-python",
    author="Ravi Jose Tristao Ramos",
    author_email="souoravi@gmail.com",
    description="A library for handling (Binary)CIF files.",
    packages=find_packages(exclude=['tests']),
    install_requires=["numpy >= 1.11.1", "msgpack >= 1.0.3"],
)
