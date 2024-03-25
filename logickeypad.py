import sys
sys.path.append('./code/lib')

from keypad import Ui_Dialog  # Import the generated Python code from your UI file

# import QDialog
from PyQt5.QtWidgets import QDialog

class mykeypad(Ui_Dialog,QDialog):
    def __init__(self,parent=None):
        super().__init__(parent)
        self.setupUi(self)
    def setupUi(self,Dialog):
        super().setupUi(Dialog=Dialog)
        self.pb_0.clicked.connect(lambda: self.pb_clicked("0"))
        self.pb_1.clicked.connect(lambda: self.pb_clicked("1"))
        self.pb_2.clicked.connect(lambda: self.pb_clicked("2"))
        self.pb_3.clicked.connect(lambda: self.pb_clicked("3"))
        self.pb_4.clicked.connect(lambda: self.pb_clicked("4"))
        self.pb_5.clicked.connect(lambda: self.pb_clicked("5"))
        self.pb_6.clicked.connect(lambda: self.pb_clicked("6"))
        self.pb_7.clicked.connect(lambda: self.pb_clicked("7"))
        self.pb_8.clicked.connect(lambda: self.pb_clicked("8"))
        self.pb_9.clicked.connect(lambda: self.pb_clicked("9"))
        self.pb_del.clicked.connect(lambda: self.pb_clicked("del"))
        self.pb_c.clicked.connect(lambda: self.pb_clicked("c"))
        self.pb_cancel.clicked.connect(lambda: self.pb_clicked("cancel"))
        self.pb_submit.clicked.connect(lambda: self.pb_clicked("submit"))
        
        
    def pb_clicked(self,button):
        print("Button clicked"+ str(button))
        
        if button == "del":
            self.lineEdit.setText(self.lineEdit.text()[:-1])
        elif button == "c":
            self.lineEdit.setText("")
        elif button == "cancel":
            self.close()
        elif button == "submit":
            main_window = self.parent()
            main_window.line_edit.setText(self.lineEdit.text())
            self.close()
        else: 
            self.lineEdit.setText(self.lineEdit.text()+str(button))
            
    def get_value(self):
        return self.lineEdit.text()
        
        
    