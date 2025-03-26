import pytest
import vidtoolz_trim as w

from argparse import Namespace, ArgumentParser


def test_create_parser():
    subparser = ArgumentParser().add_subparsers()
    parser = w.create_parser(subparser)

    assert parser is not None

    result = parser.parse_args(["hello", "-st", "0", "-et", "1"])
    assert result.input == "hello"
    assert result.starttime == 0.0
    assert result.endtime == 1.0
    assert result.output is None


def test_plugin(capsys):
    w.trim_plugin.hello(None)
    captured = capsys.readouterr()
    assert "Hello! This is an example ``vidtoolz`` plugin." in captured.out
