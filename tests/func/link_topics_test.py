# -*- coding: utf-8 -*-

from pathlib import Path

import pytest

import dot
from dot.topic import Topic


def create_structure_for_topic(topics_dir: Path, topic: Topic):
    print('Setting up fs structure for:', topic)
    this_topic_dir = topics_dir / topic.name
    this_topic_dir.mkdir()

    for sym in topic.symlinks:
        # Loop through symlinks. For each, first recursively
        # create any parent directories, then `touch` the file
        print('\tSymlink:', sym)
        sym.parent.mkdir(parents=True, exist_ok=True)
        with sym.open('w') as fh:
            fh.write(f'# File: {sym}')



@pytest.fixture()
def enabled_topic(topics_dir: Path) -> Topic:
    topic = Topic(
        name='python',
        enabled=True,
        symlinks=[
            Path(topics_dir, 'python', 'python.symlink'),
            Path(topics_dir, 'python', 'python.py.symlink'),
            Path(topics_dir, 'python', 'sub1/python_path.symlink'),
        ],
    )

    create_structure_for_topic(topics_dir, topic)

    return topic


def test_link_topic_into_dotfiles_home(enabled_topic: Topic):
    # GIVEN a topic
    # WHEN the topic is linked
    # THEN it should exist within the user's home
    dot.link_topic(enabled_topic)

    home = Path.home()
    for symlink in enabled_topic.symlinks:
        # Add a <dot> to the beginning of the filename prefix,
        # check if it's a symlink in the user's home
        target_link = home.joinpath('.' + symlink.stem)
        assert target_link.is_symlink() and target_link.exists()
        assert target_link.resolve() == symlink


def test_link_topic_with_overwrite_true(
    enabled_topic: Topic, topics_dir: Path,
):
    # GIVEN a topic
    # WHEN the topic is linked, a file already exists with
    #  the same dotted name in the user's home, and the
    #  user specifies `overwrite = True`
    # THEN the topic's symlink overwrites the existing file
    target_link = Path.home().joinpath('.python')
    target_link.touch()
    assert target_link.exists()

    dot.link_topic(enabled_topic, overwrite=True)

    assert target_link.is_symlink() and target_link.exists()
    assert target_link.resolve() == topics_dir.joinpath('python', 'python.symlink')

    # Assert that backup of existing file/symlink was made
    assert Path.home().joinpath('.python.bak').exists()
