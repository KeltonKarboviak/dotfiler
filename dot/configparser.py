# -*- coding: utf-8 -*-

import yaml


SUPPORTED_VERSIONS = [
    '1.0'
]
SUPPORTED_VERSIONS_STR = ', '.join(SUPPORTED_VERSIONS)


class DotfileConfigError(Exception):
    pass


class UnsupportedConfigVersionError(Exception):

    def __init__(self, version: str):
        self.version = version

        msg = f'Unsupported config version {version}. ' \
            f'Supported versions: {SUPPORTED_VERSIONS_STR}'

        super(UnsupportedConfigVersionError, self).__init__(msg)


class DotfileConfigValueError(DotfileConfigError):
    pass


class DotfileConfig(object):

    def __init__(self, version: str):
        self.version = version


class DotfileConfigBuilder(object):

    def version(self, version: str):
        if version not in SUPPORTED_VERSIONS:
            raise UnsupportedConfigVersionError(version)

        self._version = version

        return self

    def build(self):
        return DotfileConfig(self._version)


class DotfileConfigParser(object):

    def parse(self, filename: str) -> DotfileConfig:
        with open(filename) as fh:
            config = yaml.load(fh)

        print('DotfileConfigParser:', config)

        self._validate_version_is_present(config)

        return DotfileConfigBuilder() \
            .version(str(config.get('version'))) \
            .build()

    def _validate_version_is_present(self, config: dict):
        if 'version' not in config:
            raise DotfileConfigValueError('Key "version" must be specified.')
