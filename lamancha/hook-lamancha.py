import sys

from lamancha._collection import _python_license

source = _python_license()

datas = [
    (str(source), str(source.parent.relative_to(sys.base_prefix))),
]
