# Blue Button API SDK (Python)

# Table of contents

1. [Descritpion](#description)
2. [Installation](#installation)
3. [Configuration](#configuration)
4. [Usages: Obtain Access Grant, Probe Scope, and Access Data](#usages)
5. [A Complete Sample App](#samples)
6. [API Versions and Environments](#versions_and_environments)

## Description <a name="description"></a>

This is an SDK for interacting with [CMS Blue Button 2.0 API](https://bluebutton.cms.gov/developers/),
the API allows applications to obtain a beneficiary's (who has login account with medicare.gov) grant
to access his/her medicare claims data - through OAUTH2 [(RFC 6749)](https://datatracker.ietf.org/doc/html/rfc6749) authorization flow.

By using the SDK, the development of applications accessing Blue Button 2.0 API can be greatly simplified.

Note, following the OAUTH2 best practices, OAUTH2 PKCE etension [(RFC 7636)](https://datatracker.ietf.org/doc/html/rfc7636) is always enabled.

## Installation <a name="installation"></a>

```bash
$ pip install cms-bluebutton-sdk
```

## Configuration <a name="configuration"></a>

the SDK needs to be properly configured to work, the parameters are:

- the app's credentials - client id, client secret
- the app's callback url
- the version number of the API
- the app's environment (web location where the app is registered)

the configuration is in json format and stored in a local file, the default location
is current working directory with file name: .bluebutton-config.json

A sample configuration json:

```
{
  "clientId": "foo",
  "clientSecret": "bar",
  "callbackUrl": "https://www.fake.com/",
}

```

| parameter    | value                   | Comments                        |
| ------------ | ----------------------- | ------------------------------- |
| clientId     | "foo"                   | oauth2 client id of the app     |
| clientSecret | "bar"                   | oauth2 client secret of the app |
| callbackUrl  | "https://www.fake.com/" | oauth2 callback url of the app  |

For application registration and client id and client secret, please refer to:
[Blue Button 2.0 API Docs - Try the API](https://bluebutton.cms.gov/developers/#try-the-api)

## Sample Usages: Obtain Access Grant, Probe Scope, and Access Data <a name="usages"></a>

Below are psuedo code snippets showing SDK used with python server and flask.

```

from flask import Flask
from flask import redirect, request
from cms_bluebutton import BlueButton, AuthorizationToken

# initialize the app
app = Flask(__name__)

bb = BlueButton()
# auth_data is saved for the current user
auth_data = bb.generate_auth_data()

# AuthorizationToken holds access grant info:
# access token, expire in, expire at, token type, scope, refreh token, etc.
# it is associated with current logged in user in real app,
# check SDK python docs for more details.

auth_token = None

# start authorize flow: response with URL to redirect to Medicare.gov beneficiary login
@app.route("/", methods=["GET"])
def get_auth_url():
    return bb.generate_authorize_url(auth_data)


@app.route('/api/bluebutton/callback/', methods=['GET'])
def authorization_callback():
    request_query = request.args
    code = request_query.get('code')
    state = request_query.get('state')

    auth_token = bb.get_authorization_token(auth_data, code, state)

    # now access token obtained, note, during authorization, the beneficiary can grant
    # access to his/her demographic data and claims data or only claims data, check the scope
    # of the current access token as shown below:

    scopes = auth_token.scope;

    # iterate scope entries here or check if a permission is in the scope
    if (scopes.index("patient/Patient.read") > -1) {
        // patient info access granted
    }

    # 1. access token scope where demagraphic info included:
    #
    # scope: [
    # "patient/Coverage.read",
    # "patient/ExplanationOfBenefit.read",
    # "patient/Patient.read",
    # "profile",
    # ]
    #
    # 2. access token scope where demagraphic info not included:
    #
    # scope: [
    # "patient/Coverage.read",
    # "patient/ExplanationOfBenefit.read",
    # ]

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

From two environments: PRODUCTION and SANDBOX, Blue Button API is available in v1 and v2, data served from v1 is in FHIR STU2 format, and data from v2 is in FHIR R4 format, an application's target environment and API version can be set in the SDK configuration as shown by example below:

```
{
  "clientId": "foo",
  "clientSecret": "bar",
  "callbackUrl": "https://www.fake.com/",
  "version": "2",
  "environment": "PRODUCTION"
}

```

The default API version is v2, and default environment is SANDBOX.

Web location of the environments:

[PRODUCTION Environment: https://api.bluebutton.cms.gov](https://api.bluebutton.cms.gov)

[SANDBOX Environment: https://sandbox.bluebutton.cms.gov](https://sandbox.bluebutton.cms.gov)
