# -*- coding: utf-8 -*-
"""Test the Topic data type."""

from dot.topic import Topic


def test_defaults():
    """Using no parameters should invoke defaults."""
    expected_topic = Topic(
        name='',
        enabled=True,
        symlinks=[],
        installer='install.zsh',
        aliaser='aliases.zsh',
        pather='paths.zsh',
        enver='envs.zsh',
    )
    actual_topic = Topic()

    assert expected_topic == actual_topic
