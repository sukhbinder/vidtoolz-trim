import pytest
import vidtoolz_trim as w

from argparse import Namespace, ArgumentParser


def test_create_parser():
    subparser = ArgumentParser().add_subparsers()
    parser = w.create_parser(subparser)

    assert parser is not None

    result = parser.parse_args(["hello", "-st", "00:00", "-et", "1:00"])
    assert result.inputfile == "hello"
    assert result.starttime == "00:00"
    assert result.endtime == "1:00"
    assert result.outputfile == "output.mp4"
    assert result.duration is None


def test_plugin(capsys):
    w.trim_plugin.hello(None)
    captured = capsys.readouterr()
    assert "Hello! This is an example ``vidtoolz`` plugin." in captured.out
