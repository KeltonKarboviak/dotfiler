# -*- coding: utf-8 -*-

from io import StringIO
from unittest import TestCase, mock

from dot.configparser import (
    DotfileConfig,
    DotfileConfigBuilder,
    DotfileConfigParser,
    DotfileConfigValueError,
    UnsupportedConfigVersionError,
)


VERSIONS = ['1.0']


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
        fh = StringIO(
            f'version: {expected_version}'
        )
        mock_open.return_value = fh

        mock_yaml.load.return_value = {
            'version': expected_version,
        }

        expected_open_calls = [
            mock.call(self.config_filename),
        ]
        expected_yaml_calls = [
            mock.call(fh),
        ]

        # act
        config = self.parser.parse(self.config_filename)

        # assert
        self.assertEqual(
            expected_open_calls,
            mock_open.mock_calls)
        self.assertEqual(
            expected_yaml_calls,
            mock_yaml.load.mock_calls)
        self.assertEqual(expected_version, config.version)
        self.assertIsInstance(config, DotfileConfig)

    @mock.patch('dot.configparser.SUPPORTED_VERSIONS', VERSIONS)
    def test_config_with_unsupported_version_fails(self, mock_open, mock_yaml):
        # arrange
        expected_version = '2.0'
        fh = StringIO(
            f'version: {expected_version}'
        )
        mock_open.return_value = fh

        mock_yaml.load.return_value = {
            'version': expected_version,
        }

        expected_open_calls = [
            mock.call(self.config_filename),
        ]
        expected_yaml_calls = [
            mock.call(fh),
        ]

        # act
        try:
            config = self.parser.parse(self.config_filename)
            self.fail('Expected exception!')
        except UnsupportedConfigVersionError as err:
            pass

        # assert
        self.assertEqual(
            expected_open_calls,
            mock_open.mock_calls)
        self.assertEqual(
            expected_yaml_calls,
            mock_yaml.load.mock_calls)

    @mock.patch('dot.configparser.SUPPORTED_VERSIONS', VERSIONS)
    def test_config_with_no_version_fails(self, mock_open, mock_yaml):
        # arrange
        fh = StringIO(
            f'test_key: test_value'
        )
        mock_open.return_value = fh

        mock_yaml.load.return_value = {
            'test_key': 'test_value',
        }

        expected_open_calls = [
            mock.call(self.config_filename),
        ]
        expected_yaml_calls = [
            mock.call(fh),
        ]

        # act
        try:
            config = self.parser.parse(self.config_filename)
            self.fail('Expected exception!')
        except DotfileConfigValueError as err:
            pass

        # assert
        self.assertEqual(
            expected_open_calls,
            mock_open.mock_calls)
        self.assertEqual(
            expected_yaml_calls,
            mock_yaml.load.mock_calls)
