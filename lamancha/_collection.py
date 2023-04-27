import sys
import re
from pathlib import Path
import contextlib
import collections
try:  # pragma: no cover
    import importlib.metadata as importlib_metadata
except ImportError:  # pragma: no cover
    import importlib_metadata

from lamancha import exceptions


class Component:
    """A simple bucket class for an arbitrary software component or package."""

    name: str
    "The name of the component."
    version: str
    "Its version."
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
    def author(self):
        """Its author(s). Defaults to a generic "The xxx development team"."""
        return self._author

    @author.setter
    def author(self, author):
        if not author or author == "UNKNOWN":
            author = Placeholder(f"The {self.name} development team")
        self._author = author

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
        if name and name != "UNKNOWN":
            # Occasionally, package authors put the entire license body in place
            # of the license name. Rectify this by taking only the first non-
            # punctuation line.
            m = re.search(r"[^\n\w]*\w+.*", name)
            if m:
                name = m[0].strip()
                # To make efficient use of screen space, strip the redundant
                # word 'license' and contract 'version X' to just 'vX'.
                name = re.sub(" licen[sc]e", "", name, flags=re.I)
                name = re.sub("version ", "v", name, flags=re.I)
            else:
                name = Placeholder("UNKNOWN")
        else:
            name = Placeholder("UNKNOWN")
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


class Placeholder(str):

    def __bool__(self):
        return False


class Distribution(Component):
    """License information from a pip installed Python distribution."""

    def __init__(self, distribution: str):
        self._distribution = importlib_metadata.distribution(distribution)

        if str(self._distribution.locate_file("")).endswith((".egg", ".egg/")):
            raise exceptions.Egg(self._distribution)

        metadata = self._distribution.metadata
        files = self._distribution.files
        for file in files:
            if file.suffix == ".pth":
                with contextlib.suppress(FileNotFoundError):
                    path = file.read_text("utf8")
                    if not path or path.startswith(("#", "import ")):
                        continue
                    files.extend(Path(path).glob("*"))

        self._license_paths = {}
        for file in files:
            match = re.compile(r"LICEN[SC]E(\..*)?").fullmatch(Path(file).name)
            if match:
                self._license_paths[(match.group(1) or "")[1:]] = file

        if not self._license_paths:
            raise exceptions.NoLicense(self._distribution)

        if getattr(sys, "frozen", False):  # pragma: no cover
            try:
                self.license
            except FileNotFoundError:
                raise exceptions.FrozenEditable(self._distribution)

        self._metadata = metadata
        self.name = metadata["name"]
        self.version = self._distribution.version
        self.author = self._metadata["Author"]
        if not self._metadata["Author"]:
            match = re.match("([^<>]+)<([^>]+)>",
                             self._metadata.get("Author-Email", "").strip())
            if match:
                self.author = match[1].strip()
        self.summary = self._metadata["Summary"]
        self.license_name = self._metadata["License"]
        self.url = self._metadata["Home-page"]
        if not self.url and self._metadata["Project-URL"]:
            match = re.search("homepage, (.*)", self._metadata["Project-URL"])
            if match:  # pragma: no branch
                self.url = match[1]

        if self.license_name == "UNKNOWN":
            self.license_name = Placeholder(self.license_name)
        if not self.license_name and self._metadata.get_all("Classifier"):
            classifiers = []
            for classifier in self._metadata.get_all("Classifier"):
                if not classifier.startswith("License"):
                    continue
                classifier = classifier.split("::")[-1].strip()
                classifier = re.sub(r"^[^()]+ \(([^()]+)\)$", r"\1", classifier)
                classifiers.append(classifier)
            self.license_name = " or ".join(classifiers) or self.license_name

    @property
    def license(self):
        out = {}
        for (name, path) in self._license_paths.items():
            out[name] = path.read_text("utf-8")
        return out

    @property
    def url(self) -> str:
        """The distribution's homepage. Defaults to its PyPI page."""
        return self._url

    @url.setter
    def url(self, url):
        if not url or url == "UNKNOWN":
            url = Placeholder(f"https://pypi.org/project/{self.name}")
        self._url = url


def _python_license():
    import sysconfig
    root = sysconfig.get_path("stdlib")
    for name in ["../LICENSE.txt", "../LICENSE", "LICENSE.txt",
                 "LICENSE"]:  # pragma: no branch
        path = Path(root, name)
        if path.exists():  # pragma: no branch
            return path
    raise exceptions.NoPythonLicense()  # pragma: no cover


def collect_dependencies(*top_level):
    from packaging.requirements import Requirement

    to_do = collections.deque()
    for distribution in top_level:
        requirement = Requirement(distribution)
        if requirement.marker is None or requirement.marker.evaluate():
            to_do.append(distribution)

    collected = set()
    while to_do:
        requirement = Requirement(to_do.pop())
        collected.add(requirement.name)
        for dependency in map(
                Requirement,
                importlib_metadata.distribution(requirement.name).requires
                or []):
            if dependency.marker:
                if not dependency.marker.evaluate():
                    if not any(
                            dependency.marker.evaluate({"extra": i})
                            for i in requirement.extras):
                        continue
            to_do.append(str(dependency))
    return collected


python = Component(
    name="Python", version=sys.version.split()[0],
    author="Python Software Foundation", summary="Python is an " \
    "interpreted high-level general-purpose programming language.",
    license_name="PSF 2", license={"": _python_license().read_text("utf-8")},
    url="https://www.python.org")
