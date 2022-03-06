from pkg_resources import get_distribution
import pytest

import lamancha


def test_flit_symlink():
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
    assert self.license_name == "MIT and BSD"
    assert sorted(self.license) == ["BSD", "MIT"]
    assert "MIT" in self.license["MIT"]
    assert "BSD" in self.license["BSD"]
    assert self.url == "https://github.com/foo/setuptools_dual_license"


def test_setuptools_editable():
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


def test_setuptools_zipped_egg():
    with pytest.raises(lamancha.exceptions.Egg):
        lamancha.Distribution(get_distribution("setuptools_zipped_egg"))


def test_python():
    self = lamancha.python
    assert self.name == "Python"
    assert "PSF" in self.license[""]
