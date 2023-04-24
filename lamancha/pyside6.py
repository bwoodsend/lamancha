from ._qt import TermsAndConditions as _Base
from PySide6.QtWidgets import QWidget as _QWidget


class TermsAndConditions(_Base, _QWidget):
    from PySide6 import QtWidgets as _widgets, QtCore as _core, QtGui as _gui


if __name__ == "__main__":
    TermsAndConditions._demo()
