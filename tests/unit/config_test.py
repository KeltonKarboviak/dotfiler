# -*- coding: utf-8 -*-
"""Test the DotfileConfig data type."""

from pathlib import Path

from dot.config import DotfileConfig


def test_defaults():
    """Using no parameters should invoke defaults."""
    expected_config = DotfileConfig(
        version='',
        dotfiles_home=Path.home() / '.dotfiles',
        topics=[],
    )
    actual_config = DotfileConfig()

    assert expected_config == actual_config
