# -*- coding: utf-8 -*-

from io import StringIO
from unittest import TestCase, mock

import pytest

from dot.configparser import (
    DotfileConfig,
    DotfileConfigBuilder,
    DotfileConfigParser,
    DotfileConfigValueError,
    UnsupportedConfigVersionError,
)


VERSIONS = ['1.0']
CONFIG_FILENAME = 'dotfile_config.yml'


@pytest.fixture
def parser():
    return DotfileConfigParser()


@pytest.fixture
def mock_open(mock):
    return mock.patch('dot.configparser.open', mock.mock_open())


@pytest.fixture
def mock_yaml(mock):
    return mock.patch('dot.configparser.yaml')


@mock.patch('dot.configparser.yaml')
@mock.patch('dot.configparser.open')
class DotfileConfigParserTests(TestCase):

    def setUp(self):
        self.config_filename = 'dotfile_config.yml'
        self.parser = DotfileConfigParser()

    def tearDown(self):
        pass

    @mock.patch('dot.configparser.SUPPORTED_VERSIONS', VERSIONS)
    def test_config_with_supported_version_passes(self, mock_open, mock_yaml):
        # arrange
        expected_version = '1.0'
        mock_yaml.load.return_value = {
            'version': expected_version,
            'topics': [
                'homebrew',
                'python',
            ],
        }

        # act
        config = self.parser.parse(self.config_filename)

        # assert
        self.assertEqual(expected_version, config.version)
        self.assertIsInstance(config, DotfileConfig)

    @mock.patch('dot.configparser.SUPPORTED_VERSIONS', VERSIONS)
    def test_config_with_unsupported_version_fails(self, mock_open, mock_yaml):
        # arrange
        expected_version = '2.0'
        mock_yaml.load.return_value = {
            'version': expected_version,
            'topics': [
                'homebrew',
                'python',
            ],
        }

        # act
        try:
            config = self.parser.parse(self.config_filename)
            self.fail('Expected exception!')
        except UnsupportedConfigVersionError as err:
            pass

        # assert

    def test_config_with_no_version_fails(self, mock_open, mock_yaml):
        # arrange
        mock_yaml.load.return_value = {
            'test_key': 'test_value',
        }

        # act
        try:
            config = self.parser.parse(self.config_filename)
            self.fail('Expected exception!')
        except DotfileConfigValueError as err:
            pass

        # assert


def test_config_with_topics_list_passes(
    mock_open,
    mock_yaml,
    parser,
    valid_config
):
    # arrange
    mock_yaml.load.return_value = valid_config

    expected_topics = [
        'homebrew',
        'python',
    ]

    # act
    config = parser.parse(CONFIG_FILENAME)

    # assert
    assert expected_topics == config.topics
    assert isinstance(config, DotfileConfig)


def test_config_with_no_topics_list_fails(
    mock,
    mock_open,
    mock_yaml,
    parser,
    config_missing_topics
):
    # arrange
    mock_yaml.load.return_value = config_missing_topics

    # act
    try:
        config = parser.parse(CONFIG_FILENAME)
        assert False, 'Expected exception!'
    except DotfileConfigValueError as err:
        pass

    # assert
