import os
import sys

import pytest

import lamancha


def test_flit_symlink():
    if getattr(sys, "frozen", False):
        with pytest.raises(lamancha.exceptions.NoLicense):
            self = lamancha.Distribution("flit_symlink")
        return

    self = lamancha.Distribution("flit_symlink")
    assert self.name == "flit_symlink"
    assert self.author == "Aphid"
    assert self.license_name == "MIT"
    assert list(self.license) == [""]
    assert "Copyright (c) 2022 Aphid" in self.license[""]
    assert self.url == "https://pypi.org/project/flit_symlink"
    assert not self.url


def test_setuptools_dual_license():
    self = lamancha.Distribution("setuptools_dual_license")
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
            self = lamancha.Distribution("setuptools_editable")
        return

    self = lamancha.Distribution("setuptools_editable")
    assert self.name == "setuptools-editable"
    assert self.author == "Cat"
    assert self.license_name == "MIT"
    assert list(self.license) == [""]
    assert "MIT" in self.license[""]
    assert self.url == "https://github.com/foo/setuptools_editable"


def test_setuptools_install():
    with pytest.raises(lamancha.exceptions.Egg, match="setuptools-install"):
        self = lamancha.Distribution("setuptools_install")


def test_missing_license():
    with pytest.raises(lamancha.exceptions.NoLicense,
                       match="setuptools-missing-license"):
        lamancha.Distribution("setuptools_missing_license")


def test_setuptools_wheel():
    self = lamancha.Distribution("setuptools-wheel")
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
        lamancha.Distribution("setuptools_zipped_egg")


@pytest.mark.skipif(
    getattr(sys, "frozen", False),
    reason="PyInstaller can't find editable pyproject.toml installs.")
def test_pyproject_toml_editable():
    self = lamancha.Distribution("pyproject_toml_editable")
    assert self.name == "pyproject-toml-editable"
    assert self.author == "Hippo"
    assert self.license_name == "MIT"
    assert list(self.license) == [""]
    assert "Copyright (c) 2022, The Hippos" in self.license[""]
    assert self.url == "https://github.com/hippo/pyproject_toml_editable"


@pytest.mark.skipif(getattr(sys, "frozen", False),
                    reason="PyInstaller doesn't support .pth files.")
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
    self = lamancha.Distribution("setuptools-wheel")
    assert self.name == "setuptools-wheel"
    assert self.author == "The setuptools-wheel development team"

    self.license_name = "hello world!"
    assert self.license_name == "hello world!"

    self.license_name = "=====\n foo \n=====\n\nmore text\n"
    assert self.license_name == "foo"

    self.license_name = "----------"
    assert not self.license_name


def test_collect_dependencies():
    assert "lamancha" in lamancha.collect_dependencies("lamancha")
    assert "pytest" not in lamancha.collect_dependencies("lamancha")
    assert "pluggy" in lamancha.collect_dependencies("pytest")
    assert "pytest-cov" in lamancha.collect_dependencies("lamancha[test]")
    assert "lamancha" in lamancha.collect_dependencies(
        'lamancha; python_version > "3.6"')
    assert lamancha.collect_dependencies(
        'lamancha; python_version < "3.6"') == set()
