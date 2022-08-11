import json
import datetime
import unittest
from os.path import abspath, curdir
from unittest import mock
from urllib.parse import urlparse, parse_qs

from cms_bluebutton import AuthorizationToken, BlueButton


MOCK_BB_CONFIG = {
    "environment": "SANDBOX",
    "client_id": "fake_client_id",
    "client_secret": "fake_client_secret",
    "callback_url": "https://www.fake-sandbox.com/your/callback/here",
    "version": "2",
}


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


class MockSessionSearchPage:
    def __init__(self, json_data, status_code):
        self.response = MockResponse(json_data, status_code)

    def mount(self, *args, **kwargs):
        return

    def get(self, *args, **kwargs):
        eob_url = kwargs['url']
        parsed_url = urlparse(eob_url)
        qps = parse_qs(parsed_url.query)
        if 'startIndex' in qps:
            pg_idx = int(qps["startIndex"][0]) // 10
            with open(abspath(curdir) + "/tests/fixtures/eobs/eob_p{}.json".format(pg_idx), "r") as f:
                return MockResponse(json.load(f), 200)
        else:
            # first page (bundle of eobs)
            with open(abspath(curdir) + "/tests/fixtures/eobs/eob_p0.json", "r") as f:
                return MockResponse(json.load(f), 200)


def success_fhir_patient_request_mock(*args, **kwargs):
    return MockSession({"resourceType": "Patient", "id": "-20140000010000"}, 200)


def success_fhir_coverage_request_mock(*args, **kwargs):
    return MockSession({"resourceType": "Bundle", "id": "aaa-111-111-111-aaaa"}, 200)


def success_fhir_eob_request_mock(*args, **kwargs):
    return MockSession({"resourceType": "Bundle", "id": "bbb-222-222-222-bbbb"}, 200)


def success_fhir_eob_pages_request_mock(*args, **kwargs):
    return MockSessionSearchPage({}, 200)


def success_fhir_profile_request_mock(*args, **kwargs):
    return MockSession({"sub": "-20140000010000", "patient": "-20140000010000"}, 200)


def error_fhir_request_mock(*args, **kwargs):
    return MockSession(None, 500)


def not_found_fhir_request_mock(*args, **kwargs):
    return MockSession(None, 404)


def generate_mock_config():
    return {
        "params": {},
        "auth_token": AuthorizationToken(
            {
                "access_token": "fake_access_token",
                "refresh_token": "fake_refresh_token",
                "expires_at": datetime.datetime.now(datetime.timezone.utc)
                + datetime.timedelta(seconds=36000),
                "patient": "-20140000010000",
            }
        ),
    }


class TestAPI(unittest.TestCase):
    @mock.patch("requests.Session", side_effect=success_fhir_patient_request_mock)
    def test_successful_fhir_patient_request(self, get_request_mock):
        bb = BlueButton(config=MOCK_BB_CONFIG)
        config = generate_mock_config()
        response = bb.get_patient_data(config)
        self.assertEqual(response["auth_token"], None)
        self.assertEqual(response["response"].status_code, 200)
        self.assertEqual(response["response"].json()["id"], "-20140000010000")
        self.assertEqual(response["response"].json()["resourceType"], "Patient")
        self.assertEqual(get_request_mock.call_count, 1)

    @mock.patch("requests.Session", side_effect=success_fhir_coverage_request_mock)
    def test_successful_fhir_coverage_request(self, get_request_mock):
        bb = BlueButton(config=MOCK_BB_CONFIG)
        config = generate_mock_config()
        response = bb.get_coverage_data(config)
        self.assertEqual(response["auth_token"], None)
        self.assertEqual(response["response"].status_code, 200)
        self.assertEqual(response["response"].json()["id"], "aaa-111-111-111-aaaa")
        self.assertEqual(response["response"].json()["resourceType"], "Bundle")
        self.assertEqual(get_request_mock.call_count, 1)

    @mock.patch("requests.Session", side_effect=success_fhir_eob_request_mock)
    def test_successful_fhir_eob_request(self, get_request_mock):
        bb = BlueButton(config=MOCK_BB_CONFIG)
        config = generate_mock_config()
        response = bb.get_explaination_of_benefit_data(config)
        self.assertEqual(response["auth_token"], None)
        self.assertEqual(response["response"].status_code, 200)
        self.assertEqual(response["response"].json()["id"], "bbb-222-222-222-bbbb")
        self.assertEqual(response["response"].json()["resourceType"], "Bundle")
        self.assertEqual(get_request_mock.call_count, 1)

    @mock.patch("requests.Session", side_effect=success_fhir_eob_pages_request_mock)
    def test_successful_fhir_eob_pages_request(self, get_request_mock):
        bb = BlueButton(config=MOCK_BB_CONFIG)
        config = generate_mock_config()
        response = bb.get_explaination_of_benefit_data(config)
        self.assertEqual(response["auth_token"], None)
        self.assertEqual(response["response"].status_code, 200)
        self.assertEqual(response["response"].json()["id"], "85a22239-fb03-43b1-a8ba-952dcea76004")
        self.assertEqual(response["response"].json()["resourceType"], "Bundle")
        self.assertEqual(get_request_mock.call_count, 1)
        # fetch all the pages given the 1st page
        pages = bb.get_pages(response['response'].json(), config)
        self.assertEqual(pages["auth_token"], None)
        self.assertEqual(len(pages["pages"]), 6)
        self.assertEqual(get_request_mock.call_count, 5)

    @mock.patch("requests.Session", side_effect=success_fhir_profile_request_mock)
    def test_successful_fhir_profile_request(self, get_request_mock):
        bb = BlueButton(config=MOCK_BB_CONFIG)
        config = generate_mock_config()
        response = bb.get_profile_data(config)
        self.assertEqual(response["auth_token"], None)
        self.assertEqual(response["response"].status_code, 200)
        self.assertEqual(response["response"].json()["sub"], "-20140000010000")
        self.assertEqual(response["response"].json()["patient"], "-20140000010000")
        self.assertEqual(get_request_mock.call_count, 1)

    @mock.patch("requests.Session", side_effect=success_fhir_coverage_request_mock)
    def test_successful_fhir_custom_request(self, get_request_mock):
        bb = BlueButton(config=MOCK_BB_CONFIG)
        config = generate_mock_config()
        config["url"] = "fhir/Coverage/part-a--20140000010000/"
        response = bb.get_custom_data(config)
        self.assertEqual(response["auth_token"], None)
        self.assertEqual(response["response"].status_code, 200)
        self.assertEqual(response["response"].json()["id"], "aaa-111-111-111-aaaa")
        self.assertEqual(response["response"].json()["resourceType"], "Bundle")
        self.assertEqual(get_request_mock.call_count, 1)

    @mock.patch("requests.Session", side_effect=error_fhir_request_mock)
    def test_500_error_fhir_request(self, get_request_mock):
        bb = BlueButton(config=MOCK_BB_CONFIG)
        config = generate_mock_config()
        response = bb.get_patient_data(config)
        self.assertEqual(response["auth_token"], None)
        self.assertEqual(response["response"].status_code, 500)
        self.assertEqual(get_request_mock.call_count, 1)

    @mock.patch("requests.Session", side_effect=not_found_fhir_request_mock)
    def test_not_found_fhir_request(self, get_request_mock):
        bb = BlueButton(config=MOCK_BB_CONFIG)
        config = generate_mock_config()
        response = bb.get_patient_data(config)
        self.assertEqual(response["auth_token"], None)
        self.assertEqual(response["response"].status_code, 404)
        self.assertEqual(get_request_mock.call_count, 1)
