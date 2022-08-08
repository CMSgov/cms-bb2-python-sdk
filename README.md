# Blue Button API SDK (Python)

# Table of contents

1. [Descritpion](#description)
2. [Installation](#installation)
3. [Configuration](#configuration)
4. [Usages: Obtain Access Grant, Probe Scope, and Access Data](#usages)
5. [A Complete Sample App](#samples)
6. [API Versions and Environments](#versions_and_environments)
7. [SDK Development](#sdk_devel)

## Description <a name="description"></a>

This is an SDK for interacting with the [CMS Blue Button 2.0 API](https://bluebutton.cms.gov/developers/).
The API allows applications to obtain a beneficiary's (who has login account with medicare.gov) grant
to access their medicare claims data - through the OAuth 2.0 [(RFC 6749)](https://datatracker.ietf.org/doc/html/rfc6749) authorization flow.

By using the SDK, the development of applications accessing the Blue Button 2.0 API can be greatly simplified.

Note: In following OAuth 2.0 best practices, the PKCE extension [(RFC 7636)](https://datatracker.ietf.org/doc/html/rfc7636) is always enabled.

## Installation <a name="installation"></a>

```bash
$ pip install cms-bluebutton-sdk
```

## Configuration <a name="configuration"></a>

The SDK needs to be properly configured to work.

The configuration parameters are:

- The app's credentials - client id, client secret
- The app's callback url
- The version number of the API
- The app's environment (the BB2.0 web location where the app is registered)
- The FHIR call retry settings

| Parameter    | Value                   | Comments                        |
| ------------ | ----------------------- | ------------------------------- |
| environment     | "SANDBOX" or "PRODUCTION"                   | BB2 API environment (default="SANDBOX")
| version  | 1 or 2 | BB2 API version (default=2)  |
| client_id     | "foo"                   | oauth2 client id of the app     |
| client_secret | "bar"                   | oauth2 client secret of the app |
| callback_url  | "https://www.fake.com/callback" | oauth2 callback URL of the app  |

For application registration and client id and client secret, please refer to:
[Blue Button 2.0 API Docs - Try the API](https://bluebutton.cms.gov/developers/#try-the-api)

FHIR requests retry:

Retry is enabled by default for FHIR requests, retry_settings: parameters for exponential back off retry algorithm

| retry parameter   | value (default)      | Comments                         |
| ----------------- | -------------------- | -------------------------------- |
| backoff_factor    | 5                    | back off factor in seconds       |
| total             | 3                    | max retries                      |
| status_forcelist  | [500, 502, 503, 504] | error response codes to retry on |

the exponential back off factor (in seconds) is used to calculate interval between retries by below formular, where i starts from 0:

backoff factor * (2 ** (i - 1))

e.g. for backoff_factor is 5 seconds, it will generate wait intervals: 2.5, 5, 10, ...

to disable the retry: set total = 0

There are three ways to configure the SDK when instantiating a `BlueButton` class instance:

  * Python Dictionary:
    - A dictionary of configuration key:value pairs can be used.
    - Configuration values can be provided from your own application's configuration method.
    - Example code:
      ```python
      bb = BlueButton({
               "environment": "PRODUCTION",
               "client_id": "foo",
               "client_secret": "bar",
               "callback_url": "https://www.fake.com/callback",
               "version": 2,
               "retry_settings": {
                   "total": 3,
                   "backoff_factor": 5,
                   "status_forcelist": [500, 502, 503, 504]
               }
            }
      ```
  * JSON config file:
    - This is using a configuration file that is in a JSON format.
    - This is stored in a local file.
    - The default location is in the current working directory with a file name: .bluebutton-config.json
    - Example code:
      ```python
      bb = BlueButton("settings/my_bb2_sdk_conf.json")
      ```
    - Example JSON in file:
      ```json
      {
          "environment": "SANDBOX",
          "client_id": "foo",
          "client_secret": "bar",
          "callback_url": "https://www.fake.com/callback",
          "version": 2,
          "retry_settings": {
              "total": 3,
              "backoff_factor": 5,
              "status_forcelist": [500, 502, 503, 504]
          }
      }
      ```

  * YAML config file:
    - This is using a configuration file that is in a YAML format.
    - This is stored in a local file.
    - The default location is in the current working directory with a file name: .bluebutton-config.yaml
    - Example code:
      ```python
      bb = BlueButton("settings/my_bb2_sdk_conf.yaml")
      ```
    - Example YAML in file:
      ```yaml
      environment: "SANDBOX"
      client_id: "foo"
      client_secret: "bar"
      callback_url: "https://www.fake.com/callback"
      version: 2
      ```

## Sample Usage: Obtain Access Grant, Probe Scope, and Access Data <a name="usages"></a>

Below are psuedo code snippets showing SDK used with python server and flask.

```python
from flask import Flask
from flask import redirect, request
from cms_bluebutton import BlueButton, AuthorizationToken

# initialize the app
app = Flask(__name__)

# Instantiate SDK class instance via conf in file
bb = BlueButton()

# auth_data is saved for the current user
auth_data = bb.generate_auth_data()

"""
AuthorizationToken holds access grant info:
  access token, expire in, expire at, token type, scope, refreh token, etc.
It is associated with current logged in user in real app.
Check SDK python docs for more details.
"""

auth_token = None

# Start authorize flow: Response with URL to redirect to Medicare.gov beneficiary login
@app.route("/", methods=["GET"])
def get_auth_url():
    return bb.generate_authorize_url(auth_data)


@app.route('/api/bluebutton/callback/', methods=['GET'])
def authorization_callback():
    request_query = request.args
    code = request_query.get('code')
    state = request_query.get('state')

    auth_token = bb.get_authorization_token(auth_data, code, state)

    """
    Now access token obtained.

    Note: During authorization, the beneficiary can grant
    access to their demographic data and claims data or only claims data.

    Check the scope
    of the current access token as shown below:
    """
    scopes = auth_token.scope;

    # iterate scope entries here or check if a permission is in the scope
    if "patient/Patient.read" in scopes: 
        # patient info access granted

    """
    1. access token scope where demagraphic info included:
    
    scope: [
       "patient/Coverage.read",
       "patient/ExplanationOfBenefit.read",
       "patient/Patient.read",
       "profile",
    ]
    
    2. access token scope where demagraphic info not included:
    
    scope: [
        "patient/Coverage.read",
        "patient/ExplanationOfBenefit.read",
    ]
    """
    config = {
        "auth_token": auth_token,
        "params": {},
        "url": "to be overriden"
    }

    result = {}

    # fetch eob, patient, coverage, profile
    try:
        eob_data = bb.get_explaination_of_benefit_data(config)
        result['eob_data'] = eob_data['response'].json()

        pt_data = bb.get_patient_data(config)
        result['patient_data'] = pt_data['response'].json()

        coverage_data = bb.get_coverage_data(config)
        result['coverage_data'] = coverage_data['response'].json()

        profile_data = bb.get_profile_data(config)
        result['profile_data'] = profile_data['response'].json()
    except Exception as ex:
        print(ex)

    return result


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=3001)
```

## A Complete Sample App <a name="samples"></a>

A Python React sample app can be found at:
[CMS Blue Button Python Sample App](https://github.com/CMSgov/bluebutton-sample-client-python-react)

## API Versions and Environments <a name="versions_and_environments"></a>

Can be selected for environments: PRODUCTION and SANDBOX.

The Blue Button API is available in versions v1 and v2.

The data served from v1 is in FHIR STU2 format, and data from v2 is in FHIR R4 format.

An application's target environment and API version can be set in the SDK configuration as shown by the JSON example below:

```json
{
  "clientId": "foo",
  "clientSecret": "bar",
  "callbackUrl": "https://www.fake.com/",
  "version": "2",
  "environment": "PRODUCTION"
}
```

If not included, the default API version is v2, and the default environment is SANDBOX.

Web location of the environments:

[PRODUCTION Environment: https://api.bluebutton.cms.gov](https://api.bluebutton.cms.gov)

[SANDBOX Environment: https://sandbox.bluebutton.cms.gov](https://sandbox.bluebutton.cms.gov)

## SDK Development <a name="sdk_devel"></a>

Documentation for BB2 team members and others developing the SDK can be found here:  [README-sdk-dev.md](./README-sdk-dev.md)
