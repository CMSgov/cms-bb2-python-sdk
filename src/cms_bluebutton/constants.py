SDK_HEADER = "python"
SDK_HEADER_KEY = "X-BLUEBUTTON-SDK"

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
