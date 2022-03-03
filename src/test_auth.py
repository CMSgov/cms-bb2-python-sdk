import pytest
import requests_mock

from urllib.parse import urlparse, parse_qs
from auth import AuthRequest
from bb2 import Bb2
from fixtures.token_response import TOKEN_RESPONSE, REFRESH_TOKEN_RESPONSE

BB2_CONFIG_PKCE_V1 = {
    "baseUrl": "https://sandbox.bluebutton.cms.gov",
    "clientId": "foo",
    "clientSecret": "bar",
    "callbackUrl": "https://www.fake.com/",
    "version": "1",
    "pkce": True,
    "environment": "PRODUCTION"
}

BB2_CONFIG_NO_PKCE_V2 = {
    "baseUrl": "https://sandbox.bluebutton.cms.gov",
    "clientId": "foo",
    "clientSecret": "bar",
    "callbackUrl": "https://www.fake.com/",
    "version": "2",
    "pkce": False,
    "environment": "PRODUCTION"
}


def test_auth_url_w_pkce():
    bb = Bb2(BB2_CONFIG_PKCE_V1)
    authReq = AuthRequest(bb)

    auth_url = authReq.get_authorize_url()
    assert auth_url is not None
    parsed_url = urlparse(auth_url)
    assert parsed_url.path == "/v1/o/authorize"
    qps = parse_qs(parsed_url.query)
    assert bb.get_config()['clientId'] in qps['client_id']
    assert authReq.auth_data['state'] in qps['state']
    assert authReq.auth_data['code_challenge'] in qps['code_challenge']


def test_auth_url_no_pkce():
    bb = Bb2(BB2_CONFIG_NO_PKCE_V2)
    authReq = AuthRequest(bb)

    auth_url = authReq.get_authorize_url()
    assert auth_url is not None
    parsed_url = urlparse(auth_url)
    assert parsed_url.path == "/v2/o/authorize"
    qps = parse_qs(parsed_url.query)
    assert bb.get_config()['clientId'] in qps['client_id']
    assert authReq.auth_data['state'] in qps['state']
    assert authReq.auth_data.get('code_challenge') is None
    assert not qps.get('code_challenge')


def test_authorize_callback_missing_ac():
    with pytest.raises(ValueError) as err:
        bb = Bb2(BB2_CONFIG_NO_PKCE_V2)
        authReq = AuthRequest(bb)
        authReq.authorize_callback(None, authReq.auth_data.get("state"))
    assert err is not None
    assert "Authorization code missing." in str(err)


def test_authorize_callback_missing_state():
    with pytest.raises(ValueError) as err:
        bb = Bb2(BB2_CONFIG_NO_PKCE_V2)
        authReq = AuthRequest(bb)
        authReq.authorize_callback("ac", None)
    assert err is not None
    assert "Callback parameter 'state' missing." in str(err)


def test_authorize_callback_badstate():
    with pytest.raises(ValueError) as err:
        bb = Bb2(BB2_CONFIG_NO_PKCE_V2)
        authReq = AuthRequest(bb)
        authReq.authorize_callback("ac", "bad-state")
    assert err is not None
    assert "Provided callback state does not match." in str(err)


def test_authorize_callback():
    bb = Bb2(BB2_CONFIG_NO_PKCE_V2)
    authReq = AuthRequest(bb)
    with requests_mock.Mocker() as mock:
        mock.post(authReq.auth_token_url, json=TOKEN_RESPONSE)
        authReq.authorize_callback("authcode", authReq.auth_data.get("state"))
        assert authReq.auth_token is not None
        assert authReq.auth_token.access_token == TOKEN_RESPONSE.get("access_token")
        assert authReq.auth_token.refresh_token == TOKEN_RESPONSE.get("refresh_token")
        assert authReq.auth_token.patient == TOKEN_RESPONSE.get("patient")
        assert authReq.auth_token.expires_in == TOKEN_RESPONSE.get("expires_in")
        assert not authReq.access_token_expired()


def test_refresh_access_token_without_refreshtoken():
    bb = Bb2(BB2_CONFIG_PKCE_V1)
    authReq = AuthRequest(bb)
    with requests_mock.Mocker() as mock:
        mock.post(authReq.auth_token_url, json=TOKEN_RESPONSE)
        authReq.authorize_callback("authcode", authReq.auth_data.get("state"))
        assert authReq.auth_token is not None
        assert authReq.auth_token.access_token == TOKEN_RESPONSE.get("access_token")
        assert authReq.auth_token.refresh_token == TOKEN_RESPONSE.get("refresh_token")
        assert authReq.auth_token.patient == TOKEN_RESPONSE.get("patient")
        assert authReq.auth_token.expires_in == TOKEN_RESPONSE.get("expires_in")

        with pytest.raises(ValueError) as err:
            authReq.auth_token.refresh_token = None
            authReq.refresh_access_token()

        assert err is not None
        assert "Refresh token not available when calling refresh_access_token()." in str(err)


def test_refresh_access_token():
    bb = Bb2(BB2_CONFIG_PKCE_V1)
    authReq = AuthRequest(bb)
    with requests_mock.Mocker() as mock:
        mock.post(authReq.auth_token_url, json=TOKEN_RESPONSE)
        authReq.authorize_callback("authcode", authReq.auth_data.get("state"))
        assert authReq.auth_token is not None
        assert authReq.auth_token.access_token == TOKEN_RESPONSE.get("access_token")
        assert authReq.auth_token.refresh_token == TOKEN_RESPONSE.get("refresh_token")
        assert authReq.auth_token.patient == TOKEN_RESPONSE.get("patient")
        assert authReq.auth_token.expires_in == TOKEN_RESPONSE.get("expires_in")
    with requests_mock.Mocker() as mock2:
        mock2.post(authReq.auth_token_url, json=REFRESH_TOKEN_RESPONSE)
        authReq.refresh_access_token()
        assert authReq.auth_token is not None
        assert authReq.auth_token.access_token == REFRESH_TOKEN_RESPONSE.get("access_token")
        assert authReq.auth_token.refresh_token == REFRESH_TOKEN_RESPONSE.get("refresh_token")
        assert authReq.auth_token.patient == REFRESH_TOKEN_RESPONSE.get("patient")
        assert authReq.auth_token.expires_in == REFRESH_TOKEN_RESPONSE.get("expires_in")
