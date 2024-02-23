import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QHBoxLayout, QStackedWidget

class MyWindow(QWidget):
    def __init__(self):
        super().__init__()
        
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle('Change View Example')
        
        # Create stacked widget
        self.stacked_widget = QStackedWidget()
        self.setLayout(QVBoxLayout())
        self.layout().addWidget(self.stacked_widget)
        
        # Create views
        self.view1_layout = QVBoxLayout()
        self.view2_layout = QHBoxLayout()
        
        # Add widgets to view 1
        self.label_view1 = QLabel("This is View 1")
        self.view1_layout.addWidget(self.label_view1)
        self.button_view1 = QPushButton('Switch to View 2')
        self.button_view1.clicked.connect(self.switchToView2)
        self.view1_layout.addWidget(self.button_view1)
        
        # Add widgets to view 2
        self.label_view2 = QLabel("This is View 2")
        self.view2_layout.addWidget(self.label_view2)
        self.button_view2 = QPushButton('Switch to View 1')
        self.button_view2.clicked.connect(self.switchToView1)
        self.view2_layout.addWidget(self.button_view2)
        
        # Add views to stacked widget
        self.stacked_widget.addWidget(QWidget())
        self.stacked_widget.addWidget(QWidget())
        
        self.stacked_widget.widget(0).setLayout(self.view1_layout)
        self.stacked_widget.widget(1).setLayout(self.view2_layout)
        
        # Show view 1 by default
        self.switchToView1()
        
    def switchToView1(self):
        self.stacked_widget.setCurrentIndex(0)
        
    def switchToView2(self):
        self.stacked_widget.setCurrentIndex(1)
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWindow()
    window.setGeometry(100, 100, 400, 200)
    window.show()
    sys.exit(app.exec_())