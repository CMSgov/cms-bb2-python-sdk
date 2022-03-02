from urllib.parse import urlparse, parse_qs
from auth import AuthRequest
from bb2 import Bb2


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