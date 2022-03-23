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


class BlueButton:
    name = "bb2"
    verbose_name = "Blue Button 2.0 SDK Package"

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
