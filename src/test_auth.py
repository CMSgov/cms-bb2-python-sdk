from auth import AuthRequest


def test_auth_url():
    authReq = AuthRequest()
    auth_url = authReq.get_authorize_url()
    print(auth_url)
    assert True