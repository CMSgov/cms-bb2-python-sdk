SDK_VERSION = "1.0.0"

SDK_HEADERS = {
    "X-BLUEBUTTON-SDK": "python",
    "X-BLUEBUTTON-SDK-VERSION": SDK_VERSION
}

REFRESH_TOKEN_ENDPOINT = "/o/token/"

ENVIRONMENT_URLS = {
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
