from unittest import mock
import os.path

from allib.options.config import get_config


def test_parse_config(test_files_dir):
    cfg = get_config({}, os.path.join(test_files_dir, "config.cfg"))
    assert isinstance(cfg, dict)
    assert cfg["sec1"]["foo"] == "bar"
    assert cfg["sec1"]["bar"] == "baz"
    assert cfg["sec2"]["baz"] == "foo"


def test_parse_yaml(test_files_dir):
    cfg = get_config({}, os.path.join(test_files_dir, "config.yml"))
    assert isinstance(cfg, dict)
    assert cfg["foo"] == "bar"
    assert cfg["bar"]["baz"] == "foo"


def test_defaults():
    with mock.patch(
        "allib.options.config.ConfigAssembler.conf_file_to_dict"
    ) as mock_file_to_dict:
        mock_file_to_dict.return_value = {"conf-key": "conf-val"}
        cfg = get_config(
            {},
            "/does-not-matter",
            optional=True,
            defaults={
                "conf-key": "default-val",
                "default-key": "default-val",
            },
        )
    assert cfg["conf-key"] == "conf-val"
    assert cfg["default-key"] == "default-val"


def test_log_args():
    args = {"log_level": "debug"}
    cfg = get_config(args, None, optional=True)
    assert cfg["logging"]["level"] == "debug"
