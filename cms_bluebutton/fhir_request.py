import requests
from requests.adapters import HTTPAdapter, Retry
from .auth import refresh_auth_token
from .constants import SDK_HEADERS


def fhir_request(bb, config):
    auth_token = config["auth_token"]
    new_auth_token = handle_expired(bb, auth_token)

    if new_auth_token is not None:
        auth_token = new_auth_token

    retry_config = Retry(
        total=bb.retry_config.get("total"),
        backoff_factor=bb.retry_config.get("backoff_factor"),
        status_forcelist=bb.retry_config.get("status_forcelist")
    )
    full_url = "{}/v{}/{}".format(bb.base_url, bb.version, config["url"])
    headers = SDK_HEADERS
    headers["Authorization"] = "Bearer " + auth_token.access_token
    adapter = HTTPAdapter(max_retries=retry_config)
    sesh = requests.Session()
    sesh.mount("https://", adapter)
    sesh.mount("http://", adapter)
    response = sesh.get(url=full_url, params=config["params"], headers=headers)

    return {"auth_token": new_auth_token, "response": response}


def handle_expired(bb, auth_token):
    if auth_token.access_token_expired():
        return refresh_auth_token(bb, auth_token)
    else:
        return None
