import sys
import email.parser
import re
from pathlib import Path

import pkg_resources

from lamancha import exceptions


class Component:
    """A simple bucket class for an arbitrary software component or package."""

    name: str
    "The name of the component."
    version: str
    "Its version."
    author: str
    "Its author."
    summary: str
    "A one-line description of what the component does."
    url: str
    "The homepage of the component."

    def __init__(self, name, version, author, summary, license_name, license,
                 url):
        self.name = name
        self.version = version
        self.author = author
        self.summary = summary
        self.license_name = license_name
        self.license = license
        self.url = url

    @property
    def license_name(self) -> str:
        """License type e.g 'MIT' or 'BSD'.

        Dual licensed components may use something like 'MIT or BSD'. To keep
        this field short (and therefore more tabular friendly), the word
        'license' is removed if present and 'version' contracts to 'v'. E.g.
        'GPL license version 3' becomes 'GPL v3'.

        """
        return self._license_name

    @license_name.setter
    def license_name(self, name):
        name = name or "UNKNOWN"
        name = re.sub(" licen[sc]e", "", name, flags=re.I)
        name = re.sub("version ", "v", name, flags=re.I)
        self._license_name = name

    @property
    def license(self) -> dict:
        """The license contents.

        To accommodate cases where software is dual licensed, the `license`
        attribute is a `dict` mapping the available license types to their text
        bodies. For example a package using both MIT and BSD, containing a
        LICENSE.MIT and a LICENSE.BSD file, will have a `license` attribute::

            {"BSD": "BSD license contents", "MIT": "MIT license contents"}

        If a license file doesn't have an identifying suffix then it'll be kept
        under an empty string key.

        """
        return self._license

    @license.setter
    def license(self, x):
        self._license = x() if callable(x) else x


class Distribution(Component):
    """License information from a `pkg_resources.Distribution()`."""

    def __init__(self, distribution: pkg_resources.Distribution):
        self._distribution = distribution

        if isinstance(self._distribution, pkg_resources.DistInfoDistribution):
            metadata = self._distribution.get_metadata("METADATA")
            files = self._distribution.metadata_listdir("")
            for name in [
                    self._distribution.project_name,
                    self._distribution.project_name.replace("-", "_")
            ]:
                try:
                    path = self._distribution.get_resource_string(
                        None, name + ".pth").decode()
                except FileNotFoundError:
                    continue
                files.extend(Path(path).glob("*"))

        elif isinstance(self._distribution, pkg_resources.EggInfoDistribution):
            metadata = self._distribution.get_metadata("PKG-INFO")
            files = self._distribution.get_metadata("SOURCES.txt") \
                .strip("\n").split("\n")

        else:
            raise exceptions.Egg(self._distribution)

        self._license_paths = {}
        for file in files:
            match = re.compile(r"LICEN[SC]E(\..*)?").fullmatch(Path(file).name)
            if match:
                self._license_paths[(match.group(1) or "")[1:]] = file

        if not self._license_paths:
            raise exceptions.NoLicense(self._distribution)

        self._metadata = email.parser.HeaderParser().parsestr(metadata)
        self.name = self._distribution.project_name
        self.version = self._distribution.version
        self.author = self._metadata["Author"]
        self.summary = self._metadata["Summary"]
        self.license_name = self._metadata["License"]
        self.url = self._metadata["Home-page"]

        if self.license_name == "UNKNOWN":
            for classifier in self._metadata.get_all("Classifier"):
                if classifier.startswith("License"):
                    self.license_name = classifier.split("::")[-1].strip()

        if self.url is None or self.url == "UNKNOWN":
            self.url = "https://pypi.org/project/" + self.name

    @property
    def license(self):
        out = {}
        for (name, path) in self._license_paths.items():
            if isinstance(path, Path):
                text = path.read_text("utf-8")
            elif isinstance(self._distribution,
                            pkg_resources.DistInfoDistribution):
                text = self._distribution.get_metadata(path)
            else:
                text = self._distribution.get_resource_string('', path).decode()
            out[name] = text
        return out


def _python():
    import sysconfig
    root = sysconfig.get_path("stdlib")
    for name in ["../LICENSE.txt", "../LICENSE", "LICENSE.txt",
                 "LICENSE"]:  # pragma: no branch
        path = Path(root, name)
        try:
            return {"": path.read_text("utf-8")}
        except FileNotFoundError:  # pragma: no cover
            continue
    raise exceptions.NoPythonLicense()  # pragma: no cover


python = Component(
    name="Python", version=sys.version.split()[0],
    author="Python Software Foundation", summary="Python is an " \
    "interpreted high-level general-purpose programming language.",
    license_name="PSF 2", license=_python(),
    url="https://www.python.org")
