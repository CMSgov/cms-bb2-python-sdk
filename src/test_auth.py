import pytest
import requests_mock

from urllib.parse import urlparse, parse_qs
from auth import AuthRequest
from bb2 import Bb2
from fixtures.token_response import TOKEN_RESPONSE, REFRESH_TOKEN_RESPONSE

BB2_CONFIG_V1 = {
    "base_url": "https://sandbox.bluebutton.cms.gov",
    "client_id": "foo",
    "client_secret": "bar",
    "callback_url": "https://www.fake.com/",
    "version": "1",
    "environment": "PRODUCTION"
}

BB2_CONFIG_V2 = {
    "base_url": "https://sandbox.bluebutton.cms.gov",
    "client_id": "foo",
    "client_secret": "bar",
    "callback_url": "https://www.fake.com/",
    "version": "2",
    "environment": "PRODUCTION"
}


def test_auth_url_v1():
    bb = Bb2(BB2_CONFIG_V1)
    auth_req = AuthRequest(bb)

    auth_url = auth_req.get_authorize_url()
    assert auth_url is not None
    parsed_url = urlparse(auth_url)
    assert parsed_url.path == "/v1/o/authorize"
    qps = parse_qs(parsed_url.query)
    assert bb.get_config()['client_id'] in qps['client_id']
    assert auth_req.auth_data['state'] in qps['state']
    assert auth_req.auth_data['code_challenge'] in qps['code_challenge']


def test_auth_url_v2():
    bb = Bb2(BB2_CONFIG_V2)
    auth_req = AuthRequest(bb)

    auth_url = auth_req.get_authorize_url()
    assert auth_url is not None
    parsed_url = urlparse(auth_url)
    assert parsed_url.path == "/v2/o/authorize"
    qps = parse_qs(parsed_url.query)
    assert bb.get_config()['client_id'] in qps['client_id']
    assert auth_req.auth_data['state'] in qps['state']
    assert auth_req.auth_data.get('code_challenge') is not None
    assert qps.get('code_challenge')


def test_authorize_callback_missing_ac():
    with pytest.raises(ValueError) as err:
        bb = Bb2(BB2_CONFIG_V2)
        auth_req = AuthRequest(bb)
        auth_req.authorize_callback(None, auth_req.auth_data.get("state"))
    assert err is not None
    assert "Authorization code missing." in str(err)


def test_authorize_callback_missing_state():
    with pytest.raises(ValueError) as err:
        bb = Bb2(BB2_CONFIG_V2)
        auth_req = AuthRequest(bb)
        auth_req.authorize_callback("ac", None)
    assert err is not None
    assert "Callback parameter 'state' missing." in str(err)


def test_authorize_callback_badstate():
    with pytest.raises(ValueError) as err:
        bb = Bb2(BB2_CONFIG_V2)
        auth_req = AuthRequest(bb)
        auth_req.authorize_callback("ac", "bad-state")
    assert err is not None
    assert "Provided callback state does not match." in str(err)


def test_authorize_callback():
    bb = Bb2(BB2_CONFIG_V2)
    auth_req = AuthRequest(bb)
    with requests_mock.Mocker() as mock:
        mock.post(auth_req.auth_token_url, json=TOKEN_RESPONSE)
        auth_req.authorize_callback("authcode", auth_req.auth_data.get("state"))
        assert auth_req.auth_token is not None
        assert auth_req.auth_token.access_token == TOKEN_RESPONSE.get("access_token")
        assert auth_req.auth_token.refresh_token == TOKEN_RESPONSE.get("refresh_token")
        assert auth_req.auth_token.patient == TOKEN_RESPONSE.get("patient")
        assert auth_req.auth_token.expires_in == TOKEN_RESPONSE.get("expires_in")
        assert not auth_req.access_token_expired()


def test_refresh_access_token_without_refreshtoken():
    bb = Bb2(BB2_CONFIG_V1)
    auth_req = AuthRequest(bb)
    with requests_mock.Mocker() as mock:
        mock.post(auth_req.auth_token_url, json=TOKEN_RESPONSE)
        auth_req.authorize_callback("authcode", auth_req.auth_data.get("state"))
        assert auth_req.auth_token is not None
        assert auth_req.auth_token.access_token == TOKEN_RESPONSE.get("access_token")
        assert auth_req.auth_token.refresh_token == TOKEN_RESPONSE.get("refresh_token")
        assert auth_req.auth_token.patient == TOKEN_RESPONSE.get("patient")
        assert auth_req.auth_token.expires_in == TOKEN_RESPONSE.get("expires_in")

        with pytest.raises(ValueError) as err:
            auth_req.auth_token.refresh_token = None
            auth_req.refresh_access_token()

        assert err is not None
        assert "Refresh token not available when calling refresh_access_token()." in str(err)


def test_refresh_access_token():
    bb = Bb2(BB2_CONFIG_V1)
    auth_req = AuthRequest(bb)
    with requests_mock.Mocker() as mock:
        mock.post(auth_req.auth_token_url, json=TOKEN_RESPONSE)
        auth_req.authorize_callback("authcode", auth_req.auth_data.get("state"))
        assert auth_req.auth_token is not None
        assert auth_req.auth_token.access_token == TOKEN_RESPONSE.get("access_token")
        assert auth_req.auth_token.refresh_token == TOKEN_RESPONSE.get("refresh_token")
        assert auth_req.auth_token.patient == TOKEN_RESPONSE.get("patient")
        assert auth_req.auth_token.expires_in == TOKEN_RESPONSE.get("expires_in")
    with requests_mock.Mocker() as mock2:
        mock2.post(auth_req.auth_token_url, json=REFRESH_TOKEN_RESPONSE)
        auth_req.refresh_access_token()
        assert auth_req.auth_token is not None
        assert auth_req.auth_token.access_token == REFRESH_TOKEN_RESPONSE.get("access_token")
        assert auth_req.auth_token.refresh_token == REFRESH_TOKEN_RESPONSE.get("refresh_token")
        assert auth_req.auth_token.patient == REFRESH_TOKEN_RESPONSE.get("patient")
        assert auth_req.auth_token.expires_in == REFRESH_TOKEN_RESPONSE.get("expires_in")
