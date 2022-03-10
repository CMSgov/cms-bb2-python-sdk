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
        Bb2(config_file="file.xxx")


def test_valid_config():
    # valid config sbx
    for file_type in ["json", "yaml"]:
        bb = Bb2(config_file=CONFIGS_DIR + file_type +
                 "/bluebutton-sample-config-valid-sbx." + file_type)
        assert bb.environment == "SANDBOX"
        assert bb.base_url == "https://sandbox.bluebutton.cms.gov"
        assert bb.client_id == "<your BB2 client_id here>"
        assert bb.client_secret == "<your BB2 client_secret here>"
        assert bb.callback_url == "https://www.fake-sandbox.com/your/callback/here"
        assert bb.version == 1

    # valid config prod
    for file_type in ["json", "yaml"]:
        bb = Bb2(config_file=CONFIGS_DIR + file_type +
                 "/bluebutton-sample-config-valid-prod." + file_type)
        assert bb.environment == "PRODUCTION"
        assert bb.base_url == "https://api.bluebutton.cms.gov"
        assert bb.client_id == "<your BB2 client_id here>"
        assert bb.client_secret == "<your BB2 client_secret here>"
        assert bb.callback_url == "https://www.fake-prod.com/your/callback/here"
        assert bb.version == 1


def test_config_setting_environment():
    for file_type in ["json", "yaml"]:
        for file_name in [
            "bluebutton-sample-config-environment-missing",
            "bluebutton-sample-config-environment-wrong",
        ]:
            with pytest.raises(
                ValueError,
                match=r"Error: Configuration environment must"
                      " be set to SANDBOX or PRODUCTION in:.*",
            ):
                Bb2(config_file=CONFIGS_DIR + file_type + "/" + file_name + "." + file_type)


def test_config_setting_missing():
    for file_type in ["json", "yaml"]:
        for setting, file_name in [
            ["client_id", "bluebutton-sample-config-missing-id"],
            ["client_secret", "bluebutton-sample-config-missing-secret"],
            ["callback_url", "bluebutton-sample-config-missing-callback"],
        ]:
            with pytest.raises(
                ValueError,
                match=r"Error: Configuration setting \"{}\""
                      " is missing in:.*".format(setting),
            ):
                Bb2(config_file=CONFIGS_DIR + file_type + "/" + file_name + "." + file_type)


def test_config_version_missing_defaults_to_v2():
    for file_type in ["json", "yaml"]:
        bb = Bb2(config_file=CONFIGS_DIR + file_type +
                 "/bluebutton-sample-config-missing-version." + file_type
                 )
        assert bb.version == 2
