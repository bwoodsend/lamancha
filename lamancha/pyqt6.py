from ._qt import TermsAndConditions as _Base
from PyQt6.QtWidgets import QWidget as _QWidget


class TermsAndConditions(_Base, _QWidget):
    from PyQt6 import QtWidgets as _widgets, QtCore as _core, QtGui as _gui
