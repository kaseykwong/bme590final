import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QAction, QMessageBox, QVBoxLayout, QCheckBox, QLabel, QScrollArea, QGroupBox, QDesktopWidget, QGridLayout
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import pyqtSlot, QSize, Qt
import import_data
import server


class HIEApp(QMainWindow):
    """
    Class for the main application window -- serves as homepage
    """

    def __init__(self):
        """
        Function that initiates the main window
        """
        super().__init__()
        self.title = 'Head Impact Exposure'
        self.initUI()

    def initUI(self):
        """
        Function initializes the user interface for the main window

        Returns:
            QMainWindow: home screen with button to begin searching for data

        """
        self.setWindowTitle(self.title)
        self.setFixedHeight(600)
        self.setFixedWidth(800)
        findCenter = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        findCenter.moveCenter(centerPoint)
        self.move(findCenter.topLeft())

        pal = self.palette()
        pal.setColor(self.backgroundRole(), Qt.darkCyan)
        self.setPalette(pal)

        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu('File')

        helpButton = QAction('Help', self)
        helpButton.setStatusTip('Need assistance?')
        helpButton.setShortcut('Ctrl+H')
        helpButton.triggered.connect(self.helpInfo)
        fileMenu.addAction(helpButton)

        exitButton = QAction(QIcon('exit24.png'), 'Exit', self)
        exitButton.setShortcut('Ctrl+Q')
        exitButton.setStatusTip('Exit application')
        exitButton.triggered.connect(self.close)
        fileMenu.addAction(exitButton)

        font1 = QFont()
        font1.setBold(True)
        font1.setPointSize(18)

        button = QPushButton('Search for Data', self)
        button.setToolTip('Find Devices')
        button.setStyleSheet("background-color: white; color: blue")
        button.setFont(font1)
        button.move(250, 355)
        button.resize(300, 45)
        button.clicked.connect(self.b1_click)


        b = QLabel(self)
        b.setText('This application can be used as a multi-unit \ndownloading, '
                  'logging, and storage \nmanagement for the DASHR head impact \n'
                  'exposure sensor. \nClick below to get started.')
        b.setFont(font1)
        b.setStyleSheet("color: white")
        b.resize(720, 300)
        b.move(40, 40)

        self.show()

    @pyqtSlot()
    def helpInfo(self):
        """
        Function creates message box with information on how to use application

        Returns:
            QMessageBox: with info on how to use application

        """
        QMessageBox.question(self, 'Info', 'To begin, click on the Search for Data button.  You will then be '
                                   'prompted to select devices to pull data from.  Click the Begin '
                                   'Downloading Data button to begin transferring files from the devices '
                                   'to the database.', QMessageBox.Close, QMessageBox.Close)

    @pyqtSlot()
    def b1_click(self):
        """
        Function creates message box to confirm user is ready to begin

        Returns:
            QMessageBox: asking the user to confirm that all necessary devices are connected

        """
        launch = QMessageBox.question(self, 'Ready?', 'Are all of the necessary devices plugged in?',
                                      QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if launch == QMessageBox.Yes:
            self.buildPopUp()

    def buildPopUp(self):
        """
        Function initiates the creation of the next pop-up window

        Returns:
            popUp: window prompting user to select devices to import from
        """
        self.popUp1 = popUp()
        self.popUp1.show()


class popUp(QWidget):
    """
    Class for pop-up window prompting user to select devices to download from
    """
    def __init__(self):
        """
        Function that initiates the pop-up window
        """
        super().__init__()

        font3 = QFont()
        font3.setBold(True)
        font3.setPointSize(12)

        b = QLabel(self)
        b.setText('Select devices to download data from:')
        b.setFont(font3)
        b.resize(400, 20)
        b.move(20, 20)
        self.usbList = ['usb1', 'usb2', 'usb3', 'usb4', 'usb5', 'usb6', 'usb7', 'usb8', 'usb9',
                        'usb1', 'usb2', 'usb3', 'usb4', 'usb5', 'usb6', 'usb7', 'usb8', 'usb9',
                        'usb1', 'usb2', 'usb3', 'usb4', 'usb5', 'usb6', 'usb7', 'usb8', 'usb9',
                        'usb1', 'usb2', 'usb3', 'usb4', 'usb5', 'usb6', 'usb7', 'usb8', 'usb9']
        # self.usbList = []
        # self.usbList = import_data.find_usb()
        # self.usbList = ["rep_data"]
        # if self.usbList is []:
        #     QMessageBox.question(self, 'Info', 'No devices detect.  Please check that they are'
        #                                        'plugged in a try again.', QMessageBox.Close, QMessageBox.Close)
        # else:

        print(self.usbList)
        self.setFixedWidth(600)
        self.setFixedHeight(500)
        findCenter = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        findCenter.moveCenter(centerPoint)
        self.move(findCenter.topLeft())
        self.initUI()

    def initUI(self):
        """
        Function that initiates the user interface for the pop-up window

        Returns:
            QWindow: lets users select devices to pull from

        """
        self.checkList = []
        self.selected = []
        self.namesSelected = []
        self.createLayout_Container()
        self.layout_All = QVBoxLayout(self)
        self.layout_All.addWidget(self.scrollarea)

        pal = self.palette()
        pal.setColor(self.backgroundRole(), Qt.white)
        self.setPalette(pal)

        font2 = QFont()
        font2.setBold(True)
        font2.setPointSize(10)

        button2 = QPushButton('Begin \n Downloading \n Data', self)
        button2.setToolTip('download data')
        button2.setStyleSheet("background-color: green; color: white")
        button2.setFont(font2)
        button2.move(450, 380)
        button2.resize(130, 70)
        button2.clicked.connect(self.download)

        selectAll = QPushButton('Select All', self)
        selectAll.setToolTip('download data')
        selectAll.setFont(font2)
        selectAll.move(450, 90)
        selectAll.resize(130, 45)
        selectAll.clicked.connect(self.checkAll)

        deselectAll = QPushButton('Deselect All', self)
        deselectAll.setToolTip('download data')
        deselectAll.setFont(font2)
        deselectAll.move(450, 140)
        deselectAll.resize(130, 45)
        deselectAll.clicked.connect(self.uncheckAll)

        self.show()

    def createLayout_group(self):
        """
        Function creates list of checkboxes for each discovered device

        Returns:
            sgroupbox: a QGroupBox containing the checklist

        """
        sgroupbox = QGroupBox("Identified Devices", self)
        layout_groupbox = QVBoxLayout(sgroupbox)
        for i in range(len(self.usbList)):
            item = QCheckBox(self.usbList[i], sgroupbox)
            layout_groupbox.addWidget(item)
            self.checkList.append(item)
            print(len(self.checkList))
        layout_groupbox.addStretch(1)
        return sgroupbox

    def createLayout_Container(self):
        """
        Function creates a scroll area for the checklist to be presented in

        Returns:
            QScrollArea: on the pop-up window containing checklist of devices

        """
        self.scrollarea = QScrollArea(self)
        self.scrollarea.setFixedWidth(400)
        self.scrollarea.setFixedHeight(400)
        self.scrollarea.setWidgetResizable(True)

        widget = QWidget()
        self.scrollarea.setWidget(widget)
        self.layout_SArea = QVBoxLayout(widget)

        self.layout_SArea.addWidget(self.createLayout_group())
        self.layout_SArea.addStretch(1)

    def checkAll(self):
        """
        Function selects all devices on list

        Returns:
            all checkboxes in Checked state

        """
        for x in range(len(self.checkList)):
            op1 = self.checkList[x]
            op1.setChecked(True)

    def uncheckAll(self):
        """
        Function deselects all devices on list

        Returns:
            all checkboxes not in Checked state

        """
        for x in range(len(self.checkList)):
            op1 = self.checkList[x]
            op1.setChecked(False)

    @pyqtSlot()
    def download(self):
        """
        Function initiates download of data from devices to database

        Returns:
            files transferred to database

        """
        self.getChecked()
        self.buildStatusWindow()
        # [success, bin_files] = import_data.find_folders(self.selected)
        # if success is False:
        #     QMessageBox.question(self, 'No files found', QMessageBox.Ok, QMessageBox.Ok)
        # pins = import_data.get_pins(bin_files)
        # [times, dates, seasons] = import_data.get_creation_date(bin_files)
        # [boolean, binary] = import_data.open_bin_files(bin_files)
        # if boolean is False:
        #     QMessageBox.question(self, 'Unable to properly encode files', QMessageBox.Ok, QMessageBox.Ok)
        # [total, sort_date, sort_pin] = import_data.sort(pins, dates, times, seasons, binary)
        self.close()

    def getChecked(self):
        """
        Function makes a list of all checkboxes/devices that the user selected

        Returns:
            adds all selected devices to self.selected and self.namesSelected

        """
        print('in getchecked')
        print(len(self.checkList))
        for x in range(len(self.checkList)):
            op1 = self.checkList[x]
            if op1.isChecked():
                self.selected.append(op1)
                self.namesSelected.append(self.usbList[x])
                print(op1)

    def buildStatusWindow(self):
        """
        Function calls for the status window to be built

        Returns:
            status window

        """
        print(len(self.selected))
        self.status1 = StatusWindow(self.namesSelected)
        self.status1.show()


class StatusWindow(QWidget):
    """
    Class to create a window that informs the user of the devices data is
        being pulled from during the downloading process
    """

    def __init__(self, list1):
        """
        Function initiates StatusWindow

        Args:
            list1: list containing the names of the devices data is being
                downloaded from
        """
        super().__init__()
        self.selected = list
        self.title = 'Head Impact Exposure'
        self.names = list1
        self.done = QMessageBox
        self.initUI()

    def initUI(self):
        """
        Function initiates the user interface of the status window

        Returns:
            QWindow: containing a list of the devices data is being pulled from

        """
        self.setWindowTitle(self.title)
        self.setFixedWidth(400)
        self.setFixedHeight(500)
        findCenter = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        findCenter.moveCenter(centerPoint)
        self.move(findCenter.topLeft())

        pal = self.palette()
        pal.setColor(self.backgroundRole(), Qt.white)
        self.setPalette(pal)

        font4 = QFont()
        font4.setBold(True)
        font4.setPointSize(10)

        self.doneDownload = False
        print(self.selected)
        locx = 50
        locy = 50
        b = QLabel(self)
        b.setText("Downloading data from:")
        b.setFont(font4)
        b.move(locx, locy)

        for y in range(len(self.names)):
            locy += 20
            c = QLabel(self)
            c.setText(str(self.names[y]))
            c.move(locx, locy)
            if locy > 450:
                locx += 150
                locy = 50

        self.incomplete()
        # check the timing of this without a while loop when actually running
        self.complete()

        # self.complete()
        # if self.done == QMessageBox.Ok:
        #     self.close()

    def incomplete(self):
        """
        Function that shows the downloading list while the downloading is happening

        Returns:
            window with downloading list

        """
        self.show()
        # self.close()

    def complete(self):
        """
        Function that alerts the user when the download has completed

        Returns:
            QMessageBox: with list of devices data was downloaded from

        """
        output = 'Successfuly downloaded data from: \n'
        x = 0
        for i in range(len(self.names)):
            if x <= 3:
                output += str(self.names[i] + '\t')
                x += 1
            else:
                output += str('\n' + self.names[i] + '\t')
                x = 1
        self.done = QMessageBox.question(self, 'Complete', output, QMessageBox.Ok, QMessageBox.Ok)
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = HIEApp()
    sys.exit(app.exec())
