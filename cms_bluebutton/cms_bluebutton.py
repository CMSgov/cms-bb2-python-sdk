"""
Blue Button 2.0 SDK Class

"""
import json
import os
import pathlib
import yaml

from .auth import (
    generate_auth_data,
    generate_authorize_url,
    get_authorization_token,
    refresh_auth_token,
)
from .constants import ENVIRONMENT_URLS, FHIR_RESOURCE_TYPE
from .fhir_request import fhir_request


ROOT_DIR = os.path.abspath(os.curdir) + "/"
DEFAULT_CONFIG_FILE_LOCATION = ROOT_DIR + "./.bluebutton-config.json"


class BlueButton:

    def __init__(self, config=DEFAULT_CONFIG_FILE_LOCATION):
        self.client_id = None
        self.client_secret = None
        self.callback_url = None
        self.version = 2  # Default to BB2 version 2

        self.base_url = None

        self.set_configuration(config)

    def _read_json(self, file_path):
        with open(file_path, "r") as f:
            data = json.load(f)
            return data

    def _read_yaml(self, file_path):
        with open(file_path, "r") as f:
            return yaml.safe_load(f)

    def _read_config(self, config):
        extension = pathlib.Path(config).suffix

        if extension == ".json":
            return self._read_json(config)
        elif extension == ".yaml":
            return self._read_yaml(config)
        else:
            raise ValueError(
                "Error: Configuration file extension must be .json"
                " or .yaml for: {}".format(config)
            )

    def set_configuration(self, config):
        # Is config param a file path or dict?
        if isinstance(config, str):
            config_dict = self._read_config(config)
        else:
            config_dict = config

        # Check environment setting
        env = config_dict.get("environment", None)
        if env in ["SANDBOX", "PRODUCTION"]:
            self.base_url = ENVIRONMENT_URLS.get(env, None)
        else:
            raise ValueError(
                "Error: Configuration environment must be set to"
                " SANDBOX or PRODUCTION in: {}".format(config)
            )

        # Check other settings are provided
        for s in ["client_id", "client_secret", "callback_url"]:
            setting = config_dict.get(s, None)
            if setting is None:
                raise ValueError(
                    'Error: Configuration setting "'
                    + s
                    + '" is missing in: {}'.format(config)
                )

        self.client_id = config_dict.get("client_id")
        self.client_secret = config_dict.get("client_secret")
        self.callback_url = config_dict.get("callback_url")
        self.version = config_dict.get("version", 2)
        self.auth_base_url = "{}/v{}/o/authorize".format(self.base_url, self.version)
        self.auth_token_url = "{}/v{}/o/token/".format(self.base_url, self.version)

    def get_patient_data(self, config):
        config["url"] = FHIR_RESOURCE_TYPE["Patient"]
        return fhir_request(self, config)

    def get_coverage_data(self, config):
        config["url"] = FHIR_RESOURCE_TYPE["Coverage"]
        return fhir_request(self, config)

    def get_explaination_of_benefit_data(self, config):
        config["url"] = FHIR_RESOURCE_TYPE["ExplanationOfBenefit"]
        return fhir_request(self, config)

    def get_profile_data(self, config):
        config["url"] = FHIR_RESOURCE_TYPE["Profile"]
        return fhir_request(self, config)

    def get_custom_data(self, config):
        return fhir_request(self, config)

    def refresh_auth_token(self, auth_token):
        return refresh_auth_token(self, auth_token)

    def generate_auth_data(self):
        return generate_auth_data()

    def generate_authorize_url(self, auth_data):
        return generate_authorize_url(self, auth_data)

    def get_authorization_token(self, auth_data, callback_code, callback_state):
        return get_authorization_token(self, auth_data, callback_code, callback_state)
