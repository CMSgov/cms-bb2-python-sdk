import datetime
import unittest
from unittest import mock
from fhirRequest import fhirRequest


class MockResponse:
    def __init__(self, json_data, status_code):
        self.json_data = json_data
        self.status_code = status_code

    def json(self):
        return self.json_data


class MockSession:
    def __init__(self, json_data, status_code):
        self.response = MockResponse(json_data, status_code)

    def mount(self, *args, **kwargs):
        return

    def get(self, *args, **kwargs):
        return self.response


def success_fhir_request_mock(*args, **kwargs):
    return MockSession({"resourceType": "Patient", "id": "-20140000010000"}, 200)


def error_fhir_request_mock(*args, **kwargs):
    return MockSession(None, 500)


def not_found_fhir_request_mock(*args, **kwargs):
    return MockSession(None, 404)


def generate_mock_bb():
    return {
        "base_url": "https://sandbox.bluebutton.cms.gov",
        "client_id": "fake_client_id",
        "client_secret": "fake_client_secret",
        "version": "2",
    }


def generate_mock_config():
    return {
        "url": "/fhir/Patient/-20140000010000",
        "params": {},
        "auth_token": {
            "access_token": "fake_access_token",
            "refresh_token": "fake_refresh_token",
            "expires_at": datetime.datetime.now() + datetime.timedelta(seconds=36000),
            "patient": "-20140000010000",
        },
    }


class TestAPI(unittest.TestCase):
    @mock.patch("requests.Session", side_effect=success_fhir_request_mock)
    def test_successful_fhir_request(self, get_request_mock):
        bb = generate_mock_bb()
        config = generate_mock_config()
        response = fhirRequest(bb, config)
        self.assertEqual(response["auth_token"], None)
        self.assertEqual(response["response"].status_code, 200)
        self.assertEqual(response["response"].json()["id"], "-20140000010000")
        self.assertEqual(get_request_mock.call_count, 1)

    @mock.patch("requests.Session", side_effect=error_fhir_request_mock)
    def test_500_error_fhir_request(self, get_request_mock):
        bb = generate_mock_bb()
        config = generate_mock_config()
        response = fhirRequest(bb, config)
        self.assertEqual(response["auth_token"], None)
        self.assertEqual(response["response"].status_code, 500)
        self.assertEqual(get_request_mock.call_count, 1)

    @mock.patch("requests.Session", side_effect=not_found_fhir_request_mock)
    def test_not_found_fhir_request(self, get_request_mock):
        bb = generate_mock_bb()
        config = generate_mock_config()
        response = fhirRequest(bb, config)
        self.assertEqual(response["auth_token"], None)
        self.assertEqual(response["response"].status_code, 404)
        self.assertEqual(get_request_mock.call_count, 1)
