import sys
from PyQt5.QtWidgets import QApplication, QDialog, QPushButton, QVBoxLayout, QLineEdit, QWidget

class MyDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("My Dialog")
        
        self.button_close = QPushButton("Close Dialog")
        self.button_close.clicked.connect(self.on_close)
        
        self.line_edit_dialog = QLineEdit()
        
        layout = QVBoxLayout()
        layout.addWidget(self.line_edit_dialog)
        layout.addWidget(self.button_close)
        self.setLayout(layout)
        
    def on_close(self):
        main_window = self.parent()
        main_window.set_line_edit_text(self.line_edit_dialog.text())
        self.close()

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Main Window")
        
        self.line_edit_main = QLineEdit()
        self.button_open_dialog = QPushButton("Open Dialog")
        self.button_open_dialog.clicked.connect(self.open_dialog)
        
        layout = QVBoxLayout()
        layout.addWidget(self.line_edit_main)
        layout.addWidget(self.button_open_dialog)
        self.setLayout(layout)
        
    def open_dialog(self):
        dialog = MyDialog(self)
        dialog.exec_()
        
    def set_line_edit_text(self, text):
        self.line_edit_main.setText(text)

def main():
    app = QApplication(sys.argv)
    
    # Create the main window
    main_window = MainWindow()
    
    # Show the main window
    main_window.show()
    
    # Start the application event loop
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
