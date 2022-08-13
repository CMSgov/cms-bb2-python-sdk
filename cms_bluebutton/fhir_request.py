import requests
from requests.adapters import HTTPAdapter, Retry
from .auth import refresh_auth_token
from .constants import SDK_HEADERS


def fhir_request(bb, config):
    auth_token = config["auth_token"]
    if bb.token_refresh_on_expire:
        auth_token = handle_expired(bb, auth_token)

    url_param = config["url"]
    full_url = None

    if url_param.startswith(bb.base_url):
        # allow full url passed in from config as long as it roots from base url
        full_url = url_param
    else:
        full_url = "{}/v{}/{}".format(bb.base_url, bb.version, config["url"])

    headers = SDK_HEADERS
    headers["Authorization"] = "Bearer " + auth_token.access_token

    adapter = HTTPAdapter()

    if bb.retry_config.get("total") > 0:
        adapter = HTTPAdapter(max_retries=Retry(
            total=bb.retry_config.get("total"),
            backoff_factor=bb.retry_config.get("backoff_factor"),
            status_forcelist=bb.retry_config.get("status_forcelist")
        ))

    sesh = requests.Session()
    sesh.mount("https://", adapter)
    sesh.mount("http://", adapter)
    response = sesh.get(url=full_url, params=config["params"], headers=headers)

    return {"auth_token": auth_token, "response": response}


def handle_expired(bb, auth_token):
    return refresh_auth_token(bb, auth_token) if auth_token.access_token_expired() else auth_token
