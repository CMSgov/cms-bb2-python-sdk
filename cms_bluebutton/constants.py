from .version import __version__ as sdk_version


SDK_HEADERS = {
    "X-BLUEBUTTON-SDK": "python",
    "X-BLUEBUTTON-SDK-VERSION": sdk_version
}

REFRESH_TOKEN_ENDPOINT = "/o/token/"

ENVIRONMENT_URLS = {
    "LOCAL": "http://localhost:8000",
    "TEST": "https://test.bluebutton.cms.gov",
    "SANDBOX": "https://sandbox.bluebutton.cms.gov",
    "PRODUCTION": "https://api.bluebutton.cms.gov",
}

# Supported FHIR resource paths
FHIR_RESOURCE_TYPE = {
    "Patient": "fhir/Patient/",
    "Coverage": "fhir/Coverage/",
    "Profile": "connect/userinfo",
    "ExplanationOfBenefit": "fhir/ExplanationOfBenefit/",
}
