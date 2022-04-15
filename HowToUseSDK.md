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

Below are psuedo code snippets showing SDK used with node express server.

```

import express, { Request, Response } from 'express';

const app = express();

const bb = new BlueButton();
const authData = bb.generateAuthData();

// AuthorizationToken holds access grant info:
// access token, expire in, expire at, token type, scope, refreh token, etc.
// it is associated with current logged in user in real app,
// check SDK js docs for more details.

let authToken: AuthorizationToken;

// start authorize flow: response with URL to redirect to Medicare.gov beneficiary login
app.get('/', (req, res) => {
    const redirectUrl = bb.generateAuthorizeUrl(authData);
    res.redirect(redirectUrl);
})

// oauth2 call back: obtain access token, optionally check scope, and fetch data
app.get('api/bluebutton/callback', async (req: Request, res: Response) => {

  let results = {};
    try {
        authToken = await bb.getAuthorizationToken(authData, req.query.code, req.query.state, req.query.error);
        // now access token obtained, note, during authorization, the beneficiary can grant
        // access to his/her demographic data and claims data or only claims data, check the scope
        // of the current access token as shown below:
        const scopes: string[] = authToken.scope;
        // iterate scope entries here or check if a permission is in the scope
        if (authToken.scope.index("patient/Patient.read") > -1) {
            // patient info access granted
        }

        /**
        * 1. access token scope where demagraphic info included:
        *
        * scope: [
        * "patient/Coverage.read",
        * "patient/ExplanationOfBenefit.read",
        * "patient/Patient.read",
        * "profile",
        * ]
        *
        * 2. access token scope where demagraphic info not included:
        *
        * scope: [
        * "patient/Coverage.read",
        * "patient/ExplanationOfBenefit.read",
        * ]
        */

        // data flow: after access granted
        // the app logic can fetch the beneficiary's data in app specific ways:
        // e.g. download EOB periodically etc.
        // access token can expire, SDK automatically refresh access token when that happens.
        eobResults = await bb.getExplanationOfBenefitData(authToken);
        patientResults = await bb.getPatientData(authToken);
        coverageResults = await bb.getCoverageData(authToken);
        profileResults = await bb.getProfileData(authToken);

        results = {
            eob: eobResults.response.data,
            patient: patientResults.response.data,
            coverage: coverageResults.response.data,
            profile: profileResults.response.data
        }

        authToken = profileResults.token;

    } catch (e) {
        console.log(e);
    }

    res.json(results)

});

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
