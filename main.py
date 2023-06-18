
import sys
import os
import time

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.uic import loadUiType
from PyQt5.QtGui import QPixmap
from utils.my_connector import connector
from app import MainApp

login,_ = loadUiType(os.path.join(os.path.dirname(__file__), 'view/login.ui'))

# pyrcc5 resource.qrc -o resource_rc.py
 
class Login(QWidget , login):
    def __init__(self):
        QWidget.__init__(self)
        self.setupUi(self)
        self.pushButton.clicked.connect(self.login)
        path = os.path.join(os.path.dirname(__file__), 'resources/styles/darkorange.css')
        style = open(path , 'r')
        style = style.read()
        self.setStyleSheet(style)

    def login(self):
        self.db = connector
        self.cur = self.db.cursor()

        username = self.lineEdit.text()
        password = self.lineEdit_2.text()

        sql = ''' SELECT * FROM kullanıcılar '''

        self.cur.execute(sql)
        data = self.cur.fetchall()
        for row in data  :
            try:
                if ( int(username) == row[0] or username == row[7]) and password == row[1]:
                    print('Kullanıcı Eşleşti')
                    self.window2 = MainApp()
                    self.close()
                    self.window2.show()
            except:
                self.label.setText('Hatalı giriş yapıldı')


def main():
    app = QApplication(sys.argv)
    window = Login()
    window.show()
    app.exec_()

if __name__ == '__main__':
    main()
    # window = MainApp()
    # window.show()
    # app.exec_()



