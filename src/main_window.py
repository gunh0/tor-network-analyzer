import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import uic

# import .ui file
# .ui file must be located in the same directory as the Python code file.
form_class = uic.loadUiType("CC_Server_GUI.ui")[0]


class WindowClass(QtWidgets.QMainWindow, form_class):   # GUI Class Define
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.pBtn100_collect.clicked.connect(self.pBtn100_collect_function)

    ip_list = []

    def pBtn100_collect_function(self):
        print("100 Collect Pressed")
        self.ip_list = []
        start_ip_host = int(self.sip1004.text())
        last_ip_host = int(self.lip1004.text())
        for i in range(start_ip_host, last_ip_host+1):
            input_ip = self.sip1001.text()+"."+self.sip1002.text()+"." + \
                self.sip1003.text()+"."+str(i)
            self.ip_list.append(input_ip)
        print("IP List: ", self.ip_list)


# QApplication : Run App
app = QtWidgets.QApplication(sys.argv)

# Create an instance of WindowClass
myWindow = WindowClass()

# Showing the program screen
myWindow.show()

# Code for entering a program into an event loop (which activates the program)
app.exec_()
