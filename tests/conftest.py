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
