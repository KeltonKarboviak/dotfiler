# -*- coding: utf-8 -*-

from pathlib import Path
from typing import List, Union

import yaml


DEFAULT_DOTFILES_HOME = Path('~/.dotfiles').expanduser()
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

    def __init__(
        self,
        version: str,
        home_dir: Union[Path, str],
        topics: List[str]
    ):
        self.version = version
        self.topics = topics
        self.home_dir = home_dir


class DotfileConfigBuilder(object):

    def version(self, version: str):
        if version not in SUPPORTED_VERSIONS:
            raise UnsupportedConfigVersionError(version)

        self._version = version

        return self

    def home_dir(self, home_dir: Union[Path, str]):
        self._home_dir = Path(home_dir).expanduser()

        return self

    def topics(self, topics: List[str]):
        self._topics = topics

        return self

    def build(self):
        return DotfileConfig(
            version=self._version,
            home_dir=self._home_dir,
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
            .home_dir(config.get('dotfiles_home', DEFAULT_DOTFILES_HOME)) \
            .topics(config.get('topics')) \
            .build()

    def _validate_version_key_is_present(self, config: dict):
        if 'version' not in config:
            raise DotfileConfigValueError('Key "version" must be specified.')

    def _validate_topics_key_is_present(self, config: dict):
        if 'topics' not in config:
            raise DotfileConfigValueError('Key "topics" must be specified.')
