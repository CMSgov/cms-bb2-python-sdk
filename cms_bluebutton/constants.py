SDK_VERSION = "0.1.0"

SDK_HEADERS = {
    "X-BLUEBUTTON-SDK": "python",
    "X-BLUEBUTTON-SDK-VERSION": SDK_VERSION
}

REFRESH_TOKEN_ENDPOINT = "/o/token/"

ENVIRONMENT_URLS = {
    "SANDBOX": "https://sandbox.bluebutton.cms.gov",
    "PRODUCTION": "https://api.bluebutton.cms.gov",
    "TEST": "https://test.bluebutton.cms.gov",
    "LOCAL": "http://localhost:8000",
}

# Supported FHIR resource paths
FHIR_RESOURCE_TYPE = {
    "Patient": "fhir/Patient/",
    "Coverage": "fhir/Coverage/",
    "Profile": "connect/userinfo",
    "ExplanationOfBenefit": "fhir/ExplanationOfBenefit/",
}
