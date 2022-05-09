from PySide2 import QtWidgets
from PySide2 import QtGui
from PySide2.QtCore import Qt
from PySide2.QtWidgets import *
# from PySide2.QtUiTools import QUiLoader
import sys

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

    def setNewData(self, newData):
        self.data = newData
        allRowCounts = []
        for key, value in self.data.items():
            allRowCounts.append(len(value))
        self.rowCount = max(allRowCounts)
        self.columnCount = len(self.data)

    def setDataToTableView(self):
        self.setRowCount(self.rowCount)
        self.setColumnCount(self.columnCount)

        colHeaders = []
        for n, key in enumerate(sorted(self.data.keys())):
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
        self.label.move(50, 50)

        # lineEdit
        self.lineEdit = QLineEdit(self)
        self.lineEdit.returnPressed.connect(self.lineEditReturnPressed)
        self.lineEdit.move(50, 100)
        self.lineEdit.setFixedWidth(200)

        # button
        self.button = QtWidgets.QPushButton(self)
        self.button.setText('Click to change table data')
        self.button.clicked.connect(self.buttonClicked)
        self.button.move(50, 200)
        self.button.setFixedWidth(200)

        # table
        self.tableView = TableView(self)
        self.tableView.move(50, 300)
        self.tableView.setFixedWidth(900)
        self.tableView.setFixedHeight(400)
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


if __name__ == "__main__":
    print('main')

    app = QApplication([])

    wind = MainWindow()
    wind.show()

    sys.exit(app.exec_())
