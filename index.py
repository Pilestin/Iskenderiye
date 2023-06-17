# PyQt5 imports for GUI
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.uic import loadUiType
# Other imports
import sys
import os
import time

# Path: Library\index.py
# Compare this snippet from Library\database\getBooks.py:

ui, _ = loadUiType(os.path.join(os.path.dirname(__file__), 'library_design.ui'))

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
        
    def handle_buttons(self):
        pass 
    
    def show_books(self):
        pass 
    
    
def main():
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    app.exec_()
        
        
if __name__ == '__main__':
    main()
