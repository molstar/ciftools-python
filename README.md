[![License](http://img.shields.io/badge/license-MIT-blue.svg?style=flat)](./LICENSE)

# CIFTools Python

A library for reading and writing (Binary)CIF files in Python.

## Linting

```
autoflake --remove-all-unused-imports --remove-unused-variables --ignore-init-module-imports -ir ciftools && isort . && black .
```