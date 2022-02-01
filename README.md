Blue Button 2.0 SDK - Python Version
====================================

## Introduction

Introduction goes here!

## Install Prerequisites: 

* Install Python for your environment and verify the version with:
  ```
  python --version
  # or
  python3 --version
  ```
  This should output a 3.x version number.

* Install up to date versions of pip, setuptools and wheel:
  ```
  python3 -m pip install --upgrade pip setuptools wheel
  ```
* Optionally you can use a virtual environment for the previous insall step via the following:
  ```
  python -m venv bb2_env
  source bb2_env/bin/activate
  # Perform install and commands after sourcing the venv.
  ```

## Build

To build the cms-bb2 package do the following:

* Build the package:

  ```
  # From repository root directory:
  python setup.py bdist_wheel
  ```

## Installation

To install the package locally do the following:
```
# From repository root directory:
pip install -e .
```

## Usage

To test it out with Python interactively:
```
[cms-bb2-python-sdk]$ python
Python 3.10.1 ...
Type "help", "copyright", "credits" or "license" for more information.
>>> from bb2 import Bb2
>>> 
>>> a = Bb2()
>>> 
>>> a.hello()
Hello from BB2 SDK Class method!!!
>>> 
```