import datetime
from constants import REFRESH_TOKEN_ENDPOINT, SDK_HEADER, SDK_HEADER_KEY
import requests
from requests.adapters import HTTPAdapter, Retry


def fhirRequest(bb, config):
    auth_token = config.auth_token
    new_auth_token = handle_expired(bb, auth_token, config.refresh_token)

    if new_auth_token is not None:
        auth_token = new_auth_token

    retry_config = Retry(
        total=3, backoff_factor=0.2, status_forcelist=[500, 502, 503, 504]
    )
    full_url = bb.base_url + "/v" + bb.version + config.url
    headers = {
        "Authorization": "Bearer " + auth_token.access_token,
        [SDK_HEADER_KEY]: SDK_HEADER,
    }
    adapter = HTTPAdapter(max_retries=retry_config)
    sesh = requests.Session()
    sesh.mount("https://", adapter)
    sesh.mount("http://", adapter)
    response = sesh.get(url=full_url, params=config.params, headers=headers)

    return {"auth_token": new_auth_token, "response": response}


def handle_expired(bb, auth_token):
    if datetime.datetime.now() > auth_token.expires_at:
        return refresh_access_token(bb, auth_token.refresh_token)

    return None


def refresh_access_token(bb, refresh_token):
    full_url = bb.base_url + "/v" + bb.version + REFRESH_TOKEN_ENDPOINT

    params = {
        "client_id": bb.client_id,
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
    }

    my_response = requests.post(
        url=full_url, params=params, auth=(bb.client_id, bb.client_secret)
    )
    response_json = my_response.json()
    response_json["expires_at"] = datetime.datetime.now() + datetime.timedelta(
        seconds=response_json["expires_in"]
    )
    return response_json
