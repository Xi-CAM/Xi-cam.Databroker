from qtpy.QtCore import *
from qtpy.QtGui import *
from qtpy.QtWidgets import *
from xicam.gui.static import path

from xicam.plugins import ListViewSettingsPlugin


class DatabrokerItem(QStandardItem):
    MetadataHostRole = Qt.UserRole
    AssetsHostRole = Qt.UserRole + 1
    MetadataPortRole = Qt.UserRole + 2
    AssetPortRole = Qt.UserRole + 3
    MetadataDatabaseRole = Qt.UserRole + 4
    AssetDatabaseRole = Qt.UserRole + 5


class DatabrokerDialog(QDialog):

    def __init__(self, item: DatabrokerItem):
        super(DatabrokerDialog, self).__init__()

        self.item = item

        # Setup windowframe
        frameGm = self.frameGeometry()
        screen = QApplication.desktop().screenNumber(QApplication.desktop().cursor().pos())
        centerPoint = QApplication.desktop().screenGeometry(screen).center()
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())

        # Setup fields
        self.Name = QLineEdit()
        self.MetadataHost = QLineEdit()
        self.AssetsHost = QLineEdit()
        self.MetadataPort = QLineEdit()
        self.AssetPort = QTextEdit()
        self.MetadataDatabase = QTextEdit()
        self.AssetDatabase = QTextEdit()

        # Setup dialog buttons
        self.addButton = QPushButton("&Ok")
        self.validateButton = QPushButton("&Validate")
        self.cancelButton = QPushButton("&Cancel")
        self.okButton.clicked.connect(self.accept)
        self.validateButton.clicked.connect(self.validate)
        self.cancelButton.clicked.connect(self.close)
        self.buttonboxWidget = QDialogButtonBox()
        self.buttonboxWidget.addButton(self.addButton, QDialogButtonBox.AcceptRole)
        self.buttonboxWidget.addButton(self.simulateButton, QDialogButtonBox.AcceptRole)
        self.buttonboxWidget.addButton(self.cancelButton, QDialogButtonBox.RejectRole)

        # Compose main layout
        mainLayout = QFormLayout()
        mainLayout.addRow('Name', self.Name)
        mainLayout.addRow('Metadata Store Host', self.MetadataHost)
        mainLayout.addRow('Metadata Store Port', self.MetadataPort)
        mainLayout.addRow('Metadata Store Database', self.MetadataDatabase)
        mainLayout.addRow('Asset Store Host', self.AssetHost)
        mainLayout.addRow('Asset Store Port', self.AssetPort)
        mainLayout.addRow('Asset Store Database', self.AssetDatabase)
        mainLayout.addRow(self.buttonboxWidget)

        self.setLayout(mainLayout)
        self.setWindowTitle("Configure Databroker Instance...")

        # Set modality
        self.setModal(True)

    def accept(self):
        # Note: in some circumstance, QStandardItems get re-hydrated from their data values;
        # instance attributes are not safe!
        self.item.setData(Qt.DisplayRole, self.Name.text)
        self.item.setData(self.item.MetadataDatabaseRole, self.MetadataDatabase.text)
        self.item.setData(self.item.MetadataPortRole, self.MetadataPort.text)
        self.item.setData(self.item.MetadataDatabaseRole, self.MetadataDatabase.text)
        self.item.setData(self.item.AssetsHostRole, self.AssetsHost.text)
        self.item.setData(self.item.AssetPortRole, self.AssetPort.text)
        self.item.setData(self.item.AssetDatabaseRole, self.AssetDatabase.text)

        super(DatabrokerDialog, self).accept()

    def validate(self):
        # Test the instance
        ...


class DatabrokerDelegate(QItemDelegate):
    def __init__(self, parent):
        super(DatabrokerDelegate, self).__init__(parent)
        self._parent = parent

    def paint(self, painter, option, index):
        if not self._parent.indexWidget(index):
            button = QToolButton(self.parent(), )
            button.setAutoRaise(True)
            button.setText('Delete Plan')
            button.setIcon(QIcon(path('icons/trash.png')))
            sp = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
            sp.setWidthForHeight(True)
            button.setSizePolicy(sp)
            button.clicked.connect(index.data())

            self._parent.setIndexWidget(index, button)


DatabrokerSettingsPlugin = ListViewSettingsPlugin(DatabrokerItem, DatabrokerDialog, DatabrokerDelegate)
