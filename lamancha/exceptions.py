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


class NoLicense(Exception):

    def __init__(self, distribution):
        self.distribution = distribution

    def __str__(self):
        return f"""
Distribution '{self.distribution.project_name}' located at:
    {self.distribution.location}
appears not to have a license.
"""
