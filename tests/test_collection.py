import os
import sys

from pkg_resources import get_distribution
import pytest

import lamancha


def test_flit_symlink():
    if getattr(sys, "frozen", False):
        with pytest.raises(lamancha.exceptions.NoLicense):
            self = lamancha.Distribution(get_distribution("flit_symlink"))
        return

    self = lamancha.Distribution(get_distribution("flit_symlink"))
    assert self.name == "flit-symlink"
    assert self.author == "Aphid"
    assert self.license_name == "MIT"
    assert list(self.license) == [""]
    assert "Copyright (c) 2022 Aphid" in self.license[""]
    assert self.url == "https://pypi.org/project/flit-symlink"
    assert not self.url


def test_setuptools_dual_license():
    self = lamancha.Distribution(get_distribution("setuptools_dual_license"))
    assert self.name == "setuptools-dual-license"
    assert self.author == "Bear"
    assert self.license_name == "GPLv2 or MIT"
    assert sorted(self.license) == ["BSD", "MIT"]
    assert "MIT" in self.license["MIT"]
    assert "BSD" in self.license["BSD"]
    assert self.url == "https://github.com/foo/setuptools_dual_license"


def test_setuptools_editable():
    if getattr(sys, "frozen", False):
        with pytest.raises(lamancha.exceptions.FrozenEditable):
            self = lamancha.Distribution(
                get_distribution("setuptools_editable"))
        return

    self = lamancha.Distribution(get_distribution("setuptools_editable"))
    assert self.name == "setuptools-editable"
    assert self.author == "Cat"
    assert self.license_name == "MIT"
    assert list(self.license) == [""]
    assert "MIT" in self.license[""]
    assert self.url == "https://github.com/foo/setuptools_editable"


def test_setuptools_install():
    with pytest.raises(lamancha.exceptions.Egg, match="setuptools-install"):
        lamancha.Distribution(get_distribution("setuptools_install"))


def test_missing_license():
    with pytest.raises(lamancha.exceptions.NoLicense,
                       match="setuptools-missing-license"):
        lamancha.Distribution(get_distribution("setuptools_missing_license"))


def test_setuptools_wheel():
    self = lamancha.Distribution(get_distribution("setuptools-wheel"))
    assert self.name == "setuptools-wheel"
    assert self.author == "The setuptools-wheel development team"
    assert not self.author
    assert self.license_name == "MIT"
    assert list(self.license) == [""]
    assert "Copyright (c) 2022 Flamingo" in self.license[""]
    assert self.url == "https://pypi.org/project/setuptools-wheel"


@pytest.mark.skipif(
    getattr(sys, "frozen", False),
    reason="PyInstaller fails to collect metadata from zipped eggs.")
def test_setuptools_zipped_egg():
    with pytest.raises(lamancha.exceptions.Egg):
        lamancha.Distribution(get_distribution("setuptools_zipped_egg"))


def test_pth():
    assert sys.some_hack_pth_is_ran


def test_python():
    self = lamancha.python
    assert self.name == "Python"
    assert "PSF" in self.license[""]


@pytest.mark.skipif(getattr(sys, "frozen", False), reason="")
def test_pyinstaller_hook():
    assert "hook-lamancha.py" in os.listdir(lamancha._PyInstaller_hook_dir()[0])


def test_first_textual_line():
    self = lamancha.Distribution(get_distribution("setuptools-wheel"))
    assert self.name == "setuptools-wheel"
    assert self.author == "The setuptools-wheel development team"

    self.license_name = "hello world!"
    assert self.license_name == "hello world!"

    self.license_name = "=====\n foo \n=====\n\nmore text\n"
    assert self.license_name == "foo"

    self.license_name = "----------"
    assert not self.license_name
