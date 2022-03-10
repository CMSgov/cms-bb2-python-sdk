import pytest

from bb2 import Bb2

JSON_CONFIGS_DIR = "src/tests/test_configs/json/"


def test_invalid_file_extension():
    # Test extension not matching .json or .yaml
    with pytest.raises(
        ValueError,
        match=r"Error: Configuration file extension"
              " must be .json or .yaml for:.*",
    ):
        Bb2(config_file="file.xxx")


def test_valid_config():
    # json valid config sbx
    bb = Bb2(config_file=JSON_CONFIGS_DIR +
             "bluebutton-sample-config-valid-sbx.json")
    assert bb.environment == "SANDBOX"
    assert bb.base_url == "https://sandbox.bluebutton.cms.gov"
    assert bb.client_id == "<your BB2 client_id here>"
    assert bb.client_secret == "<your BB2 client_secret here>"
    assert bb.callback_url == "https://www.fake-sandbox.com/your/callback/here"
    assert bb.version == 1

    # json valid config prod
    bb = Bb2(config_file=JSON_CONFIGS_DIR +
             "bluebutton-sample-config-valid-prod.json")
    assert bb.environment == "PRODUCTION"
    assert bb.base_url == "https://api.bluebutton.cms.gov"
    assert bb.client_id == "<your BB2 client_id here>"
    assert bb.client_secret == "<your BB2 client_secret here>"
    assert bb.callback_url == "https://www.fake-prod.com/your/callback/here"
    assert bb.version == 1


def test_config_setting_environment():
    for f in [
        "bluebutton-sample-config-environment-missing.json",
        "bluebutton-sample-config-environment-wrong.json",
    ]:
        with pytest.raises(
            ValueError,
            match=r"Error: Configuration environment must"
                  " be set to SANDBOX or PRODUCTION in:.*",
        ):
            Bb2(config_file=JSON_CONFIGS_DIR + f)


def test_config_setting_missing():
    for setting, filename in [
        ["client_id", "bluebutton-sample-config-missing-id.json"],
        ["client_secret", "bluebutton-sample-config-missing-secret.json"],
        ["callback_url", "bluebutton-sample-config-missing-callback.json"],
    ]:
        with pytest.raises(
            ValueError,
            match=r"Error: Configuration setting \"{}\""
                  " is missing in:.*".format(setting),
        ):
            Bb2(config_file=JSON_CONFIGS_DIR + filename)


def test_config_version_missing_defaults_to_v2():
    bb = Bb2(config_file=JSON_CONFIGS_DIR +
             "bluebutton-sample-config-missing-version.json"
             )
    assert bb.version == 2
