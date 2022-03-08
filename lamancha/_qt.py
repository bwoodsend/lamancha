from textwrap import dedent


def dependency_label(component, QtWidgets):
    self = QtWidgets.QLabel(f'<a href="{component.url}">{component.name}</a>')
    self.component = component
    self.setOpenExternalLinks(True)
    return self


TABLE_STYLE = """
QLabel, QHeaderView::section:horizontal {
  margin-left: '1px';
  margin-right: '1px';
  text-align: center;
}
"""


class TermsAndConditions:
    """A Qt widget for displaying licenses.

    Usage:

        import pkg_resources
        import lamancha.pyqt5

        dependencies = [
            lamancha.python,
            *map(lamancha.Distribution, pkg_resources.require("matplotlib")),
        ]

        licenseWidget = lamancha.pyqt5.TermsAndConditions(dependencies)
        licenseWidget.show()

    """

    def __init__(self, components):
        super().__init__()
        self.setLayout(self._widgets.QHBoxLayout())
        self.components = sorted(components, key=lambda x: x.name.lower())

        left = self._widgets.QVBoxLayout()
        self.layout().addLayout(left)
        left.addWidget(self._widgets.QLabel("<h3>Components</h3>"))
        self.list = type("Table", (Table, self._widgets.QTableWidget), {})()
        self.list.setStyleSheet(TABLE_STYLE)
        self.list.setRowCount(len(self.components))
        self.list.verticalHeader().setVisible(False)
        self.list.setFont(self._gui.QFont("monospace"))
        self.list.setShowGrid(False)
        self.list.setSelectionBehavior(self.list.SelectionBehavior.SelectRows)
        self.list.setSelectionMode(self.list.SelectionMode.SingleSelection)
        left.addWidget(self.list)

        right = self._widgets.QVBoxLayout()
        self.layout().addLayout(right)
        self.description = self._widgets.QLabel()
        right.addWidget(self.description)
        self.body = self._widgets.QTextEdit()
        self.body.setLineWrapMode(self._widgets.QTextEdit.LineWrapMode.NoWrap)
        self.body.setFont(self._gui.QFont("monospace"))
        self.body.setReadOnly(True)
        self.body.setHorizontalScrollBarPolicy(
            self._core.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        right.addWidget(self.body)

        self.list.setColumnCount(3)
        for (i, heading) in enumerate(["Name", "Version", "License"]):
            self.list.setHorizontalHeaderItem(
                i, self._widgets.QTableWidgetItem(heading))

        for (i, component) in enumerate(self.components):
            self.list.setCellWidget(i, 0,
                                    dependency_label(component, self._widgets))
            self.list.setCellWidget(
                i, 1, self._widgets.QLabel(f"v{component.version} "))
            self.list.setCellWidget(
                i, 2, self._widgets.QLabel(component.license_name))

        policy = self.list.sizePolicy()
        policy.setHorizontalPolicy(policy.Policy.Minimum)
        policy.setVerticalPolicy(policy.Policy.MinimumExpanding)
        self.list.setSizePolicy(policy)

        self.list.itemSelectionChanged.connect(self._update_contents)
        self.list.selectRow(0)
        self._update_contents()

    def _update_contents(self):
        """Display the metadata and license body for whichever component is
        selected in the table on the left."""
        for index in self.list.selectedIndexes():  # pragma: no branch
            component = self.list.cellWidget(index.row(), 0).component

            self.description.setText(f"""
                <p style="margin-left: 10px">
                <h3 style="margin:1; padding:1;">{component.name}</h3>
                <div>{component.summary}</div>
                <div><b>Home page</b>:
                    <a href="{component.url}">{component.url}</a>
                </div>
                <div><b>Version</b>: {component.version}</div>
                <div><b>By</b>: {component.author}</div>
            """)
            self.description.setOpenExternalLinks(True)
            self.description.setWordWrap(True)

            text = dedent("\n\n".join(component.license.values()))
            longest_length = max(len(i) for i in text.split("\n"))
            if longest_length > 85:
                self.body.setLineWrapColumnOrWidth(80)
                self.body.setWordWrapMode(
                    self._gui.QTextOption.WrapMode.WordWrap)
                self.body.setLineWrapMode(
                    self.body.LineWrapMode.FixedColumnWidth)
            else:
                self.body.setLineWrapMode(self.body.LineWrapMode.NoWrap)
            self.body.setText(text)
            self.body.setMinimumWidth(
                int(self.body.document().idealWidth() + 20))

            return

    def centerise(self):
        """Set the widget's size and position to sit naturally in the middle of
        the screen."""
        screen = self.screen().size()
        self.setMinimumHeight((screen.height() * 2) // 3)

        size = self.sizeHint()
        self.move(
            int(screen.width() // 2 - size.width() * 0.5),
            int(screen.height() // 2 -
                max(size.height(), self.minimumHeight()) * 0.5))

    def show(self):
        self.centerise()
        super().show()


class Table:
    """A QtWidgets.QTable() subclass which automatically expands to its
    contents."""

    def sizeHint(self):
        """Use exactly the required amount of horizontal space to fit all table
        cells without resorting to abbreviating or scroll bars."""
        self.resizeColumnsToContents()
        self.resizeRowsToContents()
        width = self.verticalHeader().width() + 2
        if self.verticalScrollBar().isVisible():  # pragma: no cover
            width += self.verticalScrollBar().sizeHint().width()
        for i in range(self.columnCount()):
            width += self.columnWidth(i)

        original = super().sizeHint()
        return type(original)(width, original.height())
