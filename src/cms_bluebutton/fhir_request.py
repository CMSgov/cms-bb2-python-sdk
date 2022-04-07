import requests
from requests.adapters import HTTPAdapter, Retry

from .constants import SDK_HEADER, SDK_HEADER_KEY


def fhir_request(bb, config):
    auth_token = config["auth_token"]
    new_auth_token = handle_expired(bb, auth_token)

    if new_auth_token is not None:
        auth_token = new_auth_token

    retry_config = Retry(
        total=3, backoff_factor=5, status_forcelist=[500, 502, 503, 504]
    )
    full_url = bb.base_url + "/v" + bb.version + "/" + config["url"]
    headers = {
        "Authorization": "Bearer " + auth_token.access_token,
        SDK_HEADER_KEY: SDK_HEADER,
    }
    adapter = HTTPAdapter(max_retries=retry_config)
    sesh = requests.Session()
    sesh.mount("https://", adapter)
    sesh.mount("http://", adapter)
    response = sesh.get(url=full_url, params=config["params"], headers=headers)

    return {"auth_token": new_auth_token, "response": response}


def handle_expired(bb, auth_token):
    if auth_token.access_token_expired():
        return bb.refresh_auth_token(bb, auth_token)
    else:
        return None
