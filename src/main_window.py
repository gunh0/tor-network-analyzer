import sys
import time

from threading import Thread
from command import command

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import uic

# import .ui file
# .ui file must be located in the same directory as the Python code file.
form_class = uic.loadUiType("CC_Server_GUI.ui")[0]


class CommandSerize9999(Thread):
    def __init__(self, queue, ip_addr):
        Thread.__init__(self)
        self.queue = queue
        self.ip_addr = ip_addr
        self.port = "9999"

    def run(self):
        while True:
            command_list = self.queue.get()
            if command_list is None:
                break
            for c in range(command_list.qsize()):
                com = command_list.get()
                print(c, ": ", com)
                command(self.ip_addr, self.port, com)
                time.sleep(0.5)
            self.queue.task_done()


class CommandSerize9998(Thread):
    def __init__(self, queue, ip_addr):
        Thread.__init__(self)
        self.queue = queue
        self.ip_addr = ip_addr
        self.port = "9998"

    def run(self):
        while True:
            command_list = self.queue.get()
            if command_list is None:
                break

            for c in range(command_list.qsize()):
                print(c, ": ", com)
                com = command_list.get()
                command(self.ip_addr, self.port, com)

                time.sleep(0.5)
            self.queue.task_done()


class WindowClass(QtWidgets.QMainWindow, form_class):   # GUI Class Define
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.pBtn100_collect.clicked.connect(self.pBtn100_collect_function)

    ip_list = []
    cmd_list = []

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
