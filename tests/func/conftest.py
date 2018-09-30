# -*- coding: utf-8 -*-

import os
from pathlib import Path

import py
import pytest


@pytest.fixture()
def tmp_home_factory(tmpdir: py.path.local):
    fake_home_dir = str(tmpdir.mkdir('home'))

    def tmp_home():
        return Path(fake_home_dir)

    return tmp_home


@pytest.fixture(autouse=True)
def patch_home(monkeypatch, tmp_home_factory):
    fake_home = tmp_home_factory()
    monkeypatch.setenv('HOME', str(fake_home))
    assert os.environ['HOME'] == str(fake_home)

    monkeypatch.setattr(Path, 'home', tmp_home_factory)
    assert Path.home() == fake_home

    monkeypatch.setattr('dot.config.DEFAULT_DOTFILES_HOME', fake_home / '.dotfiles')


@pytest.fixture()
def dotfiles_dir(tmp_home_factory) -> Path:
    fake_dotfiles_home = tmp_home_factory() / '.dotfiles'
    fake_dotfiles_home.mkdir()
    return fake_dotfiles_home


@pytest.fixture()
def topics_dir(dotfiles_dir: Path) -> Path:
    fake_topics_dir = dotfiles_dir / 'topics'
    fake_topics_dir.mkdir()
    return fake_topics_dir
