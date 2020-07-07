import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import uic

# import .ui file
# .ui file must be located in the same directory as the Python code file.
form_class = uic.loadUiType("CC_Server_GUI.ui")[0]

# GUI Class Define
class WindowClass(QtWidgets.QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.btn_100.setCheckable(True)
        self.btn_100.clicked.connect(self.btn_100_function)

        self.btn_200.setCheckable(True)
        self.btn_200.clicked.connect(self.btn_200_function)

        self.btn_gcp.setCheckable(True)
        self.btn_gcp.clicked.connect(self.btn_gcp_function)

    def btn_100_function(self):
        if self.btn_100.isChecked():
            self.btn_200.setEnabled(False)
            self.btn_gcp.setEnabled(False)
            print("Button 100 Pressed")
        else:
            self.btn_200.setEnabled(True)
            self.btn_gcp.setEnabled(True)
            print("Button 100 Released")

    def btn_200_function(self):
        if self.btn_200.isChecked():
            self.btn_100.setEnabled(False)
            self.btn_gcp.setEnabled(False)
            print("Button 200 Pressed")
        else:
            self.btn_100.setEnabled(True)
            self.btn_gcp.setEnabled(True)
            print("Button 200 Released")

    def btn_gcp_function(self):
        if self.btn_gcp.isChecked():
            self.btn_100.setEnabled(False)
            self.btn_200.setEnabled(False)
            print("Button GCP Pressed")
        else:
            self.btn_100.setEnabled(True)
            self.btn_200.setEnabled(True)
            print("Button GCP Released")


# QApplication : Run App
app = QtWidgets.QApplication(sys.argv)

# Create an instance of WindowClass
myWindow = WindowClass()

# Showing the program screen
myWindow.show()

# Code for entering a program into an event loop (which activates the program)
app.exec_()
