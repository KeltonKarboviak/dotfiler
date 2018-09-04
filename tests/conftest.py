# -*- coding: utf-8 -*-

import pytest


@pytest.fixture
def valid_config() -> dict:
    yield {
        'version': '1.0',
        'topics': [
            'homebrew',
            'python',
        ],
    }


@pytest.fixture
def config_missing_version(valid_config) -> dict:
    config = valid_config.copy()
    del config['version']
    yield config


@pytest.fixture
def config_missing_topics(valid_config) -> dict:
    config = valid_config.copy()
    del config['topics']
    yield config


@pytest.fixture
def valid_config_with_no_home_dir(valid_config) -> dict:
    config = valid_config.copy()
    if 'dotfiles_home' in config:
        del config['dotfiles_home']
    yield config


@pytest.fixture
def valid_config_with_home_dir(valid_config) -> dict:
    config = valid_config.copy()
    config['dotfiles_home'] = '~/.dotdir'
    yield config
