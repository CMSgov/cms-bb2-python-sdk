import base64
import hashlib
import requests
import random
import string
import datetime
import urllib
from requests_toolbelt.multipart.encoder import MultipartEncoder

from .constants import SDK_HEADER, SDK_HEADER_KEY


class AuthorizationToken:
    def __init__(self, auth_token):
        self.access_token = auth_token.get("access_token")
        self.expires_in = auth_token.get("expires_in")
        self.expires_at = (
            auth_token.get("expires_at")
            if auth_token.get("expires_at")
            else datetime.datetime.now(datetime.timezone.utc)
            + datetime.timedelta(seconds=self.expires_in)
        )
        self.patient = auth_token.get("patient")
        self.refresh_token = auth_token.get("refresh_token")
        self.scope = auth_token.get("scope")
        self.token_type = auth_token.get("token_type")

    def access_token_expired(self):
        return self.expires_at < datetime.datetime.now(datetime.timezone.utc)


def refresh_auth_token(bb, auth_token):
    data = {
        "client_id": bb.client_id,
        "grant_type": "refresh_token",
        "refresh_token": auth_token.refresh_token,
    }

    headers = {
        SDK_HEADER_KEY: SDK_HEADER,
    }

    token_response = requests.post(
        url=bb.auth_token_url,
        data=data,
        headers=headers,
        auth=(bb.client_id, bb.client_secret),
    )

    token_response.raise_for_status()
    return AuthorizationToken(token_response.json())


def generate_authorize_url(bb, auth_data):
    params = {
        "client_id": bb.client_id,
        "redirect_uri": bb.callback_url,
        "state": auth_data["state"],
        "response_type": "code",
        "code_challenge_method": "S256",
        "code_challenge": auth_data["code_challenge"],
    }

    return (
        bb.auth_base_url
        + "?"
        + urllib.parse.urlencode(params, quote_via=urllib.parse.quote)
    )


def base64_url_encode(buffer):
    buffer_bytes = base64.urlsafe_b64encode(buffer.encode("utf-8"))
    buffer_result = str(buffer_bytes, "utf-8")
    return buffer_result


def get_random_string(length):
    letters = string.ascii_letters + string.digits + string.punctuation
    result = "".join(random.choice(letters) for i in range(length))
    return result


def generate_pkce_data():
    verifier = generate_random_state(32)
    code_challenge = base64.urlsafe_b64encode(
        hashlib.sha256(verifier.encode("ASCII")).digest()
    )
    return {"code_challenge": code_challenge.decode("utf-8"), "verifier": verifier}


def generate_random_state(num):
    return base64_url_encode(get_random_string(num))


def generate_auth_data():
    auth_data = {"state": generate_random_state(32)}
    auth_data.update(generate_pkce_data())
    return auth_data


def get_access_token_from_code(bb, auth_data, callback_code):
    data = {
        "client_id": bb.client_id,
        "client_secret": bb.client_secret,
        "code": callback_code,
        "grant_type": "authorization_code",
        "redirect_uri": bb.callback_url,
        "code_verifier": auth_data["verifier"],
        "code_challenge": auth_data["code_challenge"],
    }

    mp_encoder = MultipartEncoder(data)
    token_response = requests.post(
        url=bb.auth_token_url,
        data=mp_encoder,
        headers={"content-type": mp_encoder.content_type, SDK_HEADER_KEY: SDK_HEADER},
    )
    token_response.raise_for_status()
    token_dict = token_response.json()
    token_dict["expires_at"] = datetime.datetime.now(
        datetime.timezone.utc
    ) + datetime.timedelta(seconds=token_dict["expires_in"])

    return token_dict


def get_authorization_token(bb, auth_data, callback_code, callback_state):
    if callback_code is None:
        raise ValueError("Authorization code missing.")

    if callback_state is None:
        raise ValueError("Callback parameter 'state' missing.")

    if callback_state != auth_data["state"]:
        raise ValueError("Provided callback state does not match.")

    return AuthorizationToken(get_access_token_from_code(bb, auth_data, callback_code))
