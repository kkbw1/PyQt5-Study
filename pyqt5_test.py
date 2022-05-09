from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
import sys

WINDOW_POS_X = 400
WINDOW_POS_Y = 100

WIDTH_720P = 1280
LENGTH_720P = 720

# def on_button_clicked():
#     alert = QMessageBox()
#     alert.setText('Clicked!!')
#     alert.exec()


class mainWindow(QMainWindow):
    def __init__(self):
        super(mainWindow, self).__init__()
        self.init_ui()

    def init_ui(self):
        self.setGeometry(WINDOW_POS_X, WINDOW_POS_Y, WIDTH_720P, LENGTH_720P)
        self.setWindowTitle('Main Window')

        self.label = QtWidgets.QLabel(self)
        self.label.setText('Label')
        self.label.move(50, 50)

        self.button = QtWidgets.QPushButton(self)
        self.button.setText('Click')
        self.button.clicked.connect(self.buttonClicked)
        self.button.move(50, 100)

        self.textEdit = QTextEdit()
        # self.textEdit.clicked.connect(self.textEditClicked)
        self.textEdit.move(100, 50)

    def keyPressEvent(self, event):
        pressedKey = event.key()
        qtKey = Qt.Key(pressedKey)
        qtKeySpace = Qt.Key_Space
        if qtKey == Qt.Key_Space:
            print("Space")
        elif qtKey == Qt.Key_Enter or qtKey == Qt.Key_Return:
            print("Enter")
        elif qtKey == Qt.Key_Backspace:
            print("Backspace")

    def buttonClicked(self):
        alert = QMessageBox()
        alert.setText('Clicked')
        alert.exec()


if __name__ == "__main__":
    app = QApplication([])

    wind = mainWindow()
    wind.show()

    sys.exit(app.exec_())
