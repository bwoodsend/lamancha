class Egg(Exception):

    def __init__(self, distribution):
        self.distribution = distribution

    def __str__(self):
        return f"""
Distribution '{self.distribution.project_name}' located at:
    {self.distribution.location}
is in the legacy EGG format which does not include licenses. \
To fix this install 'wheel' then reinstall this distribution.
    pip install wheel
    pip uninstall {self.distribution.project_name}
    pip install {self.distribution.project_name}

If you installed this distribution via the deprecated:
    python setup.py install
then instead use:
    pip install .
"""


class FrozenEditable(Exception):
    __init__ = Egg.__init__

    def __str__(self):  # pragma: no cover
        return f"""
Distribution '{self.distribution.project_name}' located at:
    {self.distribution.location}
appears to have been in an editable install format which unfortunately loses \
its license in the process of freezing.
"""


class NoLicense(Exception):

    def __init__(self, distribution):
        self.distribution = distribution

    def __str__(self):
        return f"""
Distribution '{self.distribution.project_name}' located at:
    {self.distribution.location}
appears not to have a license.
"""


class NoPythonLicense(NoLicense):

    def __init__(self):  # pragma: no cover
        pass

    def __str__(self):  # pragma: no cover
        return "Python's license could not be found. If your Python " \
               "distribution does ship its license then this is a bug. Please" \
               " report it at https://github.com/bwoodsend/lamancha/issues " \
               "explaining how you installed Python."
