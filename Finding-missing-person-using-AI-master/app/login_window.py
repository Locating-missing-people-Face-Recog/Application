import json
import sys

import requests
from PyQt5 import QtGui
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QIcon, QPixmap, QStandardItem, QStandardItemModel
from PyQt5.QtWidgets import (QApplication, QLabel, QLineEdit, QListView,
                             QListWidget, QMainWindow, QMessageBox,
                             QPushButton)

from app_window import AppWindow


class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = "Login"
        self.width = 800
        self.height = 600
        self.URL = "http://localhost:8000"
        self.icon_path = '../resources/icon.png'
        self.username = None
        self.password = None

        self.initialize()

    def initialize(self):
        self.setWindowIcon(QtGui.QIcon(self.icon_path))
        self.setWindowTitle(self.title)
        self.setFixedSize(self.width, self.height)
        self.get_username()
        self.get_password()

        login_bt = QPushButton("Login", self)
        login_bt.move(340, 250)
        login_bt.clicked.connect(self.login)

        self.show()

    def get_username(self):
        username_label = QLabel(self)
        username_label.setText("Username: ")
        username_label.move(190, 90)

        self.username = QLineEdit(self)
        self.username.move(370, 170)
    
    def get_password(self):
        password_label = QLabel(self)
        password_label.setText("Password: ")
        password_label.move(190, 200)

        self.password = QLineEdit(self)
        self.password.setEchoMode(QLineEdit.Password)
        self.password.move(370, 200)
    
    def login(self):
        if not self.password.text() or not self.username.text():
            QMessageBox.about(self, "Error", "\nPlease fill all entries\t\n")
        else:
            try:
                login_status = requests.get(self.URL+'/login?username='+
                                        self.username.text()+
                                        '&password='+self.password.text())
                login_status = json.loads(login_status.text)
                if login_status.get('status', False):
                    self.app_window = AppWindow(user=self.username.text())
                else:
                    QMessageBox.about(self, "Login Failed", "\nPlease try again\t\n")
            except requests.exceptions.ConnectionError:
                QMessageBox.about(self, "Conenction Error", "\nDatabase is not running\t\n")

        


app = QApplication(sys.argv)
style = """
        QWidget{
            background:#F5F5DC;
        }
        QLabel{
            color: Brown;
            font-size: 25px;
        }
        QListView
        {
            background: #7e959e;
        }
        QLabel#round_count_label, QLabel#highscore_count_label{
            border: 1px solid #fff;
            border-radius: 8px;
            padding: 2px;
        }
        QPushButton
        {
            color: white;
            background: #0577a8;
            border: 1px #DADADA solid;
            padding: 5px 10px;
            border-radius: 2px;
            font-weight: bold;
            font-size: 9pt;
            outline: none;
        }
        QPushButton:hover{
            border: 1px #C6C6C6 solid;
            color: #fff;
            background: #0892D0;
        }
        QLineEdit {
            padding: 1px;
            color: #fff;
            border-style: solid;
            border: 2px solid #fff;
            border-radius: 8px;
        }
    """
app.setStyleSheet(style)
w = LoginWindow()
sys.exit(app.exec())
