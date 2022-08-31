# Python SDK for Blue Button 2.0 API
This Python software development kit (SDK) provides tools and resources for developers integrating with the [CMS Blue Button 2.0 (BB2.0) API](https://bluebutton.cms.gov/developers/).


# Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration Parameters](#configuration-parameters)
- [Configuration Methods](#configuration-methods)
- [Usage](#usage)
- [Sample App](#sample-app)
- [SDK Development](#sdk_devel)
- [About](#about)
- [License](#license)
- [Help and Support](#help)


## Prerequisites <a name="prerequisites"></a>

You'll need a sandbox account and sample access token to access data from the Blue Button 2.0 API.

To learn how to create a sandbox account and generate a sample access token, see **[Try the API](https://bluebutton.cms.gov/developers/#try-the-api)**.


## Installation <a name="installation"></a>

```bash
pip install cms-bluebutton-sdk
```

## Configuration Parameters<a name="configuration-parameters"></a>

Required SDK configuration parameters include:

| Parameter     | Value                           | Default |Description                                |
| ------------- | ------------------------------- |----| --------------------------------------- |
| `environment` | `SANDBOX` or `PRODUCTION`     |`SANDBOX` | Blue Button 2.0 API environment |
| `version`       | `1` or `2`                        | `2`  | Blue Button 2.0 version            |
| `client_id`    | *`your_client_id`*                          | |OAuth2.0 client ID of your app             |
| `client_secret` | *`your_client_secret`*                           | |OAuth2.0 client secret of your app         |
| `callback_url`  | *`https://www.example.com/callback`* | |OAuth2.0 callback URL of your app          |


### Access Token Refresh on Expire
SDK FHIR requests check whether the access token is expired before the data end point call. By default, if the access token is expired, the token in the current token object refreshes. Disable token refresh by setting `token_refresh_on_expire` to `false`. 

### FHIR Requests Retry Settings

Retry is enabled by default for FHIR requests. The folllowing parameters are available for the exponential back off retry algorithm.

| Retry parameter   | Value (default)      | Description                         |
| ----------------- | -------------------- | -------------------------------- |
| `backoff_factor`    | `5`                    | Backoff factor in seconds       |
| `total `            | `3`                    | Max retries                      |
| `status_forcelist`  | [`500`, `502`, `503`, `504`] | Error response codes to retry on |

The exponential backoff factor (in seconds) is used to calculate interval between retries using the formula `backoff_factor * (2 ** (i - 1))` where `i` starts from 0.

Example:

A `backoff_factor` of 5 seconds generates the wait intervals: 2.5, 5, 10, ...

To disable the retry, set `total = 0`

### Environments and Data

The Blue Button 2.0 API is available in V1 and V2 in a sandbox and production environment.

- Sandbox location: https://sandbox.bluebutton.cms.gov
- Production location: https://api.bluebutton.cms.gov

Version data formats:

- V1: FHIR STU2
- V2: FHIR R4

Sample configuration JSON with default version and environment:

```
{
  "client_id": "your_client_id",
  "client_secret": "your_client_secret",
  "callback_url": "https://www.example.com/",
}

```

If needed, you can set your application's target environment and API version.

Example:

```
{
  "client_id": "your_client_id",
  "client_secret": "your_client_secret",
  "callback_url": "https://www.example.com/",
  "version": "2",
  "environment": "PRODUCTION"
}

```

## Configuration Methods<a name="configuration-methods"></a>
There are three ways to configure the SDK when instantiating a `BlueButton` class instance.

### Python Dictionary
    - A dictionary of configuration key:value pairs can be used.
    - Configuration values can be provided from your own application's configuration method.
    - Example code:
      ```python
      bb = BlueButton({
               "environment": "PRODUCTION",
               "client_id": "your_client_id",
               "client_secret": "your_client_secret",
               "callback_url": "https://www.example.com/callback",
               "version": 2,
               "retry_settings": {
                   "total": 3,
                   "backoff_factor": 5,
                   "status_forcelist": [500, 502, 503, 504]
               }
            }
      ```
### JSON config file
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
          "client_id": "your_client_id",
          "client_secret": "your_client_secret",
          "callback_url": "https://www.example.com/callback",
          "version": 2,
          "retry_settings": {
              "total": 3,
              "backoff_factor": 5,
              "status_forcelist": [500, 502, 503, 504]
          }
      }
      ```

### YAML config file
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
      client_id: "id"
      client_secret: "your_client_secret"
      callback_url: "https://www.example.com/callback"
      version: 2
      ```

## Sample Usage: Obtain Access Grant, Probe Scope, and Access Data <a name="usages"></a>

Below are code snippets showing the SDK used with Python server and Flask.

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
    scopes = auth_token.scope

    # iterate scope entries here or check if a permission is in the scope
    if "patient/Patient.read" in scopes: 
        # patient info access granted

    """
    1. access token scope where demographic info included:
    
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
        eob_data = eob_data['response'].json()
        result['eob_data'] = eob_data

        # A FHIR search response can result in a large number of resources. 
        # For example, an EOB search of a beneficiary could return hundreds 
        # of resources. By default, search results are grouped into
        # pages with 10 resources each. For example, 
        # bb.get_explaination_of_benefit_data(config) returns the
        # first page of resources as a FHIR bundle with a link section 
        # of page navigation URLs. Pagination link names include 
        # 'first,' 'last,' 'self,' next,' and 'previous.' 
        # To get all the pages, use bb.get_pages(data, config).
        
        eob_pages = bb.get_pages(eob_data, config)
        result['eob_pages'] = eob_pages['pages']
        auth_token = eob_pages['auth_token']

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

## Sample App <a name="samples"></a>

For a complete Python React sample app, see [CMS Blue Button Python Sample App](https://github.com/CMSgov/bluebutton-sample-client-python-react).


## SDK Development <a name="sdk_devel"></a>

Documentation for BlueButton 2.0 team members and others developing the SDK can be found at [README-sdk-dev.md](./README-sdk-dev.md).

## About the Blue Button 2.0 API <a name="about"></a>

The [Blue Button 2.0 API](https://bluebutton.cms.gov/) provides Medicare enrollee claims data to applications using the [OAuth2.0 authorization flow](https://datatracker.ietf.org/doc/html/rfc6749). We aim to provide a developer-friendly, standards-based API that enables people with Medicare to connect their claims data to the applications, services, and research programs they trust.

## License<a name="license"></a>
The CMS Blue Button 2.0 Python SDK is licensed under the Creative Commons Zero v1.0 Universal. For more details, see [License](https://github.com/CMSgov/cms-bb2-python-sdk/blob/main/LICENSE).

*Note: We do our best to keep our SDKs up to date with vulnerability patching and security testing, but you are responsible for your own review and testing before implementation.*

## Help and Support <a name="help"></a>

Got questions? Need help troubleshooting? Want to propose a new feature? Contact the Blue Button 2.0 team and connect with the community in our [Google Group](https://groups.google.com/forum/#!forum/Developer-group-for-cms-blue-button-api).
