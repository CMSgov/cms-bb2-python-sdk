import pytest
import requests_mock
from urllib.parse import urlparse, parse_qs

from cms_bluebutton import BlueButton
from .fixtures.token_response import TOKEN_RESPONSE, REFRESH_TOKEN_RESPONSE


BB2_CONFIG_V1 = {
    "base_url": "https://sandbox.bluebutton.cms.gov",
    "client_id": "foo",
    "client_secret": "bar",
    "callback_url": "https://www.fake.com/",
    "version": "1",
    "environment": "PRODUCTION",
}

BB2_CONFIG_V2 = {
    "base_url": "https://sandbox.bluebutton.cms.gov",
    "client_id": "foo",
    "client_secret": "bar",
    "callback_url": "https://www.fake.com/",
    "version": "2",
    "environment": "PRODUCTION",
}


def test_auth_url_v1():
    bb = BlueButton(BB2_CONFIG_V1)

    auth_data = bb.generate_auth_data()
    auth_url = bb.generate_authorize_url(auth_data)

    assert auth_url is not None
    parsed_url = urlparse(auth_url)
    assert parsed_url.path == "/v1/o/authorize"
    qps = parse_qs(parsed_url.query)
    assert bb.client_id in qps["client_id"]
    assert auth_data["state"] in qps["state"]
    assert auth_data["code_challenge"] in qps["code_challenge"]


def test_auth_url_v2():
    bb = BlueButton(BB2_CONFIG_V2)

    auth_data = bb.generate_auth_data()
    auth_url = bb.generate_authorize_url(auth_data)

    assert auth_url is not None
    parsed_url = urlparse(auth_url)
    assert parsed_url.path == "/v2/o/authorize"
    qps = parse_qs(parsed_url.query)
    assert bb.client_id in qps["client_id"]
    assert auth_data["state"] in qps["state"]
    assert auth_data.get("code_challenge") is not None
    assert qps.get("code_challenge")


def test_get_authorization_token_missing_code():
    with pytest.raises(ValueError) as err:
        bb = BlueButton(BB2_CONFIG_V2)
        auth_data = bb.generate_auth_data()
        bb.get_authorization_token(auth_data, None, auth_data.get("state"))
    assert err is not None
    assert "Authorization code missing." in str(err)


def test_get_authorization_token_missing_state():
    with pytest.raises(ValueError) as err:
        bb = BlueButton(BB2_CONFIG_V2)
        auth_data = bb.generate_auth_data()
        bb.get_authorization_token(auth_data, "code-xxx", None)
    assert err is not None
    assert "Callback parameter 'state' missing." in str(err)


def test_get_authorization_token_bad_state():
    with pytest.raises(ValueError) as err:
        bb = BlueButton(BB2_CONFIG_V2)
        auth_data = bb.generate_auth_data()
        bb.get_authorization_token(auth_data, "code-xxx", "bad-state")
    assert err is not None
    assert "Provided callback state does not match." in str(err)


def test_get_authorization_token_callback():
    bb = BlueButton(BB2_CONFIG_V2)
    auth_data = bb.generate_auth_data()

    with requests_mock.Mocker() as mock:
        mock.post(bb.auth_token_url, json=TOKEN_RESPONSE)
        auth_token = bb.get_authorization_token(
            auth_data, "code-xxx", auth_data.get("state")
        )

        assert auth_token is not None
        assert auth_token.access_token == TOKEN_RESPONSE.get("access_token")
        assert auth_token.refresh_token == TOKEN_RESPONSE.get("refresh_token")
        assert auth_token.patient == TOKEN_RESPONSE.get("patient")
        assert auth_token.expires_in == TOKEN_RESPONSE.get("expires_in")
        assert not auth_token.access_token_expired()


def test_refresh_access_token_without_refreshtoken():
    bb = BlueButton(BB2_CONFIG_V1)
    auth_data = bb.generate_auth_data()

    with requests_mock.Mocker() as mock:
        mock.post(bb.auth_token_url, json=TOKEN_RESPONSE)
        auth_token = bb.get_authorization_token(
            auth_data, "code-xxx", auth_data.get("state")
        )

        assert auth_token is not None
        assert auth_token.access_token == TOKEN_RESPONSE.get("access_token")
        assert auth_token.refresh_token == TOKEN_RESPONSE.get("refresh_token")
        assert auth_token.patient == TOKEN_RESPONSE.get("patient")
        assert auth_token.expires_in == TOKEN_RESPONSE.get("expires_in")


def test_refresh_access_token():
    bb = BlueButton(BB2_CONFIG_V1)
    auth_data = bb.generate_auth_data()

    with requests_mock.Mocker() as mock:
        mock.post(bb.auth_token_url, json=TOKEN_RESPONSE)
        auth_token = bb.get_authorization_token(
            auth_data, "code-xxx", auth_data.get("state")
        )

        assert auth_token is not None
        assert auth_token.access_token == TOKEN_RESPONSE.get("access_token")
        assert auth_token.refresh_token == TOKEN_RESPONSE.get("refresh_token")
        assert auth_token.patient == TOKEN_RESPONSE.get("patient")
        assert auth_token.expires_in == TOKEN_RESPONSE.get("expires_in")
    with requests_mock.Mocker() as mock2:
        mock2.post(bb.auth_token_url, json=REFRESH_TOKEN_RESPONSE)
        auth_token_new = bb.refresh_auth_token(auth_token)

        assert auth_token_new is not None
        assert auth_token_new.access_token == REFRESH_TOKEN_RESPONSE.get("access_token")
        assert auth_token_new.refresh_token == REFRESH_TOKEN_RESPONSE.get(
            "refresh_token"
        )
        assert auth_token_new.patient == REFRESH_TOKEN_RESPONSE.get("patient")
        assert auth_token_new.expires_in == REFRESH_TOKEN_RESPONSE.get("expires_in")
        assert auth_token.access_token != auth_token_new.access_token
        assert auth_token.refresh_token != auth_token_new.refresh_token
