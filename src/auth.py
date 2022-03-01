import base64
import hashlib
import requests
import secrets

from datetime import datetime, timezone
from bb2 import Bb2, BB2_CONFIG
from typing import NamedTuple

BB2_AUTH_URL = "{}/v{}/o/authorize".format(BB2_CONFIG['base_url'], BB2_CONFIG['version'])
BB2_TOKEN_URL = "{}/v{}/o/token".format(BB2_CONFIG['base_url'], BB2_CONFIG['version'])
AUTH_URL_TEMPLATE = "{}?client_id=${}&redirect_uri={}&state=${}&response_type=code&{}"

class AuthData(NamedTuple):
  code_challenge: str
  verifier: str
  state: str


class TokenPostData(NamedTuple):
  client_id: str
  client_secret: str
  code: str
  grant_type: str
  redirect_uri: str
  code_verifier: str
  code_challenge: str


class PkceData(NamedTuple):
  code_challenge: str
  verifier: str


class AuthorizationToken:

    def __init__(self, auth_token):
        self.access_token = auth_token.get('access_token')
        self.expires_in = auth_token.get('expires_in')
        self.expires_at = auth_token.get('expires_at') if auth_token.get('expires_at') else datetime.datetime.now(timezone.utc) + datetime.timedelta(seconds=self.expires_in)
        self.patient = auth_token.get('patient')
        self.refresh_token = auth_token.get('refresh_token')
        self.scope = auth_token.get('scope')
        self.token_type = auth_token.get('token_type')
        self.auth_data = self._generate_authdata()

    def generate_authorize_url(self) -> str:
        pkce_params = "code_challenge_method=S256&code_challenge={}".format(self.auth_data.code_challenge)
        return AUTH_URL_TEMPLATE.format(BB2_AUTH_URL, BB2_CONFIG['clientId'],
                                    BB2_CONFIG['callbackUrl'],
                                    self.auth_data.state,
                                    pkce_params)

    def authorize_callback(self, code, state):

        if code is None:
            raise ValueError("Authorization code missing.")

        if state is None:
            raise ValueError("Callback parameter 'state' missing.")

        if state != self.auth_data.state:
            raise ValueError("Provided callback state does not match.")

        access_token = self.get_access_token(code, state)


    def refresh_accesstoken(self):

        if self.refresh_token is None:
            raise ValueError("Refresh token not available when calling refresh_accesstoken().")

        PARAMS = {
            'client_id': BB2_CONFIG['clientId'],
            'grant_type': 'refresh_token',
            'refresh_token': self.refresh_token
        }

        my_response = requests.post(url=BB2_TOKEN_URL, params=PARAMS, auth=(BB2_CONFIG.get('clientId'), BB2_CONFIG.get('clientSecret')))
        response_json = my_response.json()
        response_json['expires_at'] = datetime.datetime.now() + datetime.timedelta(seconds=response_json['expires_in'])
        return response_json

    def access_token_expired(self) -> bool:
        return self.expires_at < datetime.now(timezone.utc)

    def _sha256(self, str_val: str):
        return hashlib.sha256(str_val).encode('utf-8').hexdigest()

    def _base64_url_encode(self, bytes) -> str:
        buffer = base64.urlsafe_b64encode(bytes.encode("utf-8"))
        return str(buffer, "utf-8")

    def _generate_pkce_data(self) -> PkceData:
        verifier = self._base64_url_encode(secrets.token_bytes(32))
        code_challenge = self._base64_url_encode(self._sha256(verifier))
        return PkceData(code_challenge, verifier)

    def _generate_random_state(self):
        return self._base64_url_encode(secrets.token_bytes(32))

    def _generate_authdata(self) -> AuthData:
        pkce_data = self._generate_pkce_data()
        return AuthData(pkce_data.code_challenge, pkce_data.verifier, self._generate_random_state())
 
    def _generate_token_post_data(self, 
                              auth_data: AuthData,
                              code: str,
                              callback_state: str):

        return TokenPostData(
            BB2_CONFIG['clientId'],
            BB2_CONFIG['clientSecret'],
            code,
            "authorization_code",
            BB2_CONFIG['callBackUrl'],
            auth_data.verifier,
            auth_data.codeChallenge)

    def _get_access_token(self, code, state):
        PARAMS = {'client_id': BB2_CONFIG['clientId'],
                  'client_secret': BB2_CONFIG['clientSecret'],
                  'code':code,
                  'grant_type':'authorization_code',
                  'redirect_uri': BB2_CONFIG['callbackUrl']}
        if (BB2_CONFIG['pkce'] and state is not None):
            code_chall = DBcodeChallenges[state]
            PARAMS['code_verifier'] = code_chall.get('verifier')
            PARAMS['code_challenge'] = code_chall.get('codeChallenge')
    
        mp_encoder = MultipartEncoder(PARAMS)
        my_response = requests.post(url=BB2_ACCESS_TOKEN_URL, data=mp_encoder, headers={'content-type':mp_encoder.content_type})
        response_json = my_response.json()
        response_json['expires_at'] = datetime.datetime.now() + datetime.timedelta(seconds=response_json['expires_in'])
        return response_json
