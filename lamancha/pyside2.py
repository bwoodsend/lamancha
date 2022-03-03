from ._qt import TermsAndConditions as _Base
from PySide2.QtWidgets import QWidget as _QWidget


class TermsAndConditions(_Base, _QWidget):
    from PySide2 import QtWidgets as _widgets, QtCore as _core, QtGui as _gui
