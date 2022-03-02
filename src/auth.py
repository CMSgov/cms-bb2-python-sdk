import base64
import hashlib
import requests
import secrets
import random
import string

from datetime import datetime, timezone
from requests_toolbelt import MultipartEncoder

from bb2 import BB2_CONFIG

BB2_AUTH_URL = "{}/v{}/o/authorize".format(BB2_CONFIG['baseUrl'], BB2_CONFIG['version'])
BB2_TOKEN_URL = "{}/v{}/o/token".format(BB2_CONFIG['baseUrl'], BB2_CONFIG['version'])
AUTH_URL_TEMPLATE = "{}?client_id=${}&redirect_uri={}&state=${}&response_type=code&{}"

class AuthRequest:
    def __init__(self):
        self.auth_data = self._generate_authdata()
        self.auth_url = self._generate_authorize_url()
        self.auth_token = None

    def get_authorize_url(self):
        return self.auth_url

    def authorize_callback(self, code, state):
        if code is None:
            raise ValueError("Authorization code missing.")

        if state is None:
            raise ValueError("Callback parameter 'state' missing.")

        if state != self.auth_data['state']:
            raise ValueError("Provided callback state does not match.")

        self.auth_token = AuthorizationToken(self._get_access_token(code, state))

    def access_token_expired(self):
        return self.auth_token.access_token_expired()

    def refresh_access_token(self):
        return self.auth_token.refresh_access_token()

    def _generate_authorize_url(self):
        pkce_params = "code_challenge_method=S256&code_challenge={}".format(self.auth_data['code_challenge'])
        return AUTH_URL_TEMPLATE.format(BB2_AUTH_URL, BB2_CONFIG['clientId'],
                                    BB2_CONFIG['callbackUrl'],
                                    self.auth_data['state'],
                                    pkce_params)

    def _base64_url_encode(self, buffer):
        buffer_bytes = base64.urlsafe_b64encode(buffer.encode("utf-8"))
        buffer_result = str(buffer_bytes, "utf-8")
        return buffer_result

    def _get_random_string(self, length):
        letters = string.ascii_letters + string.digits + string.punctuation
        result = ''.join(random.choice(letters) for i in range(length))
        return result

    def _generate_pkce_data(self):
        verifier = self._generate_random_state(32)
        code_challenge = base64.urlsafe_b64encode(hashlib.sha256(verifier.encode('ASCII')).digest())
        return {'code_challenge' : code_challenge.decode('utf-8'), 'verifier' : verifier}

    def _generate_random_state(self, num):
        return self._base64_url_encode(self._get_random_string(num))

    def _generate_authdata(self):
        auth_data = {"state": self._generate_random_state(32)}
        auth_data.update(self._generate_pkce_data())
        print(auth_data)
        return auth_data
 
    def _get_access_token(self, code, state):
        params = {'client_id': BB2_CONFIG['clientId'],
                  'client_secret': BB2_CONFIG['clientSecret'],
                  'code':code,
                  'grant_type':'authorization_code',
                  'redirect_uri': BB2_CONFIG['callbackUrl']}
        if (BB2_CONFIG['pkce']):
            params['code_verifier'] = self.auth_data['verifier']
            params['code_challenge'] = self.auth_data['code_challenge']
    
        mp_encoder = MultipartEncoder(params)
        token_response = requests.post(url=BB2_TOKEN_URL, data=mp_encoder, headers={'content-type':mp_encoder.content_type})
        if token_response.status_code == 200:
            token_json = token_response.json()
            token_json['expires_at'] = datetime.datetime.now() + datetime.timedelta(seconds=token_json['expires_in'])
        else:
            raise Exception("Failed to get access token, status_code: {}, error: {}".format(token_response.status_code, token_response.content))
        return token_json

class AuthorizationToken:

    def __init__(self, auth_token):
        self.access_token = auth_token.get('access_token')
        self.expires_in = auth_token.get('expires_in')
        self.expires_at = auth_token.get('expires_at') if auth_token.get('expires_at') else datetime.datetime.now(timezone.utc) + datetime.timedelta(seconds=self.expires_in)
        self.patient = auth_token.get('patient')
        self.refresh_token = auth_token.get('refresh_token')
        self.scope = auth_token.get('scope')
        self.token_type = auth_token.get('token_type')

    def refresh_access_token(self):

        if self.refresh_token is None:
            raise ValueError("Refresh token not available when calling refresh_access_token().")

        params = {
            'client_id': BB2_CONFIG['clientId'],
            'grant_type': 'refresh_token',
            'refresh_token': self.refresh_token
        }

        token_response = requests.post(url=BB2_TOKEN_URL, params=params, auth=(BB2_CONFIG.get('clientId'), BB2_CONFIG.get('clientSecret')))

        if token_response.status_code == 200:
            token_json = token_response.json()
            token_json['expires_at'] = datetime.datetime.now() + datetime.timedelta(seconds=token_json['expires_in'])
        else:
            raise Exception("Failed to refresh access token, status_code: {}, error: {}".format(token_response.status_code, token_response.content))

        return token_json

    def access_token_expired(self):
        return self.expires_at < datetime.now(timezone.utc)
