# Blue Button 2.0 SDK Development Documentation

## Introduction

This README contains information related to developing the SDK.

It is intended for BB2 team members or others performing SDK development work.

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
## Installation

To install the package file do the following:

```
# From repository root directory:
$ pip install <package file name>
```


## Developing the Blue Button 2.0 SDK (for BB2 team SDK developers)

### Install Development

To install with the tools you need to develop and run tests do the following:

From the repository base directory:

```
$ pip install -e .[dev]
```

### Running tests

To run the tests, use the following commands:

From the package base directory:

```
$ cd cms_bluebutton

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

## Packaging and Publishing


### Create or Update Manifest

If check-manifest is not yet installed run the following:

```
$ pip install check-manifest  # If not already installed.
```

If MANIFEST.in does not yet exist, run the following to create it:

```
$ check-manifest --create
```

To help with updating MANIFEST.in run the following to get information:

```
$ check-manifest
# This creates the following directory: cms_bluebutton.egg-info
```

### Build Packages

To build the cms_bluebutton packages do the following:

- Build a wheel distribution package (.whl):

  ```
  # From repository root directory:
  $ rm -rf build/
  $ python setup.py bdist_wheel
  ```

- Build a distribution package (.tar.gz):

  ```
  # From repository root directory:
  $ rm -rf build/
  $ python setup.py sdist
  ```

- Build a source package:

  ```
  # From repository root directory:
  $ rm -rf build/
  $ python setup.py sdist
  ```

The resulting distribution files with be created in the `dist/` directory.

### Install from a Package File

Package files can be installed via the following commands:

```bash
pip install cms_bluebutton-0.1.0-py3-none-any.whl # wheel
```
or 

```bash
pip install cms_bluebutton-0.1.0.tar.gz # bdist
```

### Publishing

TODO!
