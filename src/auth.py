import base64
import hashlib
import requests
import random
import string
import datetime
import urllib

from requests_toolbelt.multipart.encoder import MultipartEncoder

from cms_bluebutton import BlueButton

BB2_AUTH_URL = "{}/v{}/o/authorize"
BB2_TOKEN_URL = "{}/v{}/o/token/"


class AuthRequest:

    def __init__(self, bb: BlueButton):
        self.bb = bb
        self.auth_base_url = BB2_AUTH_URL.format(bb.base_url, bb.version)
        self.auth_token_url = BB2_TOKEN_URL.format(bb.base_url, bb.version)
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

        self.auth_token = AuthorizationToken(self._get_access_token(code))

        return self.auth_token

    def access_token_expired(self):
        return self.auth_token.access_token_expired()

    def refresh_access_token(self):

        params = {
            'client_id': self.bb.client_id,
            'grant_type': 'refresh_token',
            'refresh_token': self.auth_token.refresh_token
        }

        token_response = requests.post(url=self.auth_token_url,
                                       params=params,
                                       auth=(self.bb.client_id,
                                             self.bb.client_secret))

        token_response.raise_for_status()
        self.auth_token = AuthorizationToken(token_response.json())

        return self.auth_token

    def _generate_authorize_url(self):
        params = {'client_id': self.bb.client_id,
                  'redirect_uri': self.bb.client_secret,
                  'state': self.auth_data['state'],
                  'response_type': 'code',
                  'code_challenge_method': 'S256',
                  'code_challenge': self.auth_data['code_challenge']}

        return self.auth_base_url + '?' + urllib.parse.urlencode(params, quote_via=urllib.parse.quote)

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
        return {'code_challenge': code_challenge.decode('utf-8'), 'verifier': verifier}

    def _generate_random_state(self, num):
        return self._base64_url_encode(self._get_random_string(num))

    def _generate_authdata(self):
        auth_data = {"state": self._generate_random_state(32)}
        auth_data.update(self._generate_pkce_data())
        return auth_data

    def _get_access_token(self, code):
        params = {'client_id': self.bb.client_id,
                  'client_secret': self.bb.client_secret,
                  'code': code,
                  'grant_type': 'authorization_code',
                  'redirect_uri': self.bb.callback_url,
                  'code_verifier': self.auth_data['verifier'],
                  'code_challenge': self.auth_data['code_challenge']}

        mp_encoder = MultipartEncoder(params)
        token_response = requests.post(url=self.auth_token_url, data=mp_encoder,
                                       headers={'content-type': mp_encoder.content_type})
        token_response.raise_for_status()
        token_json = token_response.json()
        token_json['expires_at'] = datetime.datetime.now(datetime.timezone.utc) + \
            datetime.timedelta(seconds=token_json['expires_in'])

        return token_json


class AuthorizationToken:

    def __init__(self, auth_token):
        self.access_token = auth_token.get('access_token')
        self.expires_in = auth_token.get('expires_in')
        self.expires_at = auth_token.get('expires_at') if auth_token.get('expires_at') else \
            datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(seconds=self.expires_in)
        self.patient = auth_token.get('patient')
        self.refresh_token = auth_token.get('refresh_token')
        self.scope = auth_token.get('scope')
        self.token_type = auth_token.get('token_type')

    def access_token_expired(self):
        return self.expires_at < datetime.datetime.now(datetime.timezone.utc)
