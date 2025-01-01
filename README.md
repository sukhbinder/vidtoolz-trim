# vidtoolz-trim

[![PyPI](https://img.shields.io/pypi/v/vidtoolz-trim.svg)](https://pypi.org/project/vidtoolz-trim/)
[![Changelog](https://img.shields.io/github/v/release/sukhbinder/vidtoolz-trim?include_prereleases&label=changelog)](https://github.com/sukhbinder/vidtoolz-trim/releases)
[![Tests](https://github.com/sukhbinder/vidtoolz-trim/workflows/Test/badge.svg)](https://github.com/sukhbinder/vidtoolz-trim/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/sukhbinder/vidtoolz-trim/blob/main/LICENSE)

Trim video using ffmpeg

## Installation

First install [vidtoolz](https://github.com/sukhbinder/vidtoolz).

```bash
pip install vidtoolz
```

Then install this plugin in the same environment as your vidtoolz application.

```bash
vidtoolz install vidtoolz-trim
```
## Usage

type ``vidtoolz-trim --help`` to get help



## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:
```bash
cd vidtoolz-trim
python -m venv venv
source venv/bin/activate
```
Now install the dependencies and test dependencies:
```bash
pip install -e '.[test]'
```
To run the tests:
```bash
python -m pytest
```
