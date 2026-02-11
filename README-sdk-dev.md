# Blue Button 2.0 SDK Development Documentation

## Introduction

This README contains information related to developing the SDK.

It is intended for BB2 team members or others performing SDK development work.

## Install Prerequisites:

- Install Python for your environment and verify the version with:

  ```
  python --version
  # or
  python3 --version
  ```

  This should output a 3.x version number.

- You should use a virtual environment.

  - To create a virtual environment and activate it, use the following commands:

    ```
    python3 -m venv bb2_venv
    source bb2_venv/bin/activate
    # Perform install and commands after sourcing the venv.
    ```

- Install current versions of pip, setuptools, wheel and twine.

  ```
  # Update PIP
  pip install --upgrade pip

  # Update tools
  python3 -m pip install --upgrade pip setuptools wheel twine build
  ```

## Developing the Blue Button 2.0 SDK (for BB2 team SDK developers)

### Install Development

To install with the tools you need to develop and run tests do the following:

From the repository base directory:

```
pip install -e '.[dev]'
```

### Running tests

To run the tests, use the following commands:

From the package base directory:

```
cd cms_bluebutton

# To run all tests:
pytest

# To run a specific test and show console debugging output:
pytest tests/test_fhir_request.py -s
```

To run the tests with coverage, use the following commands:

From the package base directory:

```
coverage run -m pytest

# Check report
coverage report -m
```

## Packaging and Publishing

### Build Package

To build the cms_bluebutton package do the following:

- Build a wheel distribution package (.whl):

  ```
  # From repository root directory:
  rm -rf build/
  python -m build --wheel
  ```

The resulting distribution files with be created in the `dist/` directory.

- Review the files included with the following. Update the filename for the target version.

  ```
  unzip -l dist/cms_bluebutton_sdk-1.0.0-py3-none-any.whl 
  ```


### Install from a Package File

The package file can be installed via the following command:

```bash
pip install dist/cms_bluebutton_sdk-1.0.0-py3-none-any.whl # wheel
```


### Un-install from a Package File

The package can be un-installed via the following command:

```bash
pip uninstall cms_bluebutton_sdk
```


### Publish Testing using the TestPyPI registry instance

Before publishing to the main PyPI registry, testing can be perfomed using the TestPyPI site.

See the following for more details:  https://packaging.python.org/en/latest/guides/using-testpypi/

#### Prerequisite tasks:

- Create an OWNER type of account. This is the account that will own the `cms-bluebutton-sdk` project.

- Perform the initial release upload of the project using this account. See upload instruction below.

- BB2 developers who will be uploading releases need to create their own accounts.

- The OWNER account can setup the developers as MAINTAINERS on the project.

  - Maintainers will have the following role permissions for the project:

    Has permissions to Upload releases for a package. Can upload releases. Cannot invite collaborators. Cannot delete files, releases, or the project.


#### Upload project to TestPyPI

- In your user account settings, add an API token or use one that is already available to the team.

- Setup your configuration by adding the following lines to your $HOME/.pypirc file:

  ```
  [testpypi]
  username = __token__
  password = # either a user-scoped token or a project-scoped token you want to set as the default
  ```

- Source the virtual environment from previous instruction.

  ```bash
    source bb2_venv/bin/activate
  ```

- Upload to the TestPyPI registry with the following command for your intended version.

For example with target version = 1.0.0:

  ```bash
  twine upload --repository testpypi dist/cms_bluebutton_sdk-1.0.0-py3-none-any.whl
  ```

- Confirm the project was uploaded via the following URL: https://test.pypi.org/project/cms-bluebutton-sdk


#### Install test using TestPyPI

- Setup a temporary virtual environment to test the install.

  ```bash
  python3 -m venv /tmp/test_bb2_venv
  source /tmp/test_bb2_venv/bin/activate
  # Perform install and commands after sourcing the venv.
  ```

- Remove the package, if it is already installed.

    ```bash
    pip show cms-bluebutton-sdk
    pip uninstall cms-bluebutton-sdk

    ```

- Install `cms-bluebutton-sdk` from TestPyPI. Extras are installed from the main PyPI registry.

  ```bash
  pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ cms-bluebutton-sdk
  ```


- Show the installed package.

    ```bash
    pip show cms-bluebutton-sdk
    ```

- Test imports with the following.

```bash
cat <<EOF >test_bb2_sdk.py
from cms_bluebutton import BlueButton, AuthorizationToken
EOF
python test_bb2_sdk.py 
```

  - If successful, there will be no errors in the output.


### Publish to the main PyPI registry

After testing, the package / release can be published to the main PyPI site.

See the following for more details:  https://pypi.org/

#### Prerequisite tasks:

- Create an OWNER type of account. This is the account that will own the `cms-bluebutton-sdk` project.

- Perform the initial release upload of the project using this account. See upload instruction below.

- BB2 developers who will be uploading releases need to create their own accounts.

- The OWNER account can setup the developers as MAINTAINERS on the project.

  - Maintainers will have the following role permissions for the project:

    Has permissions to Upload releases for a package. Can upload releases. Cannot invite collaborators. Cannot delete files, releases, or the project.


#### Upload project to PyPI

- In your user account settings, add an API token or use one that is already available to the team.

- Setup your configuration by adding the following lines to your $HOME/.pypirc file:

  ```
  [pypi]
  username = __token__
  password = # either a user-scoped token or a project-scoped token you want to set as the default
  ```

- Source the virtual environment from previous instruction.

  ```bash
    source bb2_venv/bin/activate
  ```

- Upload to the PyPI registry with the following command. Update the filename for the target version.

  ```bash
  twine upload dist/cms_bluebutton_sdk-1.0.0-py3-none-any.whl
  ```

- Confirm the project was uploaded at the following URL: https://pypi.org/project/cms-bluebutton-sdk


#### Install test using PyPI

- Setup a temporary virtual environment to test the install.

  ```bash
  python3 -m venv /tmp/test_bb2_venv
  source /tmp/test_bb2_venv/bin/activate
  # Perform install and commands after sourcing the venv.
  ```

- Install `cms-bluebutton-sdk` from TestPyPI. Extras are installed from the main PyPI registry.

  ```bash
  pip install cms-bluebutton-sdk
  ```

- Show the installed package.

    ```bash
    pip show cms-bluebutton-sdk
    ```

- Test imports with the following.

```bash
cat <<EOF
from cms_bluebutton import BlueButton, AuthorizationToken
print("IMPORT TEST SUCCESSFUL!!!")
EOF
python test_bb2_sdk.py 
```

  - If successful, there will be no errors and the following message will output:

       IMPORT TEST SUCCESSFUL!!!

- Remove the test virtual environmnet to clean up.

  ```bash
  rm -rf /tmp/test_bb2_venv/
  ```

### Publishing NEW versions

New versions can be published using the previous build, TestPyPI and PyPI publishing instruction.

Before building and publishing a new version, the version number needs to be increased.

NOTE: Once a file is uploaded, it can not be replaced with a new file. A new version is needed per:  https://test.pypi.org/help/#file-name-reuse

To do this, edit the following line in the `./cms_bluebutton/version.py` file with the desired release version, e.g. the SDK version to be released is 1.0.0:

```
__version__ = "1.0.0",
```

### Testing Locally

The current method for seeing the SDK in action is fairly complex, as it requires also setting up the Python sample client (https://github.com/CMSgov/bluebutton-sample-client-python-react/tree/main). These both, of course, depend upon the web-server repo for most of their logic. It is possible that in order to fully understand an issue that arises within the SDK or the sample client, a developer would have to track changes across 3 separate projects. There should be some future work to simplify this process as it is very manual and laborious.

The steps listed here are listed elsewhere in the documentation but for the sake of convenience, they are partially repeated here
and written together so that a developer should be able to follow this step by step.

The overall goals are to:

  - Build a local version of the SDK
  - Run a local version of sample client that consumes a local version of the SDK

  ### Building a local version of the SDK

    Run the following commands in the base of this SDK repository. The commands suppose that you have the Python sample client cloned in the same folder as this SDK repo. Do not be in a virtualenv while running these commands.

    ```
      rm -rf build/
      python -m build --wheel --o ../bluebutton-sample-client-python-react/server
    ```

    The --o (or outdir) command should effectively 'copy paste' the built version of the .whl file into where it would be needed for the sample client. If you do not want it in the sample client, omit the --o and file path.

  ### Run a local version of sample client that consumes a local version of the SDK

    Ensure that in bluebutton-sample-client-python-react/server/Dockerfile, uncomment the following line. Replace the version number (1.0.4 in the example) of the .whl file with what has been generated from the previous build command.

    ```
      RUN pip install cms_bluebutton_sdk-1.0.4-py3-none-any.whl
    ```
    
    In bluebutton-sample-client-python-react/server/Pipfile, add this line:

    ```
      cms-bluebutton-sdk = {file = "./cms_bluebutton_sdk-1.0.4-py3-none-any.whl"}
    ```

    In the base repository of bluebutton-sample-client-python-react, run the following commands. Ensure that you have no currently running containers or images of the sample client.

    ```
      cd server
      unzip -l cms_bluebutton_sdk-1.0.4-py3-none-any.whl
      pip install cms_bluebutton_sdk-1.0.4-py3-none-any.whl
      docker compose up
    ```

  Each time a change is made in the SDK, you must repeat all of the previous steps of building and re-running a local sample client. You must also ensure that the containers and images are removed each time.