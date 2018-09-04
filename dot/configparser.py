# -*- coding: utf-8 -*-

from typing import List

import yaml


SUPPORTED_VERSIONS = [
    '1.0'
]
SUPPORTED_VERSIONS_STR = ', '.join(SUPPORTED_VERSIONS)


class DotfileConfigError(Exception):
    pass


class UnsupportedConfigVersionError(DotfileConfigError):

    def __init__(self, version: str):
        self.version = version

        msg = f'Unsupported config version {version}. ' \
            f'Supported versions: {SUPPORTED_VERSIONS_STR}'

        super(UnsupportedConfigVersionError, self).__init__(msg)


class DotfileConfigValueError(DotfileConfigError):
    pass


class DotfileConfig(object):

    def __init__(self, version: str, topics: List[str]):
        self.version = version
        self.topics = topics


class DotfileConfigBuilder(object):

    def version(self, version: str):
        if version not in SUPPORTED_VERSIONS:
            raise UnsupportedConfigVersionError(version)

        self._version = version

        return self

    def topics(self, topics: List[str]):
        self._topics = topics

        return self

    def build(self):
        return DotfileConfig(
            version=self._version,
            topics=self._topics
        )


class DotfileConfigParser(object):

    def parse(self, filename: str) -> DotfileConfig:
        with open(filename) as fh:
            config = yaml.load(fh)

        print('DotfileConfigParser:', config)

        self._validate_version_key_is_present(config)
        self._validate_topics_key_is_present(config)

        return DotfileConfigBuilder() \
            .version(str(config.get('version'))) \
            .topics(config.get('topics', [])) \
            .build()

    def _validate_version_key_is_present(self, config: dict):
        if 'version' not in config:
            raise DotfileConfigValueError('Key "version" must be specified.')

    def _validate_topics_key_is_present(self, config: dict):
        if 'topics' not in config:
            raise DotfileConfigValueError('Key "topics" must be specified.')
