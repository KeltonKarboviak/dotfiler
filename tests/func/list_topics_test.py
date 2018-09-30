# -*- coding: utf-8 -*-

import pytest

import dot
from dot.config import DotfileConfig
from dot.topic import Topic


@pytest.fixture()
def dotfile_config():
    return DotfileConfig()


@pytest.fixture()
def config_with_topics(dotfile_config, topics_multi_states):
    return dotfile_config._replace(topics=topics_multi_states)


@pytest.fixture()
def topics_multi_states():
    """Several topics with mix of enabled & disabled states."""
    return (
        # Enabled topics
        Topic(name='homebrew', enabled=True),
        Topic(name='python', enabled=True),
        # Disabled topics
        Topic(name='ruby', enabled=False),
        Topic(name='zsh', enabled=False),
    )


def test_list_enabled_topics(config_with_topics: DotfileConfig):
    # GIVEN a config object
    # WHEN enabled topics are listed
    # THEN disabled topics should be filtered out
    expected_topics = [
        Topic('homebrew', True),
        Topic('python', True),
    ]
    topics = dot.list_topics(config_with_topics, enabled=True)

    assert expected_topics == topics


def test_list_disabled_topics(config_with_topics: DotfileConfig):
    # GIVEN a config object
    # WHEN disabled topics are listed
    # THEN enabled topics should be filtered out
    expected_topics = [
        Topic('ruby', False),
        Topic('zsh', False),
    ]
    topics = dot.list_topics(config_with_topics, enabled=False)

    assert expected_topics == topics


def test_list_all_topics(config_with_topics: DotfileConfig):
    # GIVEN a config object
    # WHEN all topics are listed
    # THEN no topics should be filtered out
    expected_topics = [
        Topic('homebrew', True),
        Topic('python', True),
        Topic('ruby', False),
        Topic('zsh', False),
    ]
    topics = dot.list_topics(config_with_topics)

    assert expected_topics == topics
