# Blue Button 2.0 SDK - Python Version

## Introduction

Introduction goes here!

## Install Prerequisites:

- Install Python for your environment and verify the version with:

  ```
  $ python --version
  # or
  $ python3 --version
  ```

  This should output a 3.x version number.

- Install up to date versions of pip, setuptools and wheel:
  ```
  $ python3 -m pip install --upgrade pip setuptools wheel
  ```
- Optionally you can use a virtual environment for the previous insall step via the following:
  ```
  $ python -m venv bb2_env
  $ source bb2_env/bin/activate
  # Perform install and commands after sourcing the venv.
  ```

## Build

To build the cms_bluebutton package do the following:

- Build the package:

  ```
  # From repository root directory:
  $ python setup.py bdist_wheel
  ```

## Installation

To install the package locally do the following:

```
# From repository root directory:
$ pip install -e .
```

## Usage

Usage goes here!

## Developing the Blue Button 2.0 SDK (for BB2 team SDK developers)

### Install Development

To install with the tools you need to develop and run tests do the following:

From the repository base directory:

```
$ pip install -e .[dev]
```

To run the tests, use the following commands:

From the package base directory:

```
$ cd src/cms_bluebutton

$ # To run all tests:
$ pytest

$ # To run a specific test and show console debugging output:
$ pytest tests/test_fhir_request.py -s
```

To run the tests with coverage, use the following commands:

From the package base directory:

```
$ coverage run -m pytest

# Check report
$ coverage report -m
```

### Create Distribution

To create a distribution run the following command:

From the repository base directory:

```
$ python setup.py sdist
```

The resulting distribution files with be created in the `sdist/` directory.

### Create Manifest

Note that the previous distribution did not include the license.txt or test files. This requires creating a manifest.

To create a MANIFEST.in file run the following commands:

```
$ pip install check-manifest  # If not already installed.
$ check-manifest --create
$ python setup.py sdist
```