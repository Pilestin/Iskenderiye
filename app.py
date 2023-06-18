import os 
# PyQt5 imports for GUI
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.uic import loadUiType

ui, _ = loadUiType(os.path.join(os.path.dirname(__file__), 'view/library_design.ui'))

class MainApp(QMainWindow, ui):
    
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        #self.handle_ui_changes()
        #self.handle_buttons()
        #self.show_books()
        
    def handle_ui_changes(self):
            
        self.setWindowTitle("Kütüphane")
        self.setFixedSize(1000, 600)
        self.tabWidget.tabBar().setVisible(True)
        
    # Button functions
    def handle_buttons(self):
        
        self.pushButton.clicked.connect(self.open_loans_tab)
        self.pushButton_2.clicked.connect(self.open_books_tab)
        self.pushButton_3.clicked.connect(self.open_users_tab)
        self.pushButton_4.clicked.connect(self.open_settings_tab)
        
    def open_loans_tab(self):
        self.tabWidget.setCurrentIndex(0)
         
    
    def open_books_tab(self):
        self.tabWidget.setCurrentIndex(1)
    
    def open_users_tab(self):
        self.tabWidget.setCurrentIndex(2) 
    
    def open_settings_tab(self):
        self.tabWidget.setCurrentIndex(3)
        
