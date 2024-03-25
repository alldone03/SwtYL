import sys
from PyQt5.QtWidgets import QApplication, QDialog, QPushButton, QVBoxLayout, QLineEdit

from logickeypad import mykeypad

class MyDialog(QDialog):
    def __init__(self):
        super().__init__()
        myui = mykeypad(self)
        myui.setupUi(self)
        

class MainWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Main Window")
        
        self.line_edit = QLineEdit()
        self.button = QPushButton('Show Dialog')
        
        self.button.clicked.connect(self.show_dialog_and_update_line_edit)
        
        layout = QVBoxLayout()
        layout.addWidget(self.button)
        layout.addWidget(self.line_edit)
        self.setLayout(layout)
        
    def show_dialog_and_update_line_edit(self):
        myui = mykeypad(self)
        myui.exec_()
        # Update the line edit after the dialog is closed
        # self.line_edit.setText("Dialog shown")

def main():
    app = QApplication(sys.argv)
    
    # Create the main window
    window = MainWindow()
    
    # Show the main window
    window.show()
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()