# -*- coding: utf-8 -*-

from pathlib import Path
from typing import Union

import py
import pytest
import yaml
from pytest import param

import dot
from dot.config import (
    DotfileConfigValueError,
    UnsupportedConfigVersionError,
)
from dot.topic import Topic


CONFIG_FIXTURES_DIR = Path('tests', 'func', 'config_fixtures')


def load_yaml_config(config_name: Union[Path, str]) -> dict:
    with CONFIG_FIXTURES_DIR.joinpath(config_name).open('r') as fh:
        config = yaml.load(fh)
    return config


@pytest.fixture()
def valid_config() -> dict:
    yield load_yaml_config('valid_config.yml')


@pytest.fixture()
def config_missing_version() -> dict:
    yield load_yaml_config('no_version_specified.yml')


@pytest.fixture()
def config_missing_topics() -> dict:
    yield load_yaml_config('no_topics_specified')


@pytest.fixture()
def valid_config_with_no_dotfiles_home(valid_config) -> dict:
    config = valid_config.copy()
    if 'dotfiles_home' in config:
        del config['dotfiles_home']
    yield config


@pytest.fixture()
def valid_config_with_dotfiles_home(valid_config) -> dict:
    yield load_yaml_config('custom_dotfiles_home_specified.yml')


@pytest.fixture()
def initialized_config_file(tmpdir: py.path.local, dotfiles_dir: Path):
    """Create a dotfile config file before testing."""
    config = {
        'version': '0.1.0',
        'dotfiles_home': '~/.dotfiles',
        'topics': [
            {
                'name': 'python',
                'enabled': True,
                'initializer': 'init.zsh',
                'aliaser': 'aliases.zsh',
                'pather': 'path.zsh',
                'enver': 'env.zsh',
            },
            {
                'name': 'zsh',
                'enabled': True,
                'initializer': 'install.zsh',
                'aliaser': 'aliases.zsh',
            },
            {
                'name': 'ruby',
                'enabled': False,
                'initializer': 'init.zsh',
            },
        ],
    }

    config_file = dotfiles_dir.joinpath('.dot.yml')
    with config_file.open('w') as fh:
        yaml.dump(config, fh)


@pytest.fixture()
def python_topic(topics_dir: Path) -> Topic:
    """Creates a python Topic that is ENABLED & has all attributes set."""
    python_topic_dir = topics_dir / 'python'
    return Topic(
        name='python',
        enabled=True,
        symlinks=[python_topic_dir / 'python.symlink'],
        installer=python_topic_dir / 'init.zsh',
        aliaser=python_topic_dir / 'aliases.zsh',
        pather=python_topic_dir / 'path.zsh',
        enver=python_topic_dir / 'env.zsh',
    )


@pytest.fixture()
def zsh_topic(topics_dir: Path) -> Topic:
    """Creates a zsh Topic that is ENABLED & does not set the
    `pather` and `enver` attributes.
    """
    zsh_topic_dir = topics_dir / 'zsh'
    return Topic(
        name='zsh',
        enabled=True,
        symlinks=[zsh_topic_dir / 'zshrc.symlink'],
        installer=zsh_topic_dir / 'install.zsh',  # Change from default 'init.zsh'
        aliaser=zsh_topic_dir / 'aliases.zsh',
        # Doesn't specify `pather` or `enver`
    )


@pytest.fixture()
def ruby_topic(topics_dir: Path) -> Topic:
    """Creates a ruby Topic that is DISABLED."""
    ruby_topic_dir = topics_dir / 'ruby'
    return Topic(
        name='ruby',
        enabled=False,
        symlinks=[ruby_topic_dir / 'ruby.symlink'],
        installer=ruby_topic_dir / 'init.zsh',
        # Doesn't specify `aliaser`, `pather`, or `enver`
    )


def test_config_with_supported_version_passes():
    # GIVEN a path to a config file with a supported `version` attribute
    # WHEN it is loaded
    # THEN the config object should contain that attribute
    config_path = CONFIG_FIXTURES_DIR / 'valid_config.yml'
    config = dot.get_config(config_path)
    assert '0.1.0' == config.version


def test_config_with_unsupported_version_fails():
    # GIVEN a path to a config file with an unsupported `version` attribute
    # WHEN it is loaded
    # THEN an exception should be thrown
    config_path = CONFIG_FIXTURES_DIR / 'unsupported_version_specified.yml'
    with pytest.raises(UnsupportedConfigVersionError):
        dot.get_config(config_path)


def test_config_with_dotfiles_home_overrides_default():
    # GIVEN a path to a config file with a custom `dotfiles_home` attribute
    # WHEN it is loaded
    # THEN the config object should contain that attribute
    config_path = CONFIG_FIXTURES_DIR / 'custom_dotfiles_home_specified.yml'
    config = dot.get_config(config_path)
    assert Path('~/.dotfiles_home').expanduser() == config.dotfiles_home


def test_config_with_no_dotfiles_home_has_default():
    # GIVEN a path to a config file with no `dotfiles_home` attribute
    # WHEN it is loaded
    # THEN the config object should contain the default
    config_path = CONFIG_FIXTURES_DIR / 'valid_config.yml'
    config = dot.get_config(config_path)
    assert Path('~/.dotfiles').expanduser() == config.dotfiles_home


def test_config_with_topics_list_passes():
    # GIVEN a path to a config file with topics
    # WHEN it is loaded
    # THEN the config object should contain those topics
    config_path = CONFIG_FIXTURES_DIR / 'valid_config.yml'
    config = dot.get_config(config_path)
    assert [Topic(name='python'), Topic(name='homebrew')] == config.topics


@pytest.mark.parametrize('config_fixture_name', [
    'no_version_specified.yml',
    'no_topics_specified.yml',
])
def test_config_missing_necessary_key_fails(config_fixture_name: str):
    # GIVEN a path to a config file without a needed key
    # WHEN it is loaded
    # THEN an exception should be thrown
    config_path = CONFIG_FIXTURES_DIR / config_fixture_name
    with pytest.raises(DotfileConfigValueError):
        dot.get_config(config_path)


"""
Topic Parsing Tests
"""


@pytest.fixture()
def topic_config_default() -> dict:
    yield {
        'name': 'python',
        'enabled': True,
        'installer': 'install.zsh',
        'aliaser': 'aliases.zsh',
        'pather': 'path.zsh',
        'enver': 'env.zsh',
    }


@pytest.fixture()
def topic_config_disabled(topic_config_default: dict) -> dict:
    config = topic_config_default.copy()
    config['enabled'] = False
    return config


@pytest.fixture()
def topic_config_no_enabled(topic_config_default: dict) -> dict:
    config = topic_config_default.copy()
    if 'enabled' in config:
        del config['enabled']
    yield config


@pytest.mark.parametrize('topic_config, expected_topic', [
    param(
        {'name': 'python'},
        Topic(
            'python',
            enabled=True,
            installer='install.zsh',
            aliaser='aliases.zsh',
            pather='paths.zsh',
            enver='envs.zsh'),
        id='defaults',
    ),
    param(
        {'name': 'python', 'enabled': False},
        Topic('python', enabled=False),
        id='enabled',
    ),
    param(
        {'name': 'python', 'symlinks': ['python.symlink']},
        Topic('python', symlinks=['python.symlink']),
        id='symlinks',
    ),
    param(
        {'name': 'python', 'install': 'init.zsh'},
        Topic('python', installer='init.zsh'),
        id='installer',
    ),
    param(
        {'name': 'python', 'aliases': 'alias.zsh'},
        Topic('python', aliaser='alias.zsh'),
        id='aliaser',
    ),
    param(
        {'name': 'python', 'paths': 'path.zsh'},
        Topic('python', pather='path.zsh'),
        id='pather',
    ),
    param(
        {'name': 'python', 'envs': 'environ.zsh'},
        Topic('python', enver='environ.zsh'),
        id='enver',
    ),
])
def test_topic_config_parse(topic_config, expected_topic):
    topic = dot.parse_topic(topic_config)
    assert expected_topic == topic
