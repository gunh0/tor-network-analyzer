import sys
import time

from queue import Queue
from threading import Thread
from command import command
from command import make_moz_cmd_list, make_tbb_cmd_list, make_copy_cmd_list, cmd_cmd_list, exit_cmd_list, watch_cmd_list

import file_open_easygui as fopen

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import uic

from tkinter import Tk, Listbox, Label

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
                com = command_list.get()
                print(c, ": ", com)
                command(self.ip_addr, self.port, com)

                time.sleep(0.5)
            self.queue.task_done()


class WindowClass(QtWidgets.QMainWindow, form_class):   # GUI Class Define
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # 100 Tab Func.
        self.pBtnSet100ip.clicked.connect(self.pBtnSet100ip_function)
        self.pBtn100_collect.clicked.connect(self.pBtn100_collect_function)
        self.pBtn100_cmd.clicked.connect(self.pBtn100_cmd_function)

        # 200 Tab Func.
        self.pBtnSet200ip.clicked.connect(self.pBtnSet200ip_function)
        self.pBtn200_watch.setEnabled(False)

        # GCP Tab Func.
        self.gcp_ipListPath.setText(
            "D:\\Tor_CIFS_300\\Source\\data\\ipList.txt")

    # Share
    ip_list = []
    cmd_list = []
    taskQueue = Queue()
    thread_list = []

    # 100 Tab Function
    def pBtnSet100ip_function(self):
        print("100 IP List Set")
        self.ip_list = []   # init. list
        start_ip_host = int(self.sip1004.text())
        last_ip_host = int(self.lip1004.text())
        for i in range(start_ip_host, last_ip_host+1):
            input_ip = self.sip1001.text()+"."+self.sip1002.text()+"." + \
                self.sip1003.text()+"."+str(i)
            self.ip_list.append(input_ip)
        print("IP List: ", self.ip_list)

        tkWindow = Tk()
        tkWindow.geometry("220x200")
        tkWindow.title("IP LIST")
        labeltxt = "Number of Collectors: "+str(len(self.ip_list))
        tkLabel = Label(tkWindow, text=labeltxt)
        tkLabel.pack()
        ipListBox = Listbox(tkWindow)
        for i in range(0, len(self.ip_list)):
            ipListBox.insert(i+1, self.ip_list[i])
        ipListBox.pack()
        tkWindow.mainloop()

    def pBtn100_collect_function(self):
        print("100 Collect Pressed")

    def pBtn100_cmd_function(self):
        print("100 CMD Sending Pressed")

        send_command = self.cmd100.text()
        for i in self.ip_list:
            print(i, self.ip_list[i])
            self.cmd_list.append(cmd_cmd_list(send_command))

        for item in self.cmd_list:
            self.taskQueue.put(item)

        for ip_addr in self.ip_list:
            t = CommandSerize9998(self.taskQueue, ip_addr)
            t.start()
        self.taskQueue.join()
        print(self.taskQueue)

        for i in range(len(self.ip_list)):
            self.taskQueue.put(None)

        for t in self.thread_list:
            t.join()

        print("100 CMD Sending Finish")
        
    # 200 Tab Function
    def pBtnSet200ip_function(self):
        print("200 IP List Set")
        self.ip_list = []   # init. list
        start_ip_host = int(self.sip2004.text())
        last_ip_host = int(self.lip2004.text())
        for i in range(start_ip_host, last_ip_host+1):
            input_ip = self.sip2001.text()+"."+self.sip2002.text()+"." + \
                self.sip2003.text()+"."+str(i)
            self.ip_list.append(input_ip)
        print("IP List: ", self.ip_list)

        tkWindow = Tk()
        tkWindow.geometry("220x200")
        tkWindow.title("IP LIST")
        labeltxt = "Number of Collectors: "+str(len(self.ip_list))
        tkLabel = Label(tkWindow, text=labeltxt)
        tkLabel.pack()
        ipListBox = Listbox(tkWindow)
        for i in range(0, len(self.ip_list)):
            ipListBox.insert(i+1, self.ip_list[i])
        ipListBox.pack()
        tkWindow.mainloop()

# QApplication : Run App
app = QtWidgets.QApplication(sys.argv)

# Create an instance of WindowClass
myWindow = WindowClass()

# Showing the program screen
myWindow.show()

# Code for entering a program into an event loop (which activates the program)
app.exec_()
