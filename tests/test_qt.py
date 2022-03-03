import os
import importlib

import pkg_resources

import lamancha

qt = os.environ.get("QT_VARIANT", "pyqt5")
lamancha_qt = importlib.import_module("lamancha." + qt)
QtWidgets = lamancha_qt.TermsAndConditions._widgets
QtCore = lamancha_qt.TermsAndConditions._core

qapp = QtWidgets.QApplication.instance() or QtWidgets.QApplication([])


def test_terms_and_conditions():
    dependencies = [
        lamancha.python,
        *map(lamancha.Distribution, pkg_resources.require("lamancha")),
    ]
    self = lamancha_qt.TermsAndConditions(dependencies)

    self.show()
    assert self.body.toPlainText()

    _check_fits_on_screen(self)
    qapp.processEvents()
    _check_fits_on_screen(self)
    assert centering(self) < .01

    for i in range(self.list.rowCount()):
        self.list.selectRow(i)
        qapp.processEvents()
        _check_fits_on_screen(self)
        assert centering(self) < .1

    self.close()


def _check_fits_on_screen(self: lamancha_qt.TermsAndConditions):
    screen = self.screen().size()
    rect = self.rect().translated(self.pos())

    assert rect.width() < 1200
    assert rect.height() < 800
    if rect.width() < screen.width():
        assert 0 < rect.left() < rect.right() < screen.width()
    if rect.height() < screen.height():
        assert 0 < rect.top() < rect.bottom() < screen.height()

    assert not self.list.horizontalScrollBar().isVisible()
    assert not self.body.horizontalScrollBar().isVisible()


def centering(self: lamancha_qt.TermsAndConditions):
    screen_center = self.screen().size() / 2
    screen_center = QtCore.QPoint(screen_center.width(), screen_center.height())
    mismatch = self.rect().translated(self.pos()).center() - screen_center
    return mismatch.manhattanLength() / max(self.height(), self.width())
