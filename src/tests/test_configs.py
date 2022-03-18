import pytest

from bb2 import Bb2


CONFIGS_DIR = "src/tests/test_configs/"


def test_invalid_file_extension():
    # Test extension not matching .json or .yaml
    with pytest.raises(
        ValueError,
        match=r"Error: Configuration file extension"
              " must be .json or .yaml for:.*",
    ):
        Bb2(config="file.xxx")


def test_read_config_json_equals_yaml():
    bb = Bb2(config=CONFIGS_DIR +
             "json/bluebutton-sample-config-valid-sbx.json")

    # Test dict's are equal for both JSON & YAML
    assert bb._read_config(
        config=CONFIGS_DIR + "json/bluebutton-sample-config-valid-sbx.json"
    ) == bb._read_config(
        config=CONFIGS_DIR + "yaml/bluebutton-sample-config-valid-sbx.yaml"
    )


def test_valid_config():
    # valid config sbx
    bb = Bb2(config=CONFIGS_DIR +
             "json/bluebutton-sample-config-valid-sbx.json")
    assert bb.base_url == "https://sandbox.bluebutton.cms.gov"
    assert bb.client_id == "<your BB2 client_id here>"
    assert bb.client_secret == "<your BB2 client_secret here>"
    assert bb.callback_url == "https://www.fake-sandbox.com/your/callback/here"
    assert bb.version == 1

    # valid config prod
    bb = Bb2(config=CONFIGS_DIR +
             "json/bluebutton-sample-config-valid-prod.json")
    assert bb.base_url == "https://api.bluebutton.cms.gov"
    assert bb.client_id == "<your BB2 client_id here>"
    assert bb.client_secret == "<your BB2 client_secret here>"
    assert bb.callback_url == "https://www.fake-prod.com/your/callback/here"
    assert bb.version == 1

    # valid config from a dictionary
    config_dict = {
        "environment": "PRODUCTION",
        "client_id": "<your BB2 client_id here>",
        "client_secret": "<your BB2 client_secret here>",
        "callback_url": "https://www.fake-prod.com/your/callback/here",
        "version": 1,
    }
    bb = Bb2(config_dict)
    assert bb.base_url == "https://api.bluebutton.cms.gov"
    assert bb.client_id == "<your BB2 client_id here>"
    assert bb.client_secret == "<your BB2 client_secret here>"
    assert bb.callback_url == "https://www.fake-prod.com/your/callback/here"
    assert bb.version == 1


def test_config_setting_environment():
    for file_name in [
        "json/bluebutton-sample-config-environment-missing.json",
        "json/bluebutton-sample-config-environment-wrong.json",
    ]:
        with pytest.raises(
            ValueError,
            match=r"Error: Configuration environment must"
            " be set to SANDBOX or PRODUCTION in:.*",
        ):
            Bb2(config=CONFIGS_DIR + file_name)


def test_config_setting_missing():
    for setting, file_name in [
        ["client_id", "json/bluebutton-sample-config-missing-id.json"],
        ["client_secret", "json/bluebutton-sample-config-missing-secret.json"],
        ["callback_url",
         "json/bluebutton-sample-config-missing-callback.json"],
    ]:
        with pytest.raises(
            ValueError,
            match=r"Error: Configuration setting \"{}\""
            " is missing in:.*".format(setting),
        ):
            Bb2(config=CONFIGS_DIR + file_name)


def test_config_version_missing_defaults_to_v2():
    bb = Bb2(config=CONFIGS_DIR +
             "json/bluebutton-sample-config-missing-version.json")
    assert bb.version == 2
