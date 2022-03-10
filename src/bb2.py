"""
Blue Button 2.0 SDK Class

"""
import json
import os
import pathlib
import yaml

ROOT_DIR = os.path.abspath(os.curdir) + "/"
DEFAULT_CONFIG_FILE_LOCATION = ROOT_DIR + "./.bluebutton-config.json"

ENVIRONMENT_URLS = {
    "SANDBOX": "https://sandbox.bluebutton.cms.gov",
    "PRODUCTION": "https://api.bluebutton.cms.gov",
}


class Bb2:
    name = "bb2"
    verbose_name = "Blue Button 2.0 SDK Package"

    def __init__(self, config_file=DEFAULT_CONFIG_FILE_LOCATION):
        self.config_file = config_file
        self.config = {}

        self.environment = None
        self.client_id = None
        self.client_secret = None
        self.callback_url = None
        self.version = 2  # Default to BB2 version 2

        self.base_url = None

        self.config = self._read_config_file()

        # Validate and set
        self.set_configuration(self.config)

    def _read_json(self, file_path):
        with open(file_path, "r") as f:
            data = json.load(f)
            return data

    def _read_yaml(self, file_path):
        with open(file_path, "r") as f:
            return yaml.safe_load(f)

    def _read_config_file(self):
        extension = pathlib.Path(self.config_file).suffix

        if extension == ".json":
            return self._read_json(self.config_file)
        elif extension == ".yaml":
            return self._read_yaml(self.config_file)
        else:
            raise ValueError(
                "Error: Configuration file extension must be .json"
                " or .yaml for: {}".format(
                    self.config_file
                )
            )

    def set_configuration(self, config):
        # Check environment setting
        env = config.get("environment", None)
        if env in ["SANDBOX", "PRODUCTION"]:
            self.environment = env
            self.base_url = ENVIRONMENT_URLS.get(env, None)
        else:
            raise ValueError(
                "Error: Configuration environment must be set to"
                " SANDBOX or PRODUCTION in: {}".format(
                    self.config_file
                )
            )

        # Check other settings are provided
        for s in ["client_id", "client_secret", "callback_url"]:
            setting = config.get(s, None)
            if setting is None:
                raise ValueError(
                    'Error: Configuration setting "'
                    + s
                    + '" is missing in: {}'.format(self.config_file)
                )

        self.client_id = config.get("client_id")
        self.client_secret = config.get("client_secret")
        self.callback_url = config.get("callback_url")
        self.version = config.get("version", 2)
