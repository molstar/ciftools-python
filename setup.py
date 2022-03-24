from setuptools import setup, find_packages

setup(
    name='CifTools',
    version='0.1.0',
    url='https://github.com/molstar/ciftools-python',
    author='Ravi Ramos',
    author_email='souoravi@gmail.com',
    description='A library for handling CIF and BinaryCIF files.',
    packages=find_packages(),    
    install_requires=['numpy >= 1.11.1', 'msgpack >= 1.0.3'],
)