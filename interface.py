import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QAction, QMessageBox, QVBoxLayout, QCheckBox, QLabel, QScrollArea, QGroupBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot, QSize, Qt
from import_data import make_folder


class HIEApp(QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = 'Head Impact Exposure'
        self.left = 300
        self.top = 300
        self.width = 640
        self.height = 400
        self.initUI()
        self.files = ['pin 173', 'pin 463', 'pin 874']

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu('File')
        settingsMenu = mainMenu.addMenu('Settings')
        portMenu = settingsMenu.addMenu('Port')
        # viewMenu = mainMenu.addMenu('View')
        # searchMenu = mainMenu.addMenu('Search')
        # toolsMenu = mainMenu.addMenu('Tools')
        # helpMenu = mainMenu.addMenu('Help')

        exitButton = QAction(QIcon('exit24.png'), 'Exit', self)
        exitButton.setShortcut('Ctrl+Q')
        exitButton.setStatusTip('Exit application')
        exitButton.triggered.connect(self.close)
        fileMenu.addAction(exitButton)

        portButton = QAction('COM1', self)
        portButton.setStatusTip('Select port')
        portButton.triggered.connect(self.close)
        portMenu.addAction(portButton)

        portButton = QAction('COM2', self)
        portButton.setStatusTip('Select port')
        portButton.triggered.connect(self.close)
        portMenu.addAction(portButton)

        portButton = QAction('COM3', self)
        portButton.setStatusTip('Select port')
        portButton.triggered.connect(self.close)
        portMenu.addAction(portButton)


        button = QPushButton('Search for data', self)
        button.setToolTip('testing buttons')
        button.move(100, 70)
        button.resize(130, 45)
        button.clicked.connect(self.b1_click)

        # self.listUSBs()
        # self.layout = QVBoxLayout()
        # self.layout.addWidget(self.tableWidget)
        # self.setLayout(self.layout)


        # launch = QMessageBox.question(self, 'HIE', 'Launch HIE application and begin searching for data?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        # if launch == QMessageBox.Yes:
        #     self.show()
        # else:
        #     self.close()
        self.show()

    @pyqtSlot()
    def table_click(self):
        print("\n")
        print(self.tableWidget.selectedItems())

    @pyqtSlot()
    def b1_click(self):
        launch = QMessageBox.question(self, 'HIE', 'Launch HIE application and begin searching for data?',
                                      QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if launch == QMessageBox.Yes:
            self.buildPopUp()

    def clickBox(self, state):
        if state == Qt.Checked:
            print("Checked")
        else:
            print("Unchecked")


    def buildPopUp(self):
        self.popUp1 = popUp('Select devices to pull data from:')
        self.popUp1.setGeometry(300, 300, 400, 400)
        self.popUp1.show()



class popUp(QWidget):
    usbList = ['usb1', 'usb2', 'usb3', 'usb4', 'usb5', 'usb6', 'usb7', 'usb8', 'usb9']

    def __init__(self, name, parent=None):
        super().__init__(parent)
        self.name = name
        self.label = QLabel(self.name, self)
        self.initUI()
        # self.checkList = []



    def initUI(self):
        self.checkList = []
        self.selected = []
        self.createLayout_Container()
        self.layout_All = QVBoxLayout(self)
        self.layout_All.addWidget(self.scrollarea)

        button2 = QPushButton('Begin \n Downloading \n Data', self)
        button2.setToolTip('download data')
        button2.move(80, 40)
        button2.resize(130, 55)
        button2.clicked.connect(self.download)

        selectAll = QPushButton('Select All', self)
        selectAll.setToolTip('download data')
        selectAll.move(200, 70)
        selectAll.resize(130, 45)
        selectAll.clicked.connect(self.checkAll)

        deselectAll = QPushButton('Deselect All', self)
        deselectAll.setToolTip('download data')
        deselectAll.move(300, 70)
        deselectAll.resize(130, 45)
        deselectAll.clicked.connect(self.uncheckAll)


        self.show()

    def createLayout_group(self, number):
        sgroupbox = QGroupBox("Identified USBs", self)
        layout_groupbox = QVBoxLayout(sgroupbox)
        for i in range(len(self.usbList)):
            item = QCheckBox(self.usbList[i], sgroupbox)
            layout_groupbox.addWidget(item)
            self.checkList.append(item)
            print(len(self.checkList))
        layout_groupbox.addStretch(1)
        for x in range(len(self.checkList)):
            op1 = self.checkList[x]
            op1.stateChanged.connect(self.pickPort)
        return sgroupbox

    def createLayout_Container(self):
        self.scrollarea = QScrollArea(self)
        self.scrollarea.setFixedWidth(250)
        self.scrollarea.setFixedHeight(200)
        self.scrollarea.setWidgetResizable(True)

        widget = QWidget()
        self.scrollarea.setWidget(widget)
        self.layout_SArea = QVBoxLayout(widget)

        for i in range(1):
            self.layout_SArea.addWidget(self.createLayout_group(i))
        self.layout_SArea.addStretch(1)

    def pickPort(self, state):
        if state == Qt.Checked:
            print("Checked")
        else:
            print("Unchecked")

    def checkAll(self):
        for x in range(len(self.checkList)):
            op1 = self.checkList[x]
            op1.setChecked(True)

    def uncheckAll(self):
        for x in range(len(self.checkList)):
            op1 = self.checkList[x]
            op1.setChecked(False)

    @pyqtSlot()
    def download(self):
        self.getChecked()
        self.buildStatusWindow()
        self.close()

    def getChecked(self):
        # selected = []
        print('in getchecked')
        print(len(self.checkList))
        for x in range(len(self.checkList)):
            print('in for loop')
            op1 = self.checkList[x]
            if op1.isChecked():
                self.selected.append(op1)
                print(op1)

    def buildStatusWindow(self):
        print(len(self.selected))
        self.status1 = StatusWindow()
        self.status1.setGeometry(300, 300, 400, 400)
        self.status1.show()


class StatusWindow(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.title = 'Head Impact Exposure'
        self.left = 300
        self.top = 300
        self.width = 640
        self.height = 400
        self.initUI()
        # self.downloadingList = downList


    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.doneDownload = True
        self.downloadinglist = ['fake1', 'fake2']
        locx = 50
        locy = 50
        b = QLabel(self)
        b.setText("Downloading data from:")
        b.move(locx, locy)

        for y in range(len(self.downloadinglist)):
            locy += 50
            c = QLabel(self)
            c.setText(str(self.downloadinglist[y]))
            c.move(locx, locy)

        # print(len(self.downloadingList))

        cancelButton = QPushButton('Cancel', self)
        cancelButton.setToolTip('download data')
        cancelButton.move(self.width / 2 - 40, 40)
        cancelButton.resize(130, 55)
        cancelButton.clicked.connect(self.cancelDownload)

        while not self.doneDownload:
            # notice that downloading from usbs X, y, z
            self.show()

        self.complete()
        self.close()

    def complete(self):
        # opens next window showing completed downloads and option to delete
        self.close()

    def cancelDownload(self):
        # whatever needs to happen to stop download on server side
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = HIEApp()
    sys.exit(app.exec())
