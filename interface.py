import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QAction, QMessageBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
from import_data import make_folder

class HIEApp(QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = 'Head Impact Exposure'
        self.left = 100
        self.top = 100
        self.width = 640
        self.height = 400
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu('File')
        editMenu = mainMenu.addMenu('Edit')
        viewMenu = mainMenu.addMenu('View')
        searchMenu = mainMenu.addMenu('Search')
        toolsMenu = mainMenu.addMenu('Tools')
        helpMenu = mainMenu.addMenu('Help')

        exitButton = QAction(QIcon('exit24.png'), 'Exit', self)
        exitButton.setShortcut('Ctrl+Q')
        exitButton.setStatusTip('Exit application')
        exitButton.triggered.connect(self.close)
        fileMenu.addAction(exitButton)

        button = QPushButton('create new folder', self)
        button.setToolTip('testing buttons')
        button.move(100, 70)
        button.resize(130, 45)
        button.clicked.connect(self.b1_click)

        launch = QMessageBox.question(self, 'HIE', 'Launch HIE application and begin searching for data?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if launch == QMessageBox.Yes:
            self.show()
        else:
            self.close()

        # self.show()

    @pyqtSlot()
    def b1_click(self):
        make_folder('fakelocation', 'fakename')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = HIEApp()
    sys.exit(app.exec())
