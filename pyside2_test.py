import json
import os.path
import sys
from collections import OrderedDict

from PySide2 import QtGui
from PySide2 import QtWidgets
from PySide2.QtCore import Qt
from PySide2.QtGui import QPixmap
from PySide2.QtWidgets import *

from PIL import Image

# from PySide2.QtUiTools import QUiLoader


WINDOW_POS_X = 400
WINDOW_POS_Y = 100

WIDTH_720P = 1280
LENGTH_720P = 720

tableData = {'col1': ['1111', '2', '3', '4', '5', '6', '7', '8', '9', '10'],
             'col2': ['1', '2', '1', '3', '4'],
             'col3': ['1', '1', '2', '1', '0']}

anotherTableData = {'data1': ['a', 'b', 'c', 'd'],
                    'data2': ['q', 'w', 'e', 'r', 't']}


class TableView(QTableWidget):
    def __init__(self, parent):
        QTableWidget.__init__(self, parent)

        self.data = 0
        self.rowCount = 0
        self.columnCount = 0

    def setNewDataFromEtradeJsonList(self, jsonList):
        # dictHeaderList = ['id', 'epoch', 'date', 'type', 'amount', 'symbol', 'quantity', 'price']
        dictHeaderList = ['date', 'type', 'amount', 'symbol', 'quantity', 'price']
        etradeTransactions = OrderedDict()
        for head in dictHeaderList:
            etradeTransactions[head] = []

        for jsonItem in jsonList:
            for head in dictHeaderList:
                if head in jsonItem is not None:
                    if head == 'date':
                        dateSubstr = jsonItem[head][:10]
                        etradeTransactions[head].append(dateSubstr)
                    elif head == 'amount' or head == 'quantity' or head == 'price':
                        valueStr = str(jsonItem[head])
                        etradeTransactions[head].append(valueStr)
                    else:
                        etradeTransactions[head].append(jsonItem[head])
                else:
                    etradeTransactions[head].append('')
        # print()
        # print(etradeTransactions)

        self.setNewData(etradeTransactions)
        self.setDataToTableView()

    def setNewData(self, newData):
        self.data = newData
        allRowCounts = []
        for key, value in self.data.items():
            allRowCounts.append(len(value))
        self.rowCount = max(allRowCounts)
        self.columnCount = len(self.data)

    def setDataToTableView(self, headerSort=False):
        self.setRowCount(self.rowCount)
        self.setColumnCount(self.columnCount)

        colHeaders = []
        dataKeys = sorted(self.data.keys()) if headerSort else self.data.keys()
        for n, key in enumerate(dataKeys):
            colHeaders.append(key)
            rowData = self.data[key]
            for m, item in enumerate(rowData):
                newItem = QTableWidgetItem(item)
                self.setItem(m, n, newItem)

        self.setHorizontalHeaderLabels(colHeaders)
        self.resizeColumnsToContents()
        self.resizeRowsToContents()


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.init_ui()

    def init_ui(self):
        self.setGeometry(WINDOW_POS_X, WINDOW_POS_Y, WIDTH_720P, LENGTH_720P)
        self.setWindowTitle('Main Window')

        # label
        self.label = QtWidgets.QLabel(self)
        self.label.setText('Label')
        self.label.move(50, 10)

        # lineEdit
        self.lineEdit = QLineEdit(self)
        self.lineEdit.returnPressed.connect(self.lineEditReturnPressed)
        self.lineEdit.move(50, 30)
        self.lineEdit.setFixedWidth(200)

        # button
        self.button = QtWidgets.QPushButton(self)
        self.button.setText('Click to change table data')
        self.button.clicked.connect(self.buttonClicked)
        self.button.move(50, 100)
        self.button.setFixedWidth(200)

        # open file dialog button
        self.button = QtWidgets.QPushButton(self)
        self.button.setText('Open JSON transactions')
        self.button.clicked.connect(self.openFileDialog)
        self.button.move(50, 150)
        self.button.setFixedWidth(200)

        # image choose file dialog button
        self.imageButton = QtWidgets.QPushButton(self)
        self.imageButton.setText('Open Image')
        self.imageButton.clicked.connect(self.openImageFD)
        self.imageButton.move(250, 150)
        self.imageButton.setFixedWidth(200)

        # table
        self.tableView = TableView(self)
        self.tableView.move(50, 200)
        self.tableView.setFixedWidth(600)
        self.tableView.setFixedHeight(500)
        self.tableView.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableView.setNewData(tableData)
        self.tableView.setDataToTableView()

    def keyPressEvent(self, event):
        pressedKey = event.key()
        qtKey = Qt.Key(pressedKey)
        qtKeySpace = Qt.Key_Space
        if qtKey == Qt.Key_Space:
            print("Space")
        elif qtKey == Qt.Key_Enter or qtKey == Qt.Key_Return:
            print("Enter")
            # QLineEdit.keyPressEvent(self, event)
        elif qtKey == Qt.Key_Backspace:
            print("Backspace")

    def lineEditReturnPressed(self):
        print('LineEdit Pressed Return')
        self.label.setText(self.lineEdit.text())

    def buttonClicked(self):
        self.tableView.setNewData(anotherTableData)
        self.tableView.setDataToTableView()

        alert = QMessageBox()
        alert.setText('Clicked')
        alert.exec()

    def openFileDialog(self):
        print('openFileDialog')
        fileDialog = QFileDialog()
        fileDialog.setFileMode(QFileDialog.AnyFile)
        fileDialog.setNameFilter('Json (*.json)')
        if fileDialog.exec_():
            print('exec')
            selectedFiles = fileDialog.selectedFiles()
            if len(selectedFiles) == 0:
                return

            jsonList = []
            jsonFilePath = selectedFiles[0]
            jsonFileOut = open(jsonFilePath, 'r')
            jsonFileData = json.load(jsonFileOut)
            for jsonItem in jsonFileData:
                jsonList.append(jsonItem)
                print(jsonItem)

            self.tableView.setNewDataFromEtradeJsonList(jsonList)

        else:
            print('not exec???')

    def openImageFD(self):
        print('openImageFileDialog')
        imageFD = QFileDialog()
        imageFD.setFileMode(QFileDialog.AnyFile)
        imageFD.setNameFilter('Images (*.png *.jpg *.jpeg)')
        if imageFD.exec_():
            selectedFiles = imageFD.selectedFiles()
            if len(selectedFiles) == 0:
                return

            print(selectedFiles)

            picWidth, picHeight = Image.open(selectedFiles[0]).size
            picRatioWH = picWidth / picHeight
            print(picWidth)
            print(picHeight)

            dlgWidth = 1500
            dlg = CustomPictureDialog()
            dlg.setSize(dlgWidth, dlgWidth / picRatioWH)
            dlg.setPicture(selectedFiles[0], picWidth, picHeight)
            dlg.exec()


class CustomPictureDialog(QDialog):
    def __init__(self):
        super(CustomPictureDialog, self).__init__()

        self.dialogHeight = None
        self.dialogWidth = None

        self.pictureHeight = None
        self.pictureWidth = None
        self.pictureRatio = None

        self.setWindowTitle('CustomPictureDialog')

        # label
        self.pixmapLabel = QtWidgets.QLabel(self)
        self.pixmapLabel.move(0, 0)

    def setSize(self, width, height):
        self.setGeometry(WINDOW_POS_X + 10, WINDOW_POS_Y + 10, width, height)
        self.dialogWidth = width
        self.dialogHeight = height

    def setPicture(self, path, width, height):
        self.setWindowTitle(os.path.basename(path))

        self.pictureWidth = width
        self.pictureHeight = height
        self.pictureRatio = width / height

        self.pixmap = QPixmap(path)
        self.pixmapLabel.setPixmap(self.pixmap)
        self.pixmapLabel.setFixedWidth(self.dialogWidth)
        self.pixmapLabel.setFixedHeight(self.dialogWidth / self.pictureRatio)
        self.pixmapLabel.setScaledContents(True)

    def resizeEvent(self, event):
        dlgSize = event.size()
        self.pixmapLabel.setFixedWidth(dlgSize.width())
        self.pixmapLabel.setFixedHeight(dlgSize.width() / self.pictureRatio)


if __name__ == "__main__":
    print('main')

    app = QApplication()

    wind = MainWindow()
    wind.show()

    sys.exit(app.exec_())
